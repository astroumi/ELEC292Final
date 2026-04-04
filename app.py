import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import joblib
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path

from training import *
from visualization import plot_app_results_embedded

from extraction import extract_features
from split import split_csv_in_memory

#Global Variables
selected_filename = ""

#Allows user to choose file from computer, executed when "File" button is pushed
def open_file():
    global selected_filename
    #Opens file browser so that user can pick csv file
    filename = filedialog.askopenfilename()

    #Check if .csv file was selected
    if filename and filename.endswith('.csv'):
        #Store it in the global variable
        selected_filename = filename
        #Print the filename
        print(f"Selected: {selected_filename}")
        file_string.set("Selected:" + selected_filename)
        return selected_filename
    else:
        file_string.set("Please select a .csv file")
        print('Please select a .csv file')
    return None

#Runs the check for whether file contains walking or jumping info, executed when 'Check' button is pushed
def check ():
    global selected_filename
    #Check if a file was selected
    if not selected_filename:
        file_string.set("Please select a .csv file first")
        print('Please select a file first')
        return None

    #Use 'try' to gracefully handle errors
    try:
        answer_string.set("Processing...")

        #Preprocess data before splitting into windows (cleans up blemishes)
        processed = process_app(selected_filename)
        #Split the data into 5 second windows make a windows list out of them
        windows = split_csv_in_memory(processed)

        #Extract features
        all_features = []
        for window_data in windows:
            features = extract_features(window_data.values)
            all_features.append(features)

        #Run the classifier on every window and add 0s or 1s to a predictions array
        predictions = lr_model.predict(all_features)

        #Count results
        walking_count = sum(predictions == 0)
        jumping_count = sum(predictions == 1)

        if walking_count > jumping_count:
            answer_string.set("Mostly walking!!!")
        else:
            answer_string.set("Mostly jumping!!!")

        #Save results to CSV
        save_results_to_csv(predictions)

        #Plot results
        plot_app_results_embedded(selected_filename, predictions, plot_frame)

    except Exception as e:
        print(f"Something went wrong: {e}")
        answer_string.set("Error - check console")
    return None

#Save predictions to a CSV file
def save_results_to_csv(predictions, window_sec=5):
    rows = []
    #Loop through every time frame and add it to the rows list
    for i, pred in enumerate(predictions):
        window_num = i + 1
        start_time = i * window_sec
        end_time = start_time + window_sec
        label = 'walking' if pred == 0 else 'jumping'
        rows.append({
            'window': window_num,
            'time': start_time,
            'end_time': end_time,
            'label': label
        })

        #Save just the filename and add _predictions
        raw_name = Path(selected_filename).stem
        suggested_name = f"{raw_name}_predictions"

    #Convert list of dictionaries into a pandas dataframe
    output_df = pd.DataFrame(rows)
    #Allows user to choose where to save the file and what to name it
    output_path = filedialog.asksaveasfilename(
        #Automatically adds .csv to the file name if not added
        defaultextension='.csv',
        #Suggest a file name
        initialfile=suggested_name,
        #Restricts the file browser to only show CSV files so users can't save it to the wrong format
        filetypes=[('CSV files', '*.csv')]
    )

    #Saves the dataframe to a csv in the output path
    if output_path:
        output_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")


#Clears the window
def clear():
    global selected_filename
    selected_filename = ""
    file_string.set("")
    answer_string.set("_ _ _")

    #Clear plot if one exists
    for plot in plot_frame.winfo_children():
        plot.destroy()




#Window
window = tk.Tk()
window.title('ELEC292 Final Project')
window.geometry('1000x1000')
window.configure(bg='#0d0d0d')
window.resizable(False, False)

#═══════════════════════════════════════
#  HEADER
#═══════════════════════════════════════
header = tk.Frame(master=window, bg='#0d0d0d')
header.pack(fill='x', pady=(15,0))

tk.Label(master=header, text='M O T I O N',
         font=('Helvetica', 38, 'bold'),
         fg='#ff003c', bg='#0d0d0d').pack()

tk.Label(master=header, text='C L A S S I F I E R',
         font=('Helvetica', 16),
         fg='#ff003c', bg='#0d0d0d').pack()

tk.Label(master=header, text='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
         fg='#ff003c', bg='#0d0d0d').pack(pady=8)

tk.Label(master=header, text='A r e   y o u   w a l k i n g   o r   j u m p i n g ?',
         font=('Helvetica', 9),
         fg='white', bg='#0d0d0d').pack()

#═══════════════════════════════════════
#  CARD
#═══════════════════════════════════════
card_border = tk.Frame(master=window, bg='#ff003c', padx=2, pady=2)
card_border.pack(pady=10, padx=40, fill='x')

card = tk.Frame(master=card_border, bg='#111111', padx=30, pady=15)
card.pack(fill='x')

tk.Label(master=card, text='▸  INPUT',
         font=('Helvetica', 9, 'bold'),
         fg='#ff003c', bg='#111111').pack(anchor='w')

tk.Frame(master=card, bg='#222222', height=1).pack(fill='x', pady=(4,14))

#File button
file_button = tk.Button(master=card, text='◈   BROWSE FILES',
                        font=('Helvetica', 12, 'bold'),
                        command=open_file,
                        bg='#1a1a1a', fg='#ff003c',
                        activebackground='#ff003c', activeforeground='#0d0d0d',
                        relief='flat', borderwidth=0,
                        padx=20, pady=12,
                        width=24,
                        cursor='hand2')
file_button.pack()

#File label
file_string = tk.StringVar()
file_label = tk.Label(master=card, font=('Helvetica', 7),
                      textvariable=file_string,
                      fg='white', bg='#111111',
                      wraplength=420)
file_label.pack(pady=8)

tk.Frame(master=card, bg='#222222', height=1).pack(fill='x', pady=(4,14))

tk.Label(master=card, text='▸  CLASSIFY',
         font=('Helvetica', 9, 'bold'),
         fg='#ff003c', bg='#111111').pack(anchor='w')

tk.Frame(master=card, bg='#222222', height=1).pack(fill='x', pady=(4,14))

#Check button
check_button = tk.Button(master=card, text='⚡   R U N   A N A L Y S I S   ⚡',
                         font=('Helvetica', 14, 'bold'),
                         command=check,
                         bg='#ff003c', fg='#0d0d0d',
                         activebackground='#cc0030', activeforeground='#0d0d0d',
                         relief='flat', borderwidth=0,
                         padx=20, pady=16,
                         width=24,
                         cursor='hand2')
check_button.pack()

#Clear button
clear_button = tk.Button(master=card, text='↺   C L E A R',
                         font=('Helvetica', 10, 'bold'),
                         command=clear,
                         bg='#1a1a1a', fg='#ff003c',
                         activebackground='#ff003c', activeforeground='#0d0d0d',
                         relief='flat', borderwidth=0,
                         padx=20, pady=8,
                         width=24,
                         cursor='hand2')
clear_button.pack(pady=6)

#═══════════════════════════════════════
#  OUTPUT
#═══════════════════════════════════════
output_frame = tk.Frame(master=window, bg='#0d0d0d')
output_frame.pack(pady=5)

tk.Label(master=output_frame, text='━━━━━━  OUTPUT  ━━━━━━',
         font=('Helvetica', 9),
         fg='#333333', bg='#0d0d0d').pack()

answer_string = tk.StringVar()
answer_string.set('_ _ _')
answer_label = tk.Label(master=output_frame,
                        font=('Helvetica', 42, 'bold'),
                        textvariable=answer_string,
                        fg='#ffffff', bg='#0d0d0d')
answer_label.pack(pady=8)

tk.Label(master=output_frame, text='▲  PREDICTION',
         font=('Helvetica', 8),
         fg='#ff003c', bg='#0d0d0d').pack()

#### PLOT
plot_frame = tk.Frame(master=window, bg='#0d0d0d')
plot_frame.pack(fill='x', expand=True, padx = 20, pady=(0, 20))

#═══════════════════════════════════════
#  FOOTER
#═══════════════════════════════════════
tk.Label(master=window,
         text='━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
         fg='#ff003c', bg='#0d0d0d').pack(side='bottom', pady=(0,4))

tk.Label(master=window,
         text="ELEC 292  ·  Queen's University  ·  2025",
         font=('Helvetica', 7),
         fg='#333333', bg='#0d0d0d').pack(side='bottom')

#run
window.mainloop()

