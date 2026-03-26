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
    for member_name in ['kipras', 'umair', 'larry']:
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
                    file_path = os.path.join(activity_path, filename)

            #Check if path exists
            if os.path.exists(member_path):
                print ("yay")
                for filename in os.listdir(member_path):
                    if filename.endswith(".csv"):
                        if filename




#love kip<3
