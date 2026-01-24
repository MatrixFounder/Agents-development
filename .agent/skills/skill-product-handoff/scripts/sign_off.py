#!/usr/bin/env python3
import sys
import os
import uuid
import time

def sign_off(backlog_path):
    """
    Appends the APPROVAL_HASH to the backlog.
    Format: APPROVAL_HASH: <UUID>-<TIMESTAMP>-APPROVED
    """
    # Open in append mode (creates file if not exists)

    unique_id = uuid.uuid4()
    timestamp = int(time.time())
    hash_line = f"\nAPPROVAL_HASH: {unique_id}-{timestamp}-APPROVED\n"
    
    with open(backlog_path, 'a') as f:
        f.write(hash_line)
        
    print(f"SUCCESS: Signed off on {backlog_path}")
    print(f"Hash: {hash_line.strip()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sign_off.py <path_to_approved_backlog>")
        sys.exit(1)
        
    path = sys.argv[1]
    sign_off(path)
