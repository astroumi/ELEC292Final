#hello world
#test
import h5py
import pandas as pd
import numpy as np

print ("fuuhhh")

with h5py.File('data') as hdf:

    #Create the main three data groups
    raw_group = hdf.require_group('Raw_Data')

    processed_group = hdf.require_group('Processed_Data')

    segmented_group = hdf.require_group('Segmented_Data')

    #Fill group member data into raw_group
    member_group = raw_group.require_group('Kipras')

    member_group = raw_group.require_group('Umair')

    member_group = raw_group.require_group('Larry')



https://code-with-me.global.jetbrains.com/QXD5okIZCM-0wugTX5MmSw

#love kip<3
