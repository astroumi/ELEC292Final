from hdf import *
import h5py
import matplotlib.pyplot as plt


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

#Plot app results
def plot_app_results(csv_path, predictions, window_sec=5):
    #Load the original CSV
    df = pd.read_csv(csv_path)

    #Set up layout
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,8), sharex=True)

    # Assign data by position
    time_data = df.iloc[:, 0]
    mag_data = df.iloc[:, 4]

    #Plot the raw magnitude signal on top
    ax1.plot(time_data, mag_data, color='purple', label='Magnitude')
    ax1.set_ylabel('Magnitude (m/s²)')
    ax1.set_xlabel('Time (s)')
    ax1.set_title('Magnitude of acceleration vs time')

    ax1.tick_params(labelbottom=True)
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    #Plot the predictions as a step plot of walking or jumping over time

    #Build the time and label arrays
    times = [i * window_sec for i in range(len(predictions))]
    labels = [int(pred) for pred in predictions]

    time_start = time_data.iloc[0]
    times = [time_start + i * window_sec for i in range(len(predictions))]

    #Plot as a step chart
    ax2.step(times, labels, where='post')

    #Set custom ytick labels
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Walking', 'Jumping'])


    #Fill the step plot with colors to make reading easier
    for i, pred in enumerate(predictions):
        color = 'lightgreen' if pred == 0 else 'lightcoral'
        ax2.axvspan(times[i], times[i] + window_sec, alpha=0.3, color=color)

    ax2.set_xlabel('Time (s)')
    ax2.set_title('Predicted Activity over Time')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()