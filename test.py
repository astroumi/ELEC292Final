import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================
FILENAME = 'kip_jumping_backpack_1.csv'  # Change to your split filename
WINDOW_SIZES = [3, 5, 10, 20]


def preprocessing_test(raw_data, window):
    """Preprocessing without gravity removal for testing window impact."""
    time = raw_data[:, 0]

    # Interpolate missing data
    df_axes = pd.DataFrame(raw_data[:, 1:4], columns=['X', 'Y', 'Z'])
    df_axes = df_axes.interpolate(method='linear', limit_direction='both')

    # Rolling mean (The heart of the window test)
    df_smoothed = df_axes.rolling(window=window, center=True, min_periods=1).mean()

    # Magnitude calculation (Gravity remains included)
    mag = np.sqrt(df_smoothed['X'] ** 2 + df_smoothed['Y'] ** 2 + df_smoothed['Z'] ** 2)

    return pd.DataFrame({
        'time': time, 'X': df_smoothed['X'],
        'Y': df_smoothed['Y'], 'Z': df_smoothed['Z'], 'Magnitude': mag
    })


def run_matrix_test():
    # Setup Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data_split', FILENAME)

    if not os.path.exists(file_path):
        print(f"Error: {FILENAME} not found in 'data_split' folder.")
        return

    # Load Raw Data
    raw_df = pd.read_csv(file_path)
    raw_np = raw_df.to_numpy()

    # Create 4x4 Grid
    fig, axes = plt.subplots(4, 4, figsize=(16, 10), sharex='col', sharey='row')
    metrics = ['X', 'Y', 'Z', 'Magnitude']
    colors = ['red', 'blue', 'green', 'purple']

    for col_idx, w_size in enumerate(WINDOW_SIZES):
        # Process data for this window
        proc_df = preprocessing_test(raw_np, w_size)

        for row_idx, metric in enumerate(metrics):
            ax = axes[row_idx, col_idx]

            # Plot Raw in light gray as the "Ghost" background
            ax.plot(raw_df.iloc[:, 0], raw_df.iloc[:, row_idx + 1],
                    color='gray', alpha=0.2, label='Raw')

            # Plot Processed in bold
            ax.plot(proc_df['time'], proc_df[metric],
                    color=colors[row_idx], linewidth=1.2)

            # Labeling the top and left sides only
            if row_idx == 0:
                ax.set_title(f"Window: {w_size}", fontsize=12, fontweight='bold')
            if col_idx == 0:
                ax.set_ylabel(f"{metric} (m/s²)", fontweight='bold')

            ax.grid(True, alpha=0.2)

    fig.suptitle(f"Split File Window Comparison: {FILENAME}\n(Gravity Included)",
                 fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


if __name__ == "__main__":
    run_matrix_test()