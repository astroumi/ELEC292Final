from pathlib import Path
from hdf import *

#### Defines which split to run on runtime
split_csv = False
split_hdf = True

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


########## SPLIT 35s CSV FILES TO 5s CSV FILES
if split_csv:
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

    print(f"\nCSV: {total_csv} total 5s csv files from {num_inputs} 35s csv files in output dir")

########## SPLIT 35s HDF DATASET to MANY 5s DATASETS IN DEFINED OUTPUT DIR
if split_hdf:
    total_hdf = 0
    num_inputs = 0
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

    print(f"\nHDF: Created {total_hdf} 5s datasets from {num_inputs} 35s datasets in output groups")