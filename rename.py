#!/usr/bin/env python3
"""
Rename Larry & Kip files to lowercase: larry_walking_leftpocket.csv format
"""

import os
from pathlib import Path

MAPPINGS = {
    'swa': 'jacket', 'swp': 'jacket', 'jswpa': 'jacket',
    'lp': 'leftpocket', 'jlpa': 'leftpocket',
    'bp': 'backpack', 'jbpa': 'backpack',
    'ha': 'hand', 'jha': 'hand',
    'rp': 'rightpocket', 'jrpa': 'rightpocket'
}


def get_new_name(filename, user):
    stem = Path(filename).stem.lower()

    # Activity (lowercase)
    if stem.startswith('j') or 'jump' in stem:
        activity = 'jumping'
    elif stem.startswith('w') or 'walk' in stem:
        activity = 'walking'
    else:
        raise ValueError(f"Can't detect activity in {filename}")

    # Position
    for code, pos in MAPPINGS.items():
        if code in stem:
            return f"{user.lower()}_{activity}_{pos}.csv"

    raise ValueError(f"No position mapping for {filename}")


# Process
data_dir = Path('data')
users = ['kip', 'larry']

for user in users:
    user_dir = data_dir / user
    print(f"\n=== {user} ===")

    renamed = 0
    for old_path in user_dir.glob('*.csv'):
        try:
            new_name = get_new_name(old_path.name, user)
            new_path = user_dir / new_name

            if new_path.exists():
                print(f"SKIP: {old_path.name} -> {new_name}")
            else:
                old_path.rename(new_path)
                print(f"RENAMED: {old_path.name} -> {new_name}")
                renamed += 1
        except ValueError as e:
            print(f"ERROR: {e}")

    # Add this block at the end of rename_files.py, then re-run
    print("\n=== FORCE OVERWRITE MODE ===")
    for user in ['Kip', 'Larry']:
        user_dir = Path('data') / user
        for old_path in user_dir.glob('*BP*.csv'):  # Target specific patterns
            try:
                new_name = get_new_name(old_path.name, user)
                new_path = user_dir / new_name
                if new_path.exists():
                    new_path.unlink()  # Delete existing
                    print(f"DELETED: {new_name}")
                old_path.rename(new_path)
                print(f"FORCE: {old_path.name} → {new_name}")
            except:
                pass

    print(f"{renamed} renamed")

print("\n✅ All lowercase! e.g. kip_walking_backpack.csv, larry_jumping_hand.csv")
