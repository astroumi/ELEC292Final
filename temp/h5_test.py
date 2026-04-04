from pathlib import Path
import h5py
import pandas as pd

base_dir = Path(__file__).resolve().parent
data_folder = base_dir / "data"
split_folder = base_dir / "data_split"
h5_path = base_dir / "ELEC292_Project.h5"

def init_hdf5():
    with h5py.File(h5_path, "a") as hdf:
        raw_group = hdf.require_group("Raw_Data")
        processed_group = hdf.require_group("Processed_Data")
        split_group = hdf.require_group("Split_Data")

        # Raw Data
        for member_name in ["kip", "umair", "larry"]:
            member_path = data_folder / member_name
            member_group = raw_group.require_group(member_name)

            for activity in ["jumping", "walking"]:
                activity_path = member_path / activity
                activity_group = member_group.require_group(activity)

                if not activity_path.exists():
                    print(f"WARNING: {activity_path} not found, skipping.")
                    continue

                for csv_file in activity_path.glob("*.csv"):
                    df = pd.read_csv(csv_file)
                    data_matrix = df.to_numpy()
                    dataset_name = csv_file.stem

                    if dataset_name in activity_group:
                        del activity_group[dataset_name]
                    activity_group.create_dataset(dataset_name, data=data_matrix,
                                                  compression="gzip", compression_opts=4)

        # Split (5s) Data
        for split_activity in ["jumping", "walking"]:
            split_activity_group = split_group.require_group(split_activity)
            split_activity_path = split_folder / split_activity

            if not split_activity_path.exists():
                print(f"WARNING: {split_activity_path} not found, skipping.")
                continue

            for csv_file in split_activity_path.glob("*.csv"):
                df = pd.read_csv(csv_file)
                data_matrix = df.to_numpy()
                dataset_name = csv_file.stem

                if dataset_name in split_activity_group:
                    del split_activity_group[dataset_name]
                split_activity_group.create_dataset(dataset_name, data=data_matrix,
                                                    compression="gzip", compression_opts=4)

    print("INFO: HDF5 Initialization Complete.")
    return 0