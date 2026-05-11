#!/usr/bin/env python3
"""
Script to verify RT04-App backup integrity
"""

import os
import json
import hashlib
from datetime import datetime

def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def verify_backup():
    print("🔍 Verifying RT04-App Backup Integrity")
    print("=" * 50)
    
    # Check critical files
    critical_files = [
        "index.html",
        "data.json", 
        "login.html",
        "style.css",
        "gist-sync.js"
    ]
    
    all_ok = True
    
    for file in critical_files:
        filepath = os.path.join(".", file)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {file}: {size:,} bytes")
            
            # Special checks for certain files
            if file == "data.json":
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    print(f"   ↳ Contains {len(data)} records")
                    if len(data) > 0:
                        print(f"   ↳ First record: {data[0].get('nama', 'N/A')}")
                except Exception as e:
                    print(f"   ❌ Error reading {file}: {e}")
                    all_ok = False
                    
            elif file == "index.html":
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    if "Dashboard RT 04/RW 11" in content:
                        print("   ↳ Contains dashboard")
                    if "refreshDashboard" in content:
                        print("   ↳ Contains refresh function")
                except Exception as e:
                    print(f"   ❌ Error reading {file}: {e}")
                    all_ok = False
                    
        else:
            print(f"❌ {file}: MISSING")
            all_ok = False
    
    # Count total files
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk("."):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.startswith('.'):
                filepath = os.path.join(root, file)
                total_files += 1
                total_size += os.path.getsize(filepath)
    
    print(f"\n📊 Backup Summary:")
    print(f"   Total files: {total_files}")
    print(f"   Total size: {total_size:,} bytes")
    print(f"   Backup date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for removed security files
    removed_files = ["security.js", "xss-fix.js", "data-encryption.js"]
    for file in removed_files:
        if os.path.exists(os.path.join(".", file)):
            print(f"⚠️  {file}: Still present (should be removed)")
        else:
            print(f"✅ {file}: Removed (as expected)")
    
    if all_ok:
        print("\n🎉 Backup verification PASSED")
        return True
    else:
        print("\n❌ Backup verification FAILED")
        return False

if __name__ == "__main__":
    # Change to backup directory
    backup_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(backup_dir)
    
    verify_backup()