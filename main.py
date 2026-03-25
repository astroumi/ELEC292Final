#hello world
#test
import h5py
import pandas as pd
import numpy as np

print ("fuuhhh")

with h5py.File('data') as hdf:

    #Create the main three data groups
    if 'Raw_Data' not in hdf:
        raw_group = hdf.create_group('Raw_Data')
    else:
        raw_group = hdf['Raw_Data']

    if 'Processed_Data' not in hdf:
        processed_group = hdf.create_group('Processed_Data')
    else:
        processed_group = hdf['Processed_Data']

    if 'Segmented_Data' not in hdf:
        segmented_group = hdf.create_group('Segmented_Data')
    else:
        segmented_group = hdf['Segmented_Data']

    #Fill group member data into raw_group
    if 'Kipras' not in raw_group:
        member_group = raw_group.create_group('Kipras')
    else:
        member_group = raw_group['Kipras']

    if 'Umair' not in raw_group:
        member_group = raw_group.create_group('Umair')
    else:
        member_group = raw_group['Umair']

    if 'Larry' not in raw_group:
        member_group = raw_group.create_group('Larry')
    else:
        member_group = raw_group['Larry']



#love kip<3
