import h5py
import pandas as pd
import numpy as np
import os

print ("fuuhhh")

#Setup names for paths
#Find the folder where the script is
base_dir = os.path.dirname(os.path.abspath(__file__))
#Points to the 'data' folder
data_folder = os.path.join(base_dir, "data")
#Defines a name for the HDF5 database file
h5_path = os.path.join(base_dir, "ELEC292_Project.h5")

#Open the folder at the end of the h5_path in append mode 'a'
with h5py.File(h5_path, 'a') as hdf:

    #Create the main three data groups
    raw_group = hdf.require_group('Raw_Data')
    processed_group = hdf.require_group('Processed_Data')
    segmented_group = hdf.require_group('Segmented_Data')

    #Fill group member data into raw_group
    for member_name in ['Kip', 'Umair', 'Larry']:
        #Creates path to the named folder
        member_path = os.path.join(data_folder, member_name)
        #Creates name for the member_group
        member_group = raw_group.require_group(member_name)

        #Loop through activities
        for activity in ['jumping', 'walking']:
            #Creates path to activity folder
            activity_path = os.path.join(data_folder, member_name, activity)
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








#love kip<3
