# main.py
import sys
import os
from pathlib import Path

# Data pipeline imports
from hdf import init_hdf5, h5_path
from preprocessing import preprocess_data
from split import split_all, isolate_test_splits, reorganize_split_group_by_recording
from extraction import run_extraction
from training import run_training
from app import launch_app



def data_processing_menu():
    print("\n--- 2. Init Data Processing ---")
    print("a. Divide data randomly")
    print("b. Divide data by recording")
    print("c. Go back")

    choice = input("Input (a/b/c): ").strip().lower()

    if choice in ['a', 'b']:
        # Delete old HDF file
        if h5_path.exists():
            h5_path.unlink()
            print(f"\nINFO: Deleted old HDF file.")

        print("INFO: Building new HDF file...")
        init_hdf5()
        preprocess_data()
        split_all('hdf')

        # Execute the chosen split method
        if choice == 'a':
            isolate_test_splits()
        elif choice == 'b':
            reorganize_split_group_by_recording()

        print("\n--- Data Processing Complete ---")
    elif choice != 'c':
        print("Invalid choice. Returning to main menu.")


def extraction_menu():
    print("\n--- 3. Extract Features ---")
    print("a. Magnitude features only")
    print("b. XYZ and Magnitude features")
    print("c. Go back")

    choice = input("Input (a/b/c): ").strip().lower()

    if choice == 'a':
        print("\nINFO: Extracting Magnitude features...")
        run_extraction(mode='mag')
    elif choice == 'b':
        print("\nINFO: Extracting XYZ and Magnitude features...")
        run_extraction(mode='xyz_mag')
    elif choice != 'c':
        print("Invalid choice. Returning to main menu.")


def training_menu():
    print("\n--- 4. Train Model ---")
    print("a. Logistic Regression")
    print("b. K-Nearest Neighbors (KNN)")
    print("c. Go back")

    choice = input("Input (a/b/c): ").strip().lower()

    if choice in ['a', 'b']:
        # Check for and delete old model on disk
        model_path = Path("trained_model.pkl")  # Update this if you named it differently
        if model_path.exists():
            model_path.unlink()
            print("\nINFO: Deleted old model from disk.")

        if choice == 'a':
            # print("INFO: Training Logistic Regression...")
            run_training(model_type='lr')
        elif choice == 'b':
            # print("INFO: Training K-Nearest Neighbors...")
            run_training(model_type='knn')

    elif choice != 'c':
        print("Invalid choice. Returning to main menu.")



while True:
    print("\n════════════════════════════════════")
    print(" ELEC 292 Project - Run Controller ")
    print("════════════════════════════════════")
    print("1. Launch App (or press Enter)")
    print("2. Init Data Processing (Deletes old HDF)")
    print("3. Extract Features")
    print("4. Train Model (Deletes old Model)")
    print("5. Exit")

    choice = input("\nInput (1-5): ").strip().lower()

    if choice == '1' or choice == '':
        print("\n--- Launching App ---")
        launch_app()

    elif choice == '2':
        data_processing_menu()

    elif choice == '3':
        extraction_menu()

    elif choice == '4':
        training_menu()

    elif choice == '5':
        print("Exiting... peace and love <3")
        sys.exit()

    else:
        print("Invalid choice. Please select 1-5.")