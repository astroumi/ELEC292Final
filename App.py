import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import joblib
import numpy as np
import pandas as pd

from visualization import plot_app_results

# from Extraction import extract_features
# from split import split_csv_in_memory

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

        #Split the data into 5 second windows make a windows list out of them
        windows = split_csv_in_memory(selected_filename)

        #Extract features
        all_features = []
        for window_data in windows:
            features = extract_features(window_data.values)
            all_features.append(features)

        #Normalize the data
        #Converts all_features into a 2D numpy array and normalizes every feature using fitted scaler
        features_scaled = scaler.transform(np.array(all_features))

        #Run the classifier on every window and add 0s or 1s to a predictions array
        predictions = model.predict(features_scaled)

        #Count results
        walking_count = sum(predictions == 0)
        jumping_count = sum(predictions == 1)

        if walking_count > jumping_count:
            answer_string.set("walking!!!")
        else:
            answer_string.set("jumping!!!")

        #Save results to CSV
        save_results_to_csv(predictions)

        #Plot results
        plot_app_results(selected_filename, predictions)

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

    #Convert list of dictionaries into a pandas dataframe
    output_df = pd.DataFrame(rows)
    #Allows user to choose where to save the file and what to name it
    output_path = filedialog.asksaveasfilename(
        #Automatically adds .csv to the file name if not added
        defaultextension='.csv',
        #Restricts the file browser to only show CSV files so users can't save it to the wrong format
        filetypes=[('CSV files', '*.csv')]
    )

    #Saves the dataframe to a csv in the output path
    if output_path:
        output_df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")





#Window
window = tk.Tk()
window.title('ELEC292 Final Project')
window.geometry('500x500')
window.configure(bg = 'lightblue')

#Title
title_label = tk.Label(master=window, text='Walking or Jumping???', font=('Times New Roman bold', 24), fg = 'purple', bg='lightblue')
title_label.pack()

#Input field
input_frame = tk.Frame(master=window, bg = 'lightblue', bd=0, highlightthickness = 0)
file_button = tk.Button(master = input_frame, text = 'File', font=('Times New Roman', 14), command = open_file, highlightthickness = 0, borderwidth = 1, width = 6, height = 1)
check_button = tk.Button(master = input_frame, text = 'Check', font=('Times New Roman', 18), command = check, highlightthickness = 0, borderwidth = 1, width = 10, height = 2)
file_button.pack(padx = 10, pady = 2)
check_button.pack(padx = 10, pady = 2)
check_button.pack()
input_frame.pack(pady = 10)

#File output
file_string = tk.StringVar()
file_label = tk.Label(master=window, font=('Times New Roman', 8), textvariable = file_string, bg='lightblue')
file_label.pack()
file_label.pack(pady = 20)

#Answer output
answer_string = tk.StringVar()
answer_label = tk.Label(master=window, font = ('Times New Roman', 20), textvariable = answer_string, bg='lightblue')
answer_label.pack(pady = 20)

#run
window.mainloop()

