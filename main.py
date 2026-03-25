import h5py
import pandas as pd
import numpy as np
import os

print ("fuuhhh")

#Setup names for paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_dir, "data")  # This is your main 'data' folder
h5_path = os.path.join(base_dir, "ELEC292_Project.h5")

#Open the folder at the end of the h5_path in append mode 'a'
with h5py.File(h5_path, 'a') as hdf:

    #Create the main three data groups
    raw_group = hdf.require_group('Raw_Data')

    processed_group = hdf.require_group('Processed_Data')

    segmented_group = hdf.require_group('Segmented_Data')

    #Fill group member data into raw_group
    member_group = raw_group.require_group('Kipras')

    member_group = raw_group.require_group('Umair')

    member_group = raw_group.require_group('Larry')


#love kip<3
