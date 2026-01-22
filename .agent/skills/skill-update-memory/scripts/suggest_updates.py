
import os
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

IGNORE_PATTERNS = {
    'node_modules', 'dist', 'build', '__pycache__', '.git', 
    '.DS_Store', 'package-lock.json', 'yarn.lock'
}
IGNORE_EXTS = {'.min.js', '.min.css', '.map', '.lock', '.pyc'}

def get_changed_files():
    # Try staged files first
    cmd = ["git", "diff", "--name-only", "--staged"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().splitlines()
    
    # Fallback to modified files (not staged)
    cmd = ["git", "diff", "--name-only"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def find_target_agents_file(file_path: str):
    path = Path(file_path).parent.resolve()
    root = Path.cwd()
    
    while path >= root:
        candidate = path / ".AGENTS.md"
        if candidate.exists():
            return candidate
        if path == root:
            break
        path = path.parent
        
    return root / ".AGENTS.md"

def generate_suggestion(files):
    grouped = defaultdict(list)
    
    for f in files:
        if any(p in f for p in IGNORE_PATTERNS):
            continue
        if Path(f).suffix in IGNORE_EXTS:
            continue
            
        target = find_target_agents_file(f)
        grouped[target].append(f)
        
    for target, file_list in grouped.items():
        print(f"\n### Target: {target.relative_to(Path.cwd())}")
        print("Suggested Updates:\n")
        
        for f in file_list:
            fname = Path(f).name
            print(f"#### [{fname}]")
            print(f"**Purpose:** [Update purpose for {fname}]")
            print("**Classes/Functions:**")
            print(f"- `ClassName` — [Description]")
            print()

if __name__ == "__main__":
    try:
        files = get_changed_files()
        if not files:
            print("No changed files found.")
        else:
            print(f"Found {len(files)} changed files.")
            generate_suggestion(files)
    except Exception as e:
        print(f"Error: {e}")
