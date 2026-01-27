#!/usr/bin/env python3
import os
import argparse
import sys
import re

def parse_frontmatter(file_path):
    """
    Parses YAML frontmatter using a robust manual parser (Vanilla Python).
    Handles key-value, lists, quoted strings, and comments.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        lines = content.splitlines()
        # Basic check for frontmatter block
        if not lines or lines[0].strip() != '---':
            return {}, content

        frontmatter = {}
        found_end = False
        end_idx = 0
        current_list_key = None
        
        for i, line in enumerate(lines[1:], 1):
            line_stripped = line.split('#')[0].rstrip()
            
            if line_stripped.strip() == '---':
                found_end = True
                end_idx = i
                break
            
            if not line_stripped.strip(): 
                continue

            # Case 1: List Item (- value)
            if line_stripped.strip().startswith('-'):
                if current_list_key and isinstance(frontmatter.get(current_list_key), list):
                    val = line_stripped.strip()[1:].strip()
                    val = val.strip('"').strip("'")
                    frontmatter[current_list_key].append(val)
                continue

            # Case 2: Key-Value (key: value)
            if ':' in line_stripped:
                key, val = line_stripped.split(':', 1)
                key = key.strip()
                val = val.strip()
                
                if not val:
                    # Start of a list
                    current_list_key = key
                    frontmatter[key] = []
                else:
                    current_list_key = None
                    val = val.strip('"').strip("'")
                    
                    if val.startswith('[') and val.endswith(']'):
                         inner = val[1:-1]
                         val = [x.strip() for x in inner.split(',')]
                    
                    frontmatter[key] = val

        if not found_end:
            return {}, content
            
        return frontmatter, "\n".join(lines[end_idx+1:])

    except Exception as e:
        print(f"YAML Parse Error: {e}")
        return {}, content

def analyze_skill(skill_path):
    """
    Analyzes a skill directory for gaps against the Gold Standard.
    """
    skill_name = os.path.basename(os.path.normpath(skill_path))
    print(f"Analyzing '{skill_name}' at {skill_path}...")
    
    gaps = []
    
    # 1. Check SKILL.md existence
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md_path):
        print(f"CRITICAL: Missing SKILL.md in {skill_path}")
        return
        
    meta, body = parse_frontmatter(skill_md_path)
    body_lower = body.lower()

    # 2. Check CSO (Description)
    if 'description' in meta:
        desc = meta['description']
        # CSO Rule 1: Allowed Prefixes
        allowed_prefixes = ["use when", "guidelines for", "standards for", "defines", "helps with", "helps to"]
        desc_lower = desc.lower().strip()
        if not any(desc_lower.startswith(prefix) for prefix in allowed_prefixes):
            gaps.append(f"[CSO] Description should start with one of {allowed_prefixes}")
        
        if len(desc.split()) > 50:
             gaps.append(f"[CSO] Description too long ({len(desc.split())} words). Target < 50.")
    else:
        gaps.append("[Critical] Missing 'description' in frontmatter")

    # 3. Check Rationalization Resilience
    if "red flags" not in body_lower:
        gaps.append("[Resilience] Missing 'Red Flags' section")
    
    if "rationalization table" not in body_lower:
        gaps.append("[Resilience] Missing 'Rationalization Table'")

    # 5. Check Deep Logic (Passive Voice & Lazy TODOs)
    passive_keywords = ["should", "can", "suggested", "recommended", "encouraged", "might", "consider", "ideally", "optionally"]
    
    # Analyze line by line for context
    body_lines = body.splitlines()
    deep_logic_gaps = []
    
    for i, line in enumerate(body_lines, 1):
        line_lower = line.lower()
        found = [w for w in passive_keywords if re.search(r'\b' + re.escape(w) + r'\b', line_lower)]
        if found:
            snippet = line.strip()[:60] + "..." if len(line.strip()) > 60 else line.strip()
            deep_logic_gaps.append(f"Line {i}: Found {found} -> \"{snippet}\"")
            
    if deep_logic_gaps:
        gaps.append(f"[Deep Logic] Passive wording found. Rewrite to Imperative:\n    " + "\n    ".join(deep_logic_gaps[:5]))
        if len(deep_logic_gaps) > 5:
            gaps.append(f"    ... and {len(deep_logic_gaps) - 5} more.")

    if "todo" in body_lower:
        gaps.append("[Lazy] Found 'TODO' placeholder. Finish the skill.")

    # 6. Check Examples Content
    examples_dir = os.path.join(skill_path, "examples")
    if not os.path.isdir(examples_dir) or not os.listdir(examples_dir):
        gaps.append("[Richness] Missing or empty 'examples/' directory")
    else:
        for f in os.listdir(examples_dir):
            if f.startswith("."): continue
            fp = os.path.join(examples_dir, f)
            if os.path.getsize(fp) < 10:
                gaps.append(f"[Richness] Example '{f}' is too small/empty. Real examples required.")

    # 7. Check Token Efficiency (Inline Blocks)
    lines = body.splitlines()
    in_block = False
    block_start = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("```"):
            if in_block:
                # End of block
                block_length = i - block_start - 1
                if block_length > 12:
                    gaps.append(f"[Token Efficiency] Inline code block at line {block_start + 1} is too large ({block_length} lines). Max allowed is 12. Extract to examples/ or resources/.")
                in_block = False
            else:
                # Start of block
                in_block = True
                block_start = i

    # Report
    if gaps:
        print(f"⚠️  Gaps Detected for '{skill_name}':")
        for gap in gaps:
            print(f"  - {gap}")
        print("\nRecommendation: Run 'Execute Improvement Plan' to fix these gaps.")
        sys.exit(1) # Exit 1 to signal gaps found
    else:
        print(f"✅ No Gaps Found for '{skill_name}'. Skill is Gold Standard compliant.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Analyze a skill for Gold Standard compliance gaps.")
    parser.add_argument("path", help="Path to the skill directory")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.")
        sys.exit(1)

    analyze_skill(args.path)

if __name__ == "__main__":
    main()
