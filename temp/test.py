import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import h5py
from hdf import *

# ==========================================
# CONFIGURATION
# ==========================================
# FILENAME = 'umair_jumping_hand_1.csv'  # Change to your split filename
# WINDOW_SIZES = [2, 5, 10, 20]
#
#
# def preprocessing_test(raw_data, window):
#     """Preprocessing without gravity removal for testing window impact."""
#     time = raw_data[:, 0]
#
#     # Interpolate missing data
#     df_axes = pd.DataFrame(raw_data[:, 1:4], columns=['X', 'Y', 'Z'])
#     df_axes = df_axes.interpolate(method='linear', limit_direction='both')
#
#     # Rolling mean (The heart of the window test)
#     df_smoothed = df_axes.rolling(window=window, center=True, min_periods=1).mean()
#
#     # Magnitude calculation (Gravity remains included)
#     mag = np.sqrt(df_smoothed['X'] ** 2 + df_smoothed['Y'] ** 2 + df_smoothed['Z'] ** 2)
#
#     return pd.DataFrame({
#         'time': time, 'X': df_smoothed['X'],
#         'Y': df_smoothed['Y'], 'Z': df_smoothed['Z'], 'Magnitude': mag
#     })
#
#
# def run_matrix_test():
#     # Setup Paths
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_dir, 'data_split', 'jumping', FILENAME)
#
#     if not os.path.exists(file_path):
#         print(f"Error: {FILENAME} not found in 'data_split' folder.")
#         return
#
#     # Load Raw Data
#     raw_df = pd.read_csv(file_path)
#     raw_np = raw_df.to_numpy()
#
#     # Create 4x4 Grid
#     fig, axes = plt.subplots(4, 4, figsize=(16, 10), sharex='col', sharey='row')
#     metrics = ['X', 'Y', 'Z', 'Magnitude']
#     colors = ['red', 'blue', 'green', 'purple']
#
#     for col_idx, w_size in enumerate(WINDOW_SIZES):
#         # Process data for this window
#         proc_df = preprocessing_test(raw_np, w_size)
#
#         for row_idx, metric in enumerate(metrics):
#             ax = axes[row_idx, col_idx]
#
#             # Plot Raw in light gray as the "Ghost" background
#             ax.plot(raw_df.iloc[:, 0], raw_df.iloc[:, row_idx + 1],
#                     color='gray', alpha=0.5, label='Raw')
#
#             # Plot Processed in bold
#             ax.plot(proc_df['time'], proc_df[metric],
#                     color=colors[row_idx], linewidth=1.2)
#
#             # Labeling the top and left sides only
#             if row_idx == 0:
#                 ax.set_title(f"Window: {w_size}", fontsize=12, fontweight='bold')
#             if col_idx == 0:
#                 ax.set_ylabel(f"{metric} (m/s²)", fontweight='bold')
#
#             ax.grid(True, alpha=0.2)
#
#     fig.suptitle(f"Split File Window Comparison: {FILENAME}\n",
#                  fontsize=16, fontweight='bold')
#     plt.tight_layout(rect=[0, 0, 1, 0.95])
#     plt.show()
#
#
# if __name__ == "__main__":
#     run_matrix_test()




###### VISUALIZATION TESTS

# def plot_accel_data(df, title="Accelerometer Data"):
#     #Sets up 4-row grid
#     fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex='all')
#     axes = [ax1, ax2, ax3, ax4]
#
#     #Assign data by position
#     time_data = df.iloc[:, 0]
#     x_data = df.iloc[:, 1]
#     y_data = df.iloc[:, 2]
#     z_data = df.iloc[:, 3]
#     mag_data = df.iloc[:, 4]
#
#     # Plot X-Axis
#     ax1.plot(time_data, x_data, color='red', label='X-axis')
#     ax1.set_ylabel('X (m/s²)')
#     ax1.set_title('X-axis acceleration vs time')
#
#     # Plot Y-axis
#     ax2.plot(time_data, y_data, color='blue', label='Y-axis')
#     ax2.set_ylabel('Y (m/s²)')
#     ax2.set_title('Y-axis acceleration vs time')
#
#     # Plot Z-axis
#     ax3.plot(time_data, z_data, color='green', label='Z-axis')
#     ax3.set_ylabel('Z (m/s²)')
#     ax3.set_title('Z-axis acceleration vs time')
#
#     # Plot Magnitude
#     ax4.plot(time_data, mag_data, color='purple', label='Magnitude')
#     ax4.set_ylabel('Magnitude (m/s²)')
#     ax4.set_title('Magnitude of acceleration vs time')
#
#     # Formatting loop for all axes
#     for ax in axes:
#         ax.tick_params(labelbottom=True)
#         ax.grid(True, alpha=0.3)
#         ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
#
#     # Set x-axis limits
#     plt.xlim(time_data.min(), time_data.max())
#
#     # Set the main title
#     fig.suptitle(title, fontsize=16, fontweight='bold')
#
#     # Adjust layout to prevent the suptitle from overlapping
#     plt.tight_layout(rect=[0, 0, 1, 0.96])
#     plt.show()
#
# with h5py.File(h5_path, 'r') as hdf:
#     walking_data = hdf['Raw_Data/kip/walking/kip_walking_backpack'][:]
#     jumping_data = hdf['Raw_Data/kip/jumping/kip_jumping_backpack'][:]
#
# walking_df = pd.DataFrame(walking_data)
# jumping_df = pd.DataFrame(jumping_data)
#
# plot_accel_data(walking_df, title='Kip - Walking - Backpack')
# plot_accel_data(jumping_df, title='Kip - Jumping - Backpack')

# #Overlaps raw and processed data in 4 figure layout for comparison
# def compare_raw_vs_processed(h5_path, raw_path, proc_path, title="Comparison"):
#     with h5py.File(h5_path, 'r') as hdf:
#         #Pull numerical data from both groups
#         raw_data = hdf[raw_path][:]
#         proc_data = hdf[proc_path][:]
#         #Convert data to data frames
#         df_raw = pd.DataFrame(raw_data)
#         df_proc = pd.DataFrame(proc_data)
#
#     #Sets up 4-row grid
#     fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 12), sharex='all')
#     axes = [ax1, ax2, ax3, ax4]
#     labels = ['X-Axis', 'Y-Axis', 'Z-Axis', 'Magnitude']
#
#     #Loop through each plot
#     for i, ax in enumerate(axes):
#         col_idx = i + 1
#
#         # Plot raw data: Thin, transparent red
#         ax.plot(df_raw.iloc[:, 0], df_raw.iloc[:, col_idx],
#                 color='red', alpha=0.3, label='Raw (Noisy)')
#
#         # Plot processed data: Solid black
#         ax.plot(df_proc.iloc[:, 0], df_proc.iloc[:, col_idx],
#                 color='black', linewidth=1.2, label='Processed (Filtered)')
#
#         # Labels and Styling
#         ax.set_ylabel(f'{labels[i]} (m/s²)')
#         ax.set_title(f'{labels[i]} comparison')
#         ax.grid(True, alpha=0.3)
#         ax.tick_params(labelbottom=True)
#         ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
#         #Add Legend
#         ax.legend(loc='upper right', fontsize='small')
#
#     # Set x-axis limits
#     plt.xlim(df_proc.iloc[:, 0].min(), df_proc.iloc[:, 0].max())
#
#     #Set the main title
#     fig.suptitle(title, fontsize=16, fontweight='bold')
#
#     plt.tight_layout(rect=[0, 0, 1, 0.96])
#     plt.show()
#
# compare_raw_vs_processed(h5_path,
#                          raw_path='Raw_Data/kip/walking/kip_walking_backpack',
#                          proc_path='Processed_Data/kip/walking/kip_walking_backpack',
#                          title='Kip - Walking - Backpack - Raw vs Processed')
#
#
# #Plot acceleration data as a 3D trajectory
# def plot_3d_trajectory(df, title="3D Acceleration Path"):
#     fig = plt.figure(figsize=(10, 8))
#     ax = fig.add_subplot(111, projection='3d')
#
#     #Assign colums by position
#     time = df.iloc[:, 0]
#     x = df.iloc[:, 1]
#     y = df.iloc[:, 2]
#     z = df.iloc[:, 3]
#
#     #Create a scatter plot where the color changes over time
#     scatter = ax.scatter(x, y, z, c=time, cmap='viridis', s=5, alpha = 0.6)
#
#     #Add a color bar to show time progressoin
#     cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
#     cbar.set_label('Time Progression (s)')
#
#     #Labels
#     ax.set_xlabel('X Acceleration (m/s²)')
#     ax.set_ylabel('Y Acceleration (m/s²)')
#     ax.set_zlabel('Z Acceleration (m/s²)')
#
#     fig.suptitle(title, fontsize=15, fontweight='bold')
#     plt.show()
#
# positions = ['hand', 'rightpocket', 'leftpocket', 'backpack', 'jacket']
#
# with h5py.File(h5_path, 'r') as hdf:
#     for position in positions:
#         dataset_name = f'umair_walking_{position}'
#         if dataset_name in hdf['Raw_Data/umair/walking']:
#             data = hdf[f'Raw_Data/umair/walking/{dataset_name}'][:]
#             df = pd.DataFrame(data)
#             plot_3d_trajectory(df, title=f'Kip - Walking - {position.capitalize()}')
#         else:
#             print(f'Dataset {dataset_name} not found')


#
# with h5py.File(h5_path, 'r') as hdf:
#     walking_data = hdf['Raw_Data/kip/walking/kip_walking_rightpocket'][:]
#     jumping_data = hdf['Raw_Data/kip/jumping/kip_jumping_rightpocket'][:]
#
# walking_df = pd.DataFrame(walking_data)
# jumping_df = pd.DataFrame(jumping_data)
#
# plot_3d_trajectory(walking_df, title='Kip - Walking - Right Pocket - 3D Trajectory')
# plot_3d_trajectory(jumping_df, title='Kip - Jumping - Right Pocket - 3D Trajectory')