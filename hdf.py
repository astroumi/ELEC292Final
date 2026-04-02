import h5py
from pathlib import Path
import pandas as pd

############################ ADDING DATA TO HDF

#Setup names for paths
#Find the folder where the script is
base_dir = Path(__file__).resolve().parent
data_folder = base_dir / "data"
split_folder = base_dir / "data_split"
h5_path = base_dir / "ELEC292_Project.h5"

def init_hdf5():
#Open the folder at the end of the h5_path in append mode 'a'
    with h5py.File(h5_path, 'a') as hdf:

        ######Create the main three data groups
        raw_group = hdf.require_group('Raw_Data')
        processed_group = hdf.require_group('Processed_Data')
        split_group = hdf.require_group('Split_Data')

        ##### Raw Data Group Set-up
        for member_name in ['kip', 'umair', 'larry']:
            #Creates path to the named folder
            member_path = data_folder / member_name
            #Creates name for the member_group
            member_group = raw_group.require_group(member_name)

            #Loop through activities
            for activity in ['jumping', 'walking']:
                #Creates path to activity folder
                activity_path = member_path / activity
                #Creates activity folder
                activity_group = member_group.require_group(activity)

                for csv_file in activity_path.glob("*.csv"):
                    # Read the CSV file into Pandas DataFrame
                    df = pd.read_csv(csv_file)
                    # Converth the data into a Numpy array
                    data_matrix = df.to_numpy()
                    # Remove the .csv for cleanliness
                    dataset_name = csv_file.stem
                    # Delete duplicates
                    if dataset_name in activity_group:
                        del activity_group[dataset_name]
                    activity_group.create_dataset(dataset_name, data=data_matrix)

        ############### ADDING 5s SPLIT CSV DATA TO HDF AS NUMPY MATRICES
        for split_activity in ['jumping', 'walking']:
            split_activity_group = split_group.require_group(split_activity) #group for hdf walking/jumping folders
            split_activity_path = split_folder / split_activity

            for csv_file in split_activity_path.glob("*.csv"):
                    # Read the CSV file into Pandas DataFrame
                    df = pd.read_csv(csv_file)
                    # Converth the data into a Numpy array
                    data_matrix = df.to_numpy()
                    # Remove the .csv for cleanliness
                    dataset_name = csv_file.stem
                    # Delete duplicates
                    if dataset_name in activity_group:
                        del activity_group[dataset_name]
                    # Save the dataset to the activity subgroup
                    activity_group.create_dataset(dataset_name, data=data_matrix)
    print("INFO: HDF5 Initialization Complete.")
    return 0