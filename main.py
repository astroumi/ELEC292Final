# main.py
import sys
from pathlib import Path

# Data pipeline imports
from hdf import init_hdf5, h5_path, appdata_dir, features_path, model_path
from preprocessing import preprocess_data
from split import split_all, isolate_test_splits, reorganize_split_group_by_recording
from extraction import run_extraction
from training import run_training
from app import launch_app

def default_run():
    print("\n--- 1. Default Setup/Training ---")

    if h5_path.exists():
        h5_path.unlink()
        print(f"\nINFO: Deleted old HDF file.")

    print("\nINFO: Building new HDF file...")
    init_hdf5()

    print("\nINFO: Preprocessing data...")
    preprocess_data()

    print("\nINFO: Splitting data and isolating test splits...")
    split_all('hdf')
    isolate_test_splits()

    if features_path.exists():
        features_path.unlink()
        print(f"\nINFO: Deleted old feature extraction file.")

    print("\nINFO: Extracting Magnitude features...")
    run_extraction(mode='mag')

    if model_path.exists():
        model_path.unlink()
        print("\nINFO: Deleted old model from disk.")

    run_training(model_type='lr')

    print("\nINFO: Default setup complete... please run app.")


while True:
    print("\n════════════════════════════════════")
    print(" ELEC 292 Project - Run Controller ")
    print("════════════════════════════════════")
    print("1. Launch App (or press Enter)")
    print("2. Default Setup/Training")
    print("3. Exit")

    choice = input("\nInput (1-3): ").strip().lower()

    if choice == '1' or choice == '':
        print("\n--- Launching App ---")
        launch_app()

    elif choice == '2':
        default_run()

    elif choice == '3':
        print("Exiting... peace and love <3")
        sys.exit()

    else:
        print("Invalid choice. Please select 1-3.")