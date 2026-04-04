from hdf import *
import h5py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    # Assign data by position
    time_data = df.iloc[:, 0]
    mag_data = df.iloc[:, 4]

    #Dark theme to match app
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.patch.set_facecolor('#111111')
    ax1.set_facecolor('#111111')
    ax2.set_facecolor('#111111')

    #Plot the raw magnitude signal on top with fill under curve
    ax1.plot(time_data, mag_data, color='#ff003c', linewidth=1.2)
    ax1.fill_between(time_data, mag_data, alpha=0.15, color='#ff003c')
    ax1.set_ylabel('Magnitude (m/s²)', color='#aaaaaa', fontsize=9)
    ax1.set_title('Acceleration Magnitude', color='white', fontsize=10, fontweight='bold')
    ax1.grid(True, alpha=0.1)
    ax1.tick_params(colors='#aaaaaa', labelsize=8)

    #Remove margins so line touches edges
    ax1.set_xlim(time_data.min(), time_data.max())
    ax1.margins(x=0)

    #Build the time and label arrays
    time_start = time_data.iloc[0]
    times = [time_start + i * window_sec for i in range(len(predictions))]
    labels = [int(pred) for pred in predictions]

    # Add endpoint so last prediction holds its value
    times.append(times[-1] + window_sec)
    labels.append(labels[-1])

    #Plot as a step chart
    ax2.step(times, labels, where='post', color='white', linewidth=1.5)

    #Fill only the half of the plot relevant to each prediction
    for i, pred in enumerate(predictions):
        end = times[i] + window_sec
        if pred == 0:
            #Walking fills the bottom half green
            ax2.axvspan(times[i], end, ymin=0, ymax=0.5, alpha=0.3, color='#00e676')
        else:
            #Jumping fills the top half red
            ax2.axvspan(times[i], end, ymin=0.5, ymax=1.0, alpha=0.3, color='#ff003c')

    #Set custom ytick labels
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['WALKING', 'JUMPING'], color='#aaaaaa', fontsize=8)
    ax2.set_xlabel('Time (s)', color='#aaaaaa', fontsize=9)
    ax2.set_title('Predicted Activity', color='white', fontsize=10, fontweight='bold')
    ax2.grid(True, alpha=0.1)
    ax2.tick_params(colors='#aaaaaa', labelsize=8)

    #Remove margins so step touches edges
    ax2.set_xlim(time_data.min(), time_data.max())
    ax2.margins(x=0)
    ax2.set_ylim(-0.1, 1.1)

    plt.tight_layout(pad=1.5)
    plt.show()

#Plot app results inside the app window
def plot_app_results_embedded(csv_path, predictions, window, window_sec=5):
    #Load the original CSV
    df = pd.read_csv(csv_path)

    # Assign data by position
    time_data = df.iloc[:, 0]
    mag_data = df.iloc[:, 4]

    #Dark theme to match app
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 4.5), constrained_layout=True)
    fig.patch.set_facecolor('#111111')
    ax1.set_facecolor('#111111')
    ax2.set_facecolor('#111111')

    #Plot the raw magnitude signal on top with fill under curve
    ax1.plot(time_data, mag_data, color='#ff003c', linewidth=1.2)
    ax1.fill_between(time_data, mag_data, alpha=0.15, color='#ff003c')
    ax1.set_ylabel('Magnitude (m/s²)', color='#aaaaaa', fontsize=8)
    ax1.set_title('Acceleration Magnitude', color='white', fontsize=9, fontweight='bold')
    ax1.grid(True, alpha=0.1)
    ax1.tick_params(colors='#aaaaaa', labelsize=7)

    #Remove margins so line touches edges
    ax1.set_xlim(time_data.min(), time_data.max())
    ax1.margins(x=0)

    #Build the time and label arrays
    time_start = time_data.iloc[0]
    times = [time_start + i * window_sec for i in range(len(predictions))]
    labels = [int(pred) for pred in predictions]

    # Add endpoint so last prediction holds its value
    times.append(times[-1] + window_sec)
    labels.append(labels[-1])

    #Plot as a step chart
    ax2.step(times, labels, where='post', color='white', linewidth=1.5)

    #Fill only the half of the plot relevant to each prediction
    for i, pred in enumerate(predictions):
        end = times[i] + window_sec
        if pred == 0:
            #Walking fills the bottom half green
            ax2.axvspan(times[i], end, ymin=0, ymax=0.5, alpha=0.3, color='#00e676')
        else:
            #Jumping fills the top half red
            ax2.axvspan(times[i], end, ymin=0.5, ymax=1.0, alpha=0.3, color='#ff003c')

    #Set custom ytick labels
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['WALKING', 'JUMPING'], color='#aaaaaa', fontsize=7)
    ax2.set_xlabel('Time (s)', color='#aaaaaa', fontsize=8)
    ax2.set_title('Predicted Activity', color='white', fontsize=9, fontweight='bold')
    ax2.grid(True, alpha=0.1)
    ax2.tick_params(colors='#aaaaaa', labelsize=7)

    #Remove margins so step touches edges
    ax2.set_xlim(time_data.min(), time_data.max())
    ax2.margins(x=0)
    ax2.set_ylim(-0.1, 1.1)

    plt.tight_layout(pad=1.2)

    #Embed in tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)