import h5py
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

#Function to make it easier to plot straight HDF5 datasets
def plot_hdf5_dataset(internal_path, title="Accelerometer Data"):
    #Pull data from HDF5
    with h5py.File(h5_path, 'r') as hdf:
        #Pull raw numbers
        data = hdf[internal_path][:]
        #Create the data frame
        df = pd.DataFrame(data)
        #Call the regular plotting function
        plot_accel_data(df, title=title if title else internal_path)


#Creates a figure with 4 sublots for X, Y, Z and magnitude stacked vertical
def plot_accel_data(df, title="Accelerometer Data"):
    #Sets up 4-row grid
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex='all')
    axes = [ax1, ax2, ax3, ax4]

    #Assign data by position
    time_data = df.iloc[:, 0]
    x_data = df.iloc[:, 1]
    y_data = df.iloc[:, 2]
    z_data = df.iloc[:, 3]
    mag_data = df.iloc[:, 4]

    # Plot X-Axis
    ax1.plot(time_data, x_data, color='red', label='X-axis')
    ax1.set_ylabel('X (m/s²)')
    ax1.set_title('X-axis acceleration vs time')

    # Plot Y-axis
    ax2.plot(time_data, y_data, color='blue', label='Y-axis')
    ax2.set_ylabel('Y (m/s²)')
    ax2.set_title('Y-axis acceleration vs time')

    # Plot Z-axis
    ax3.plot(time_data, z_data, color='green', label='Z-axis')
    ax3.set_ylabel('Z (m/s²)')
    ax3.set_title('Z-axis acceleration vs time')

    # Plot Magnitude
    ax4.plot(time_data, mag_data, color='purple', label='Magnitude')
    ax4.set_ylabel('Magnitude (m/s²)')
    ax4.set_title('Magnitude of acceleration vs time')

    # Formatting loop for all axes
    for ax in axes:
        ax.tick_params(labelbottom=True)
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    # Set x-axis limits
    plt.xlim(time_data.min(), time_data.max())

    # Set the main title
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Adjust layout to prevent the suptitle from overlapping
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

#Overlaps raw and processed data in 4 figure layout for comparison
def compare_raw_vs_processed(h5_path, raw_path, proc_path, title="Comparison"):
    with h5py.File(h5_path, 'r') as hdf:
        #Pull numerical data from both groups
        raw_data = hdf[raw_path][:]
        proc_data = hdf[proc_path][:]
        #Convert data to data frames
        df_raw = pd.DataFrame(raw_data)
        df_proc = pd.DataFrame(proc_data)

    #Sets up 4-row grid
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex='all')
    axes = [ax1, ax2, ax3, ax4]
    labels = ['X-Axis', 'Y-Axis', 'Z-Axis', 'Magnitude']

    #Loop through each plot
    for i, ax in enumerate(axes):
        col_idx = i + 1

        # Plot raw data: Thin, transparent red
        ax.plot(df_raw.iloc[:, 0], df_raw.iloc[:, col_idx],
                color='red', alpha=0.3, label='Raw (Noisy)')

        # Plot processed data: Solid black
        ax.plot(df_proc.iloc[:, 0], df_proc.iloc[:, col_idx],
                color='black', linewidth=1.2, label='Processed (Filtered)')

        # Labels and Styling
        ax.set_ylabel(f'{labels[i]} (m/s²)')
        ax.set_title(f'{labels[i]} comparison')
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelbottom=True)
        ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
        #Add Legend
        ax.legend(loc='upper right', fontsize='small')

    # Set x-axis limits
    plt.xlim(df_proc.iloc[:, 0].min(), df_proc.iloc[:, 0].max())

    #Set the main title
    fig.suptitle(title, fontsize=16, fontweight='bold')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

#Makes it easier to plot HDF5 files as 3D trajectories
def plot_hdf5_3d(internal_path, title=""):

    with h5py.File(h5_path, 'r') as hdf:
        #Pulls raw numbers
        data = hdf[internal_path][:]
        #Creates data frame
        df = pd.DataFrame(data)
        #Calls main 3D trajectory plot funciton
        plot_3d_trajectory(df, title=title if title else internal_path)

#Plot acceleration data as a 3D trajectory
def plot_3d_trajectory(df, title="3D Acceleration Path"):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    #Assign colums by position
    time = df.iloc[:, 0]
    x = df.iloc[:, 1]
    y = df.iloc[:, 2]
    z = df.iloc[:, 3]

    #Create a scatter plot where the color changes over time
    scatter = ax.scatter(x, y, z, c=time, cmap='viridis', s=5, alpha = 0.6)

    #Add a color bar to show time progressoin
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Time Progression (s)')

    #Labels
    ax.set_xlabel('X Acceleration (m/s²)')
    ax.set_ylabel('Y Acceleration (m/s²)')
    ax.set_zlabel('Z Acceleration (m/s²)')

    fig.suptitle(title, fontsize=15, fontweight='bold')
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

print("Preprocessing complete.")

#Test visualization
with h5py.File(h5_path, 'r') as hdf:
    #Plot processed
    plot_hdf5_dataset('/Processed_Data/kip/walking/kip_walking_backpack')
    #Plot processed
    plot_hdf5_dataset('/Processed_Data/kip/jumping/kip_jumping_backpack')
    #Plot Raw
    plot_hdf5_dataset('/Raw_Data/kip/walking/kip_walking_backpack')

    file_path = os.path.join(base_dir, 'data_split', 'kip_jumping_backpack_1.csv')
    plot_accel_data(pd.read_csv(file_path))

    # Define your paths
    raw_int_path = 'Raw_Data/kip/jumping/kip_jumping_backpack'
    proc_int_path = 'Processed_Data/kip/jumping/kip_jumping_backpack'

    # Run the comparison
    compare_raw_vs_processed(h5_path, raw_int_path, proc_int_path, title="Kip Jumping: Filter Verification")

    # The simple way (using your existing function)
    plot_hdf5_3d('Processed_Data/kip/jumping/kip_jumping_backpack')


    # #Segmented Data Group Set-up
    # for type in ['Train', 'Test']:
    #     #Creates path to type folder
    #     type_path = os.path.join(member_path, type)
    #     #Creates type folder
    #     type_path = member_group.require_group(type)






#love kip<3
