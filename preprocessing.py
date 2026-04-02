import h5py
import pandas as pd
import numpy as np
from hdf import *


def preprocessing(raw_data):

    #raw_data_array: [Time, X, Y, Z, Abs]
    time = raw_data[:,0]

    #Linearly impute missing data
    df_axes = pd.DataFrame(raw_data[:, 1:4], columns=['X', 'Y', 'Z'])
    df_axes = df_axes.interpolate(method='linear', limit_direction='both')

    #Filter out high frequency noise with moving average
    #A window of size 5 is used
    df_smoothed = pd.DataFrame(df_axes, columns=['X', 'Y', 'Z'])
    df_smoothed = df_smoothed.rolling(window=5, center=True, min_periods=1).mean()

    #Calculate magnitude of acceleration from smooth X, Y, Z
    mag = np.sqrt(df_smoothed['X']**2 + df_smoothed['Y']**2 + df_smoothed['Z']**2)

    #Build the processed dataframe
    processed_df = pd.DataFrame({
        'time': time,
        'X': df_smoothed['X'],
        'Y': df_smoothed['Y'],
        'Z': df_smoothed['Z'],
        'Magnitude': mag
    })

    return processed_df

################## PREPROCESSING ALL HDF DATA

#Preprocessed Data Group Set-up
with h5py.File(h5_path, 'a') as hdf:
    for member_name in ['kip', 'umair', 'larry']:
        #Creates name for the member_group
        member_group = processed_group.require_group(member_name)

        #Loop through activities
        for activity in ['jumping', 'walking']:
            #Creates activity folder
            activity_group = member_group.require_group(activity)

            #Loop through every dataset stored in the raw group
            for dataset_name in raw_group[member_name][activity]:
                #Get the 2D array from the raw group
                raw_data = raw_group[member_name][activity][dataset_name][:]
                #Process the information inside
                processed_df = preprocessing(raw_data)

                #Delete duplicates and save processed data to HDF5
                if dataset_name in activity_group:
                    del activity_group[dataset_name]
                activity_group.create_dataset(dataset_name, data=processed_df.to_numpy())

print("INFO: Data Preprocessing Complete.")