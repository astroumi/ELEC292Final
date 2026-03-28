#!/usr/bin/env python3
"""
Split each 30-35s CSV into exactly 5s (500-sample) CSV files.
Naming: user_activity_position_windowN.csv
Assumes fs=100Hz → 5s=500 lines.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def split_csv_to_windows(csv_path, output_dir, fs=100, window_sec=5):
    """Split one CSV → multiple 5s CSVs"""
    window_len = int(fs * window_sec)  # 500

    df = pd.read_csv(csv_path)
    n_samples = len(df) #how many lines

    filename = csv_path.stem.lower()
    print(f"Splitting {csv_path.name}: {n_samples} samples")

    n_windows = n_samples // window_len
    created = 0

    for i in range(n_windows):
        start = i * window_len
        end = start + window_len

        window_df = df.iloc[start:end].reset_index(drop=True)

        # Name: kip_walking_backpack_window0.csv
        new_name = f"{filename}_{i+1}.csv"
        new_path = output_dir / new_name

        window_df.to_csv(new_path, index=False)
        created += 1

    print(f"Created {created} files (up to {n_windows * 5:.0f}s)")
    return created


# Main
input_dir = Path('data')
output_dir = Path('data_split')
output_dir.mkdir(exist_ok=True)

total_windows = 0
for csv_file in input_dir.rglob('*.csv'):
    if csv_file.stat().st_size > 2400:  # Skip tiny files
        n = split_csv_to_windows(csv_file, output_dir)
        total_windows += n

print(f"\n{total_windows} total 5s windows in output dir")