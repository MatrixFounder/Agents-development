#!/usr/bin/env python3
"""
Skill: security-audit
Script: run_audit.py
Purpose: Validate security using static analysis (secrets, patterns, deps) and external tools (bandit, slither).
Usage: python run_audit.py [project_path] [--scan-type all|deps|secrets|patterns|config|external]
"""
import subprocess
import json
import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Fix Windows console encoding for Unicode output
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

# ============================================================================
#  CONFIGURATION
# ============================================================================

SECRET_PATTERNS = [
    # API Keys & Tokens
    (r'api[_-]?key\s*[=:]\s*["\'][^"\']{10,}["\']', "API Key", "high"),
    (r'token\s*[=:]\s*["\'][^"\']{10,}["\']', "Token", "high"),
    (r'bearer\s+[a-zA-Z0-9\-_.]+', "Bearer Token", "critical"),
    
    # Cloud Credentials
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key", "critical"),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\'][^"\']+["\']', "AWS Secret", "critical"),
    (r'AZURE[_-]?[A-Z_]+\s*[=:]\s*["\'][^"\']+["\']', "Azure Credential", "critical"),
    (r'GOOGLE[_-]?[A-Z_]+\s*[=:]\s*["\'][^"\']+["\']', "GCP Credential", "critical"),
    
    # Database & Connections
    (r'password\s*[=:]\s*["\'][^"\']{4,}["\']', "Password", "high"),
    (r'(mongodb|postgres|mysql|redis):\/\/[^\s"\']+', "Database Connection String", "critical"),
    
    # Private Keys
    (r'-----BEGIN\s+(RSA|PRIVATE|EC)\s+KEY-----', "Private Key", "critical"),
    (r'ssh-rsa\s+[A-Za-z0-9+/]+', "SSH Key", "critical"),
    (r'0x[a-fA-F0-9]{64}', "Private Key (Hex)", "critical"),
    
    # JWT
    (r'eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+', "JWT Token", "high"),
]

DANGEROUS_PATTERNS = [
    # Injection risks
    (r'eval\s*\(', "eval() usage", "critical", "Code Injection risk"),
    (r'exec\s*\(', "exec() usage", "critical", "Code Injection risk"),
    (r'new\s+Function\s*\(', "Function constructor", "high", "Code Injection risk"),
    (r'child_process\.exec\s*\(', "child_process.exec", "high", "Command Injection risk"),
    (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "subprocess with shell=True", "high", "Command Injection risk"),
    
    # XSS risks
    (r'dangerouslySetInnerHTML', "dangerouslySetInnerHTML", "high", "XSS risk"),
    (r'\.innerHTML\s*=', "innerHTML assignment", "medium", "XSS risk"),
    (r'document\.write\s*\(', "document.write", "medium", "XSS risk"),
    
    # SQL Injection indicators
    (r'["\'][^"\']*\+\s*[a-zA-Z_]+\s*\+\s*["\'].*(?:SELECT|INSERT|UPDATE|DELETE)', "SQL String Concat", "critical", "SQL Injection risk"),
    (r'f"[^"]*(?:SELECT|INSERT|UPDATE|DELETE)[^"]*\{', "SQL f-string", "critical", "SQL Injection risk"),
    
    # Insecure configurations
    (r'verify\s*=\s*False', "SSL Verify Disabled", "high", "MITM risk"),
    (r'--insecure', "Insecure flag", "medium", "Security disabled"),
    (r'disable[_-]?ssl', "SSL Disabled", "high", "MITM risk"),
    
    # Unsafe deserialization
    (r'pickle\.loads?\s*\(', "pickle usage", "high", "Deserialization risk"),
    (r'yaml\.load\s*\([^)]*\)(?!\s*,\s*Loader)', "Unsafe YAML load", "high", "Deserialization risk"),
]

SKIP_DIRS = {
    'node_modules', '.git', 'dist', 'build', '__pycache__', '.venv', 'venv', '.next',
    '.cache', '.idea', '.vscode', 'vendor', 'tmp', 'coverage', '.tox', '.mypy_cache',
}
CODE_EXTENSIONS = {'.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.java', '.rb', '.php', '.sol', '.rs'}
CONFIG_EXTENSIONS = {'.json', '.yaml', '.yml', '.toml', '.env', '.env.local', '.env.development'}

# Self-exclusion: skip the scanner's own directory to prevent false positives
SELF_DIR = str(Path(__file__).resolve().parent)

# ============================================================================
#  HELPER FUNCTIONS
# ============================================================================

def run_command(cmd, cwd=None, shell=False):
    """Run a shell command, capture exit code, and report status."""
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    print(f"[*] Running: {cmd_str}")
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=shell, check=False, timeout=120)
        if result.returncode != 0:
            print(f"[!] {cmd_str} exited with code {result.returncode}")
    except FileNotFoundError:
        print(f"[!] Tool not found: {cmd[0] if isinstance(cmd, list) else cmd.split()[0]}")
    except subprocess.TimeoutExpired:
        print(f"[!] Timeout: {cmd_str} exceeded 120s limit")

def _should_skip_dir(dirpath: str) -> bool:
    """Check if directory should be skipped using basename matching."""
    parts = Path(dirpath).parts
    return any(part in SKIP_DIRS for part in parts)

def _is_self_path(filepath: str) -> bool:
    """Check if file is within the scanner's own directory (false positive prevention)."""
    try:
        return str(Path(filepath).resolve()).startswith(SELF_DIR)
    except (OSError, ValueError):
        return False

def detect_project_types(root_dir):
    """Detect project types based on file extensions."""
    types = set()
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if any(f.endswith(".sol") for f in files):
            types.add("solidity")
        if any(f.endswith(".py") for f in files):
            types.add("python")
        if any(f.endswith(".js") or f.endswith(".ts") for f in files):
            types.add("javascript")
        if any(f.endswith(".rs") for f in files) or "Cargo.toml" in files:
            types.add("rust")
    return list(types)

# ============================================================================
#  SCANNING FUNCTIONS
# ============================================================================

def scan_dependencies(project_path: str) -> Dict[str, Any]:
    """Validate supply chain security (OWASP A03)."""
    results = {"tool": "dependency_scanner", "findings": [], "status": "[OK] Secure"}
    
    lock_files = {
        "npm": ["package-lock.json", "npm-shrinkwrap.json"],
        "yarn": ["yarn.lock"],
        "pnpm": ["pnpm-lock.yaml"],
        "pip": ["requirements.txt", "Pipfile.lock", "poetry.lock"],
        "rust": ["Cargo.lock"],
    }
    
    for manager, files in lock_files.items():
        if manager == "pip" and (Path(project_path) / "requirements.txt").exists():
             continue # Requirements.txt is common, lock file check is stricter
        
        # Check if project type exists first
        is_type = False
        if manager in ["npm", "yarn", "pnpm"] and (Path(project_path) / "package.json").exists():
            is_type = True
        elif manager == "rust" and (Path(project_path) / "Cargo.toml").exists():
            is_type = True
            
        if is_type:
            has_lock = any((Path(project_path) / f).exists() for f in files)
            if not has_lock:
                results["findings"].append({
                    "type": "Missing Lock File",
                    "severity": "high",
                    "message": f"{manager}: No lock file found. Supply chain integrity at risk."
                })

    # Run npm audit if applicable
    if (Path(project_path) / "package.json").exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            try:
                audit_data = json.loads(result.stdout)
                vulnerabilities = audit_data.get("vulnerabilities", {})
                severity_count = {"critical": 0, "high": 0}
                for vuln in vulnerabilities.values():
                    sev = vuln.get("severity", "low").lower()
                    if sev in severity_count:
                        severity_count[sev] += 1
                
                if severity_count["critical"] > 0:
                    results["status"] = "[!!] Critical vulnerabilities"
                    results["findings"].append({
                        "type": "npm audit",
                        "severity": "critical",
                        "message": f"{severity_count['critical']} critical vulnerabilities in dependencies"
                    })
            except json.JSONDecodeError:
                pass
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
            
    return results

def scan_secrets(project_path: str) -> Dict[str, Any]:
    """Validate no hardcoded secrets (OWASP A02)."""
    results = {
        "tool": "secret_scanner",
        "findings": [],
        "status": "[OK] No secrets detected",
        "scanned_files": 0,
        "skipped_files": 0,
        "by_severity": {"critical": 0, "high": 0}
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CODE_EXTENSIONS and ext not in CONFIG_EXTENSIONS:
                continue
                
            filepath = Path(root) / file
            
            if _is_self_path(str(filepath)):
                continue
            
            results["scanned_files"] += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern, secret_type, severity in SECRET_PATTERNS:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            results["findings"].append({
                                "file": str(filepath.relative_to(project_path)),
                                "type": secret_type,
                                "severity": severity,
                                "count": len(matches)
                            })
                            if severity in results["by_severity"]:
                                results["by_severity"][severity] += len(matches)
            except Exception as e:
                results["skipped_files"] += 1
                print(f"[WARN] Skipped {filepath}: {e}", file=sys.stderr)
    
    if results["by_severity"]["critical"] > 0:
        results["status"] = "[!!] CRITICAL: Secrets exposed!"
    elif results["by_severity"]["high"] > 0:
        results["status"] = "[!] HIGH: Secrets found"
        
    results["findings"] = results["findings"][:15]
    return results

def scan_code_patterns(project_path: str) -> Dict[str, Any]:
    """Validate dangerous code patterns (OWASP A03 Injection)."""
    results = {
        "tool": "pattern_scanner",
        "findings": [],
        "status": "[OK] No dangerous patterns",
        "scanned_files": 0,
        "skipped_files": 0
    }
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CODE_EXTENSIONS:
                continue
                
            filepath = Path(root) / file
            
            if _is_self_path(str(filepath)):
                continue
            
            results["scanned_files"] += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line_num, line in enumerate(lines, 1):
                        for pattern, name, severity, category in DANGEROUS_PATTERNS:
                            if re.search(pattern, line, re.IGNORECASE):
                                results["findings"].append({
                                    "file": str(filepath.relative_to(project_path)),
                                    "line": line_num,
                                    "pattern": name,
                                    "severity": severity,
                                    "category": category,
                                    "snippet": line.strip()[:80]
                                })
            except Exception as e:
                results["skipped_files"] += 1
                print(f"[WARN] Skipped {filepath}: {e}", file=sys.stderr)
    
    critical = sum(1 for f in results["findings"] if f["severity"] == "critical")
    if critical > 0:
        results["status"] = f"[!!] CRITICAL: {critical} dangerous patterns"
    elif results["findings"]:
        results["status"] = "[?] Patterns found"
        
    results["findings"] = results["findings"][:20]
    return results

def scan_configuration(project_path: str) -> Dict[str, Any]:
    """Validate security configuration (OWASP A05 Misconfiguration)."""
    results = {"tool": "config_scanner", "findings": [], "status": "[OK] Config secure", "skipped_files": 0}
    
    config_issues = [
        (r'"DEBUG"\s*:\s*true', "Debug mode enabled", "high"),
        (r'debug\s*=\s*True', "Debug mode enabled", "high"),
        (r'"CORS_ALLOW_ALL".*true', "CORS allow all", "high"),
        (r'"Access-Control-Allow-Origin".*\*', "CORS wildcard", "high"),
    ]
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            ext = Path(file).suffix.lower()
            if ext not in CONFIG_EXTENSIONS:
                continue
            
            filepath = Path(root) / file
            
            if _is_self_path(str(filepath)):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern, issue, severity in config_issues:
                        if re.search(pattern, content, re.IGNORECASE):
                            results["findings"].append({
                                "file": str(filepath.relative_to(project_path)),
                                "issue": issue,
                                "severity": severity
                            })
            except Exception as e:
                results["skipped_files"] += 1
                print(f"[WARN] Skipped {filepath}: {e}", file=sys.stderr)
                
    if any(f["severity"] == "high" for f in results["findings"]):
        results["status"] = "[!] HIGH: Config issues"
        
    return results

def run_external_tools(project_path: str, types: List[str]):
    """Run external security tools based on project type."""
    print(f"\n{'='*60}")
    print(f"External Tools Scan: {', '.join(types)}")
    print(f"{'='*60}")
    
    cwd = project_path

    if "solidity" in types:
        run_command(["slither", "."], cwd=cwd)

    if "python" in types:
        run_command(["bandit", "-r", ".", "-q"], cwd=cwd)
        run_command(["safety", "check"], cwd=cwd)

    if "javascript" in types:
        if (Path(cwd) / "yarn.lock").exists():
            run_command(["yarn", "audit"], cwd=cwd)
        else:
            run_command(["npm", "audit"], cwd=cwd)

    if "rust" in types:
        run_command(["cargo", "audit"], cwd=cwd)
        run_command(["cargo", "clippy"], cwd=cwd)

# ============================================================================
#  MAIN
# ============================================================================

def run_full_scan(project_path: str, scan_type: str = "all") -> Dict[str, Any]:
    """Execute security validation scans."""
    
    report = {
        "project": project_path,
        "timestamp": datetime.now().isoformat(),
        "scan_type": scan_type,
        "scans": {},
        "summary": {
            "total_findings": 0,
            "critical": 0,
            "high": 0,
            "overall_status": "[OK] SECURE"
        }
    }
    
    scanners = {
        "deps": ("dependencies", scan_dependencies),
        "secrets": ("secrets", scan_secrets),
        "patterns": ("code_patterns", scan_code_patterns),
        "config": ("configuration", scan_configuration),
    }
    
    for key, (name, scanner) in scanners.items():
        if scan_type == "all" or scan_type == key:
            print(f"[*] Running {name} scan...")
            result = scanner(project_path)
            report["scans"][name] = result
            
            findings_count = len(result.get("findings", []))
            report["summary"]["total_findings"] += findings_count
            
            for finding in result.get("findings", []):
                sev = finding.get("severity", "low")
                if sev == "critical":
                    report["summary"]["critical"] += 1
                elif sev == "high":
                    report["summary"]["high"] += 1
    
    if report["summary"]["critical"] > 0:
        report["summary"]["overall_status"] = "[!!] CRITICAL ISSUES FOUND"
    elif report["summary"]["high"] > 0:
        report["summary"]["overall_status"] = "[!] HIGH RISK ISSUES"
    elif report["summary"]["total_findings"] > 0:
        report["summary"]["overall_status"] = "[?] REVIEW RECOMMENDED"
    
    return report

def main():
    parser = argparse.ArgumentParser(description="Security Audit Tool")
    parser.add_argument("project_path", nargs="?", default=".", help="Project directory")
    parser.add_argument("--scan-type", choices=["all", "deps", "secrets", "patterns", "config", "external"],
                        default="all", help="Type of scan")
    parser.add_argument("--output", choices=["json", "summary"], default="summary",
                        help="Output format")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.project_path):
        print(json.dumps({"error": f"Directory not found: {args.project_path}"}))
        sys.exit(1)
        
    # Run Pattern Matching Scans
    if args.scan_type != "external":
        result = run_full_scan(args.project_path, args.scan_type)
        
        if args.output == "summary":
            print(f"\n{'='*60}")
            print(f"Security Scan: {result['project']}")
            print(f"{'='*60}")
            print(f"Status: {result['summary']['overall_status']}")
            print(f"Total Findings: {result['summary']['total_findings']}")
            print(f"  Critical: {result['summary']['critical']}")
            print(f"  High: {result['summary']['high']}")
            
            total_skipped = sum(s.get('skipped_files', 0) for s in result['scans'].values())
            if total_skipped > 0:
                print(f"  ⚠ Skipped Files: {total_skipped} (see stderr)")
            print(f"{'='*60}\n")
            
            for scan_name, scan_result in result['scans'].items():
                print(f"\n{scan_name.upper()}: {scan_result['status']}")
                for finding in scan_result.get('findings', [])[:5]:
                    f_str = f"  - [{finding.get('severity', 'INFO').upper()}] {finding.get('type') or finding.get('pattern') or finding.get('issue')}"
                    if 'file' in finding:
                        f_str += f" in {finding['file']}"
                    if 'line' in finding:
                        f_str += f":{finding['line']}"
                    if 'message' in finding:
                         f_str += f" - {finding['message']}"
                    print(f_str)
        else:
            print(json.dumps(result, indent=2))

    # Run External Tools
    if args.scan_type == "all" or args.scan_type == "external":
        types = detect_project_types(args.project_path)
        if types:
            run_external_tools(args.project_path, types)

if __name__ == "__main__":
    main()
