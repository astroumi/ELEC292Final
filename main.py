import h5py
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def preprocessing(raw_data):

    #raw_data_array: [Time, X, Y, Z, Abs]
    time = raw_data[:,0]

    #Linearly imputate missing data
    df_axes = pd.DataFrame(raw_data[:, 1:4], columns=['X', 'Y', 'Z'])
    df_axes = df_axes.interpolate(method='linear', limit_direction='both')

    #Remove offset from gravity
    #Subtracts the mean from each axis to center the raw data around 0 m/s^2
    no_gravity = df_axes.values - np.mean(df_axes.values, axis=0)

    #Filter out high frequency noise with moving average
    #A window of size 5 is used
    df_smoothed = pd.DataFrame(no_gravity, columns=['X', 'Y', 'Z'])
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

#Creates a figure with 4 sublots for X, Y, Z and magnitude stacked vertical
def plot_accel_data(df, title="Accelerometer Data")
    #Sets up 4-row grid
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    #Plot X-Axis
    ax1.plot(df['time'], df['X'], color='red', label='X-axis')
    ax1.set_ylabel('X (m/s²)')
    ax1.grid(True, alpha=0.3)
    ax1.set_title('X-axis acceleration vs time')

    #Plot Y-axis
    ax2.plot(df['time'], df['Y'], color='blue', label='Y-axis')
    ax2.set_ylabel('Y (m/s²)')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Y-axis acceleration vs time')

    #Plot Z-axis
    ax3.plot(df['time'], df['Z'], color='green', label='Z-axis')
    ax3.set_zlabel('Z')
    ax3.grid(True, alpha=0.3)
    ax3.set_title('Z-axis acceleration vs time')

    #Plot Magnitude
    ax4.plot(df['time'], df['Magnitude'], color='purple', label='Magnitude')
    ax4.set_ylabel('Magnitude')
    ax4.grid(True, alpha=0.3)
    ax4.set_title('Magnitude of acceleration vs time')

    plt.tight_layout()
    plt.show()


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

    #Raw Data Group Set-up
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

    #Preprocessed Data Group Set-up
    for member_name in ['kip', 'umair', 'larry']:
        #Creates path to the named folder
        member_path = os.path.join(data_folder, member_name)
        #Creates name for the member_group
        member_group = processed_group.require_group(member_name)

        #Loop through activities
        for activity in ['jumping', 'walking']:
            #Creates path to activity folder
            activity_path = os.path.join(member_path, activity)
            #Creates activity folder
            activity_group = member_group.require_group(activity)

            #Loop through every dataset stored in the raw group
            for dataset_name in raw_group[member_name][activity]:
                #Get the 2D array from the raw group
                raw_data = raw_group[member_name][activity][dataset_name][:]
                #Process the information inside
                processed_signal = preprocessing(raw_data)

                #Delete duplicates
                if dataset_name in activity_group:
                    del activity_group[dataset_name]
                activity_group.create_dataset(dataset_name, data=processed_signal)

print("Preprocessing complete.")




    # #Segmented Data Group Set-up
    # for type in ['Train', 'Test']:
    #     #Creates path to type folder
    #     type_path = os.path.join(member_path, type)
    #     #Creates type folder
    #     type_path = member_group.require_group(type)






#love kip<3
