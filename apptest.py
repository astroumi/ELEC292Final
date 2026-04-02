import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


    #Fill the step plot with colors to make reading easier
    for i, pred in enumerate(predictions):
        color = 'lightgreen' if pred == 0 else 'lightcoral'
        ax2.axvspan(times[i], times[i] + window_sec, alpha=0.3, color=color)

    ax2.set_xlabel('Time (s)')
    ax2.set_title('Predicted Activity over Time')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def fake_predictions(csv_path, window_sec=5, fs=100):
    import pandas as pd
    df = pd.read_csv(csv_path)
    n_windows = len(df) // (fs * window_sec)

    # Random probability of switching activity each window
    predictions = []
    current = np.random.randint(0, 2)
    for _ in range(n_windows):
        # 30% chance of switching activity each window
        if np.random.random() < 0.3:
            current = 1 - current
        predictions.append(current)

    return np.array(predictions)


predictions = fake_predictions(r'C:\Users\23qf31\PycharmProjects\ELEC292Final\data\kip\jumping\kip_jumping_backpack.csv')
plot_app_results(r'C:\Users\23qf31\PycharmProjects\ELEC292Final\data\kip\jumping\kip_jumping_backpack.csv', predictions)


