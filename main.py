#hello world
#test
import h5py
import pandas as pd
import numpy as np

print ("fuuhhh")

with h5py.File('C:\Users\23qf31\ELEC 292\292_Final_Project_Files\RawAccelerationData') as hdf:

    raw_group = hdf.create_group('Raw_Data')
    processed_group = hdf.create_group('Processed_Data')
    segmented_group = hdf.create_group('Segmented_Data')

#love kip<3
