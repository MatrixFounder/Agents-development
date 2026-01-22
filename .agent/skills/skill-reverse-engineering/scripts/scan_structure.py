
import os
import sys
import argparse
from pathlib import Path

IGNORE_DIRS = {
    '.git', '.idea', '.vscode', '__pycache__', 'node_modules', 
    'dist', 'build', 'coverage', '.DS_Store', 'venv', '.venv'
}

IGNORE_EXTS = {
    '.pyc', '.o', '.so', '.class', '.lock', '.log'
}

def scan_directory(root_path: Path, max_depth: int = 2):
    print(f"## Directory Scan: {root_path.resolve()}\n")
    
    summary = []
    
    for item in root_path.iterdir():
        if item.name in IGNORE_DIRS or item.name.startswith('.'):
            continue
            
        if item.is_dir():
            print(f"### 📁 {item.name}/")
            file_count = 0
            subdirs = 0
            exts = {}
            
            for root, dirs, files in os.walk(item):
                if any(p in Path(root).parts for p in IGNORE_DIRS):
                    continue
                
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
                
                subdirs += len(dirs)
                for f in files:
                    ext = Path(f).suffix
                    if ext not in IGNORE_EXTS:
                        file_count += 1
                        exts[ext] = exts.get(ext, 0) + 1
            
            # Identify dominant language
            dominant = max(exts.items(), key=lambda x: x[1])[0] if exts else "N/A"
            
            print(f"- Files: {file_count}")
            print(f"- Subdirectories: {subdirs}")
            print(f"- Dominant Type: {dominant} ({exts.get(dominant, 0)})\n")
            
            summary.append((item.name, file_count, dominant))
            
    print("## Summary Table")
    print("| Directory | Files | Type |")
    print("|-----------|-------|------|")
    for name, count, dom in summary:
        print(f"| {name:<9} | {count:<5} | {dom:<4} |")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan directory structure for reverse engineering.")
    parser.add_argument("path", nargs="?", default=".", help="Root path to scan")
    parser.add_argument("--depth", type=int, default=2, help="Max depth for summary")
    
    args = parser.parse_args()
    scan_directory(Path(args.path), args.depth)
