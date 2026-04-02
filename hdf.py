import h5py
import os
import pandas as pd

############################ ADDING DATA TO HDF

#Setup names for paths
#Find the folder where the script is
base_dir = os.path.dirname(os.path.abspath(__file__))
#Points to the 'data' folder
data_folder = os.path.join(base_dir, "data")
split_folder = os.path.join(base_dir, "data_split")
#Defines a name for the HDF5 database file
h5_path = os.path.join(base_dir, "ELEC292_Project.h5")


#Open the folder at the end of the h5_path in append mode 'a'
with h5py.File(h5_path, 'a') as hdf:

    ######Create the main three data groups
    raw_group = hdf.require_group('Raw_Data')
    processed_group = hdf.require_group('Processed_Data')
    split_group = hdf.require_group('Split_Data')

    ##### Raw Data Group Set-up
    for member_name in ['kip', 'umair', 'larry']:
        #Creates path to the named folder
        member_path = os.path.join(data_folder, member_name)
        #Creates name for the member_group
        member_group = raw_group.require_group(member_name)

        #Loop through activities
        for activity in ['jumping', 'walking']:
            #Creates path to activity folder
            activity_path = os.path.join(member_path, activity)
            #Creates activity folder
            activity_group = member_group.require_group(activity)

            for filename in os.listdir(activity_path):
                if filename.endswith(".csv"):
                    #Creates a path to the file
                    file_path = os.path.join(activity_path, filename)
                    #Read the CSV file into Pandas DataFrame
                    df = pd.read_csv(file_path)
                    #Converth the data into a Numpy array
                    data_matrix = df.to_numpy()
                    #Remove the .csv for cleanliness
                    dataset_name = filename.replace(".csv", "")
                    #Delete duplicates
                    if dataset_name in activity_group:
                        del activity_group[dataset_name]
                    #Save the dataset to the activity subgroup
                    activity_group.create_dataset(dataset_name, data=data_matrix)

    ############### ADDING 5s SPLIT CSV DATA TO HDF AS NUMPY MATRICES
    for split_activity in ['jumping', 'walking']:
        split_activity_group = split_group.require_group(split_activity) #group for hdf walking/jumping folders
        split_activity_path = os.path.join(split_folder, split_activity) #path to walking/jumping folder where 5s .csv files live

        for filename in os.listdir(split_activity_path):
            if filename.endswith(".csv"):
                # Creates a path to the individual 5s .csv file
                file_path = os.path.join(split_activity_path, filename)
                # Read the CSV file into Pandas DataFrame
                df = pd.read_csv(file_path)
                # Convert the data into a Numpy array
                data_matrix = df.to_numpy()
                # Remove the .csv for cleanliness
                dataset_name = filename.replace(".csv", "")
                # Delete duplicates
                if dataset_name in activity_group:
                    del activity_group[dataset_name]
                # Save the dataset to the activity subgroup
                activity_group.create_dataset(dataset_name, data=data_matrix)

print("INFO: HDF5 Initialization Complete.")