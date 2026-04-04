from pathlib import Path
from hdf import *
import numpy as np

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

def split_df_in_memory(processed_df, fs=100, window_sec=5):
    """Split one CSV → multiple 5s CSVs but keeps output in memory"""
    window_len = int(fs * window_sec)

    # df = pd.read_csv(csv_path)
    n_samples = len(processed_df) #how many lines

    windows = [] #creates windows array

    #Compute number of windows
    n_windows = n_samples // window_len

    for i in range(n_windows):
        start = i * window_len
        end = start + window_len
        windows_df = processed_df.iloc[start:end].reset_index(drop=True)
        windows.append(windows_df)

    return windows

def split_hdf_dataset(dataset: h5py.Dataset, dest_group: h5py.Group, fs=100, window_sec=5):
    ####### SPLITS HDF DATASET INTO MANY 5s DATASETS IN DESTINATION GROUP
    window_len = int(fs * window_sec)  # 500

    n_samples = dataset.shape[0]
    n_windows = n_samples // window_len
    created = 0

    curr_name = dataset.name.split('/')[-1]
    for i in range(n_windows):
        #setup window
        start = i * window_len
        end = start + window_len

        #get window data from dataset
        window_data = dataset[start:end, :]
        window_name = f"{curr_name}_{i+1}"

        #add 5s window dataset to destination group/folder
        if window_name in dest_group:
            del dest_group[window_name]
        dest_group.create_dataset(window_name, data=window_data)
        created += 1

    # print(f"Created {created} datasets (up to {n_windows * 5:.0f}s)")
    return created

def split_all(type: str):
    ########## SPLIT 35s CSV FILES TO 5s CSV FILES
    if type == 'csv':
        input_dir = Path('data')
        output_dir = Path('data_split')
        output_dir.mkdir(exist_ok=True)

        num_inputs = 0
        total_csv = 0

        for csv_file in input_dir.rglob('*.csv'):
            if csv_file.stat().st_size > 2400:  # Skip tiny files
                n = split_csv_to_windows(csv_file, output_dir)
                num_inputs += 1
                total_csv += n

        print(f"INFO: Created {total_csv} total 5s csv files from {num_inputs} 35s csv files in output dir")

    ########## SPLIT 35s HDF DATASET to MANY 5s DATASETS IN DEFINED OUTPUT DIR
    if type == 'hdf':
        with h5py.File(h5_path, 'a') as hdf:
            total_hdf = 0
            num_inputs = 0
            processed_group = hdf['Processed_Data']
            split_group = hdf['Split_Data']
            for member_name in ['kip', 'umair', 'larry']:
                member_group = processed_group[member_name]

                for activity in ['jumping', 'walking']:
                    activity_group = member_group[activity]
                    dest_group = split_group.require_group(activity)

                    for input_name, input_data in activity_group.items():
                        if not isinstance(input_data, h5py.Dataset):
                            continue
                        num_inputs += 1
                        total_hdf += split_hdf_dataset(input_data, dest_group) #splits each 35s dataset into many 5s datasets in destination group

            print(f"INFO: Created {total_hdf} 5s datasets from {num_inputs} 35s datasets in output groups")
    return 0

def isolate_test_splits(seed: int = 42):
    # Picks 10 random datasets from walking and jumping (~10%) and isolates them in testing folder, restructures Split_Data group to accomodate
    np.random.seed(seed)  # Reproducible randomness
    print("INFO: Isolating test splits.")
    with h5py.File(h5_path, "a") as hdf:
        split_group = hdf["Split_Data"]

        for activity in ["walking", "jumping"]:
            activity_group = split_group[activity]

            # Get all dataset names in this activity group
            all_names = []
            for name, obj in activity_group.items():
                if isinstance(obj, h5py.Dataset):
                    all_names.append(name)

            # Randomly pick 10 unique datasets for testing
            test_names = list(np.random.choice(all_names, size=10, replace=False))
            # Gets rest of dataset names for training
            train_names = [n for n in all_names if n not in test_names]

            # Create destination subgroups
            train_group = split_group.require_group(f"training/{activity}")
            test_group  = split_group.require_group(f"testing/{activity}")

            # Copy datasets to training
            for name in train_names:
                if name in train_group:
                    del train_group[name] #delete duplicates if run multiple times
                hdf.copy(activity_group[name], train_group, name=name)

            # Copy datasets to testing
            for name in test_names:
                if name in test_group:
                    del test_group[name] #delete duplicates if run multiple times
                hdf.copy(activity_group[name], test_group, name=name)

            # Delete the original flat activity group not that all datasets are in training/testing
            del split_group[activity]

            print(f"    {activity}: {len(train_names)} training, {len(test_names)} testing")

    print(f"INFO: Test splits randomly separated.")

    return 0

def reorganize_split_group_by_recording(seed: int = 42) -> None:
    """
    Splits by RECORDING (35s trial), not by individual window.
    Picks 2 full recordings per activity for testing, rest go to training.
    All 5s windows from a recording stay together in the same split.
    """
    np.random.seed(seed)

    with h5py.File(h5_path, "a") as hdf:
        split_group = hdf["Split_Data"]

        # Remove old training/testing if they exist
        for key in ["training", "testing"]:
            if key in split_group:
                del split_group[key]

        for activity in ["walking", "jumping"]:
            activity_group = split_group[activity]

            all_names = [
                name for name, obj in activity_group.items()
                if isinstance(obj, h5py.Dataset)
            ]

            # Group windows by their parent recording (strip _N suffix)
            import re
            recordings = {}
            for name in all_names:
                base = re.sub(r'_\d+$', '', name)
                recordings.setdefault(base, []).append(name)

            # Randomly pick 2 full recordings for testing
            all_bases = list(recordings.keys())
            test_bases = list(np.random.choice(all_bases, size=2, replace=False))
            train_bases = [b for b in all_bases if b not in test_bases]

            train_grp = split_group.require_group(f"training/{activity}")
            test_grp  = split_group.require_group(f"testing/{activity}")

            for base in train_bases:
                for name in recordings[base]:
                    hdf.copy(activity_group[name], train_grp, name=name)

            for base in test_bases:
                for name in recordings[base]:
                    hdf.copy(activity_group[name], test_grp, name=name)

            print(f"{activity}: {len(train_bases)} recordings → training, "
                  f"{len(test_bases)} recordings → testing "
                  f"({sum(len(recordings[b]) for b in test_bases)} test windows)")

        # Remove old flat activity groups
        for activity in ["walking", "jumping"]:
            if activity in split_group:
                del split_group[activity]

    print("INFO: Test splits isolated by recording.")