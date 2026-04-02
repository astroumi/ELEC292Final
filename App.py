import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import joblib
import numpy as np
import pandas as pd

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

        #Split the data into 5 second windows
        windows = split_csv_in_memory(selected_filename)

        #Extract features
        all_features = []
        for window_data in windows:
            features = extract_features(window_data.values)
            all_features.append(features)

        #Normalize the data
        features_scaled = scaler.transform(np.array(all_features))

        #Check
        prediction = model.predict(features_scaled)

        #Count results
        walking_count = sum(prediction == 0)
        jumping_count = sum(prediction == 1)

        if walking_count > jumping_count:
            answer_string.set("walking!!!")
        else:
            answer_string.set("jumping!!!")
    except Exception as e:
        print(f"Something went wrong: {e}")
        answer_string.set("Error - check console")
    return None



#Window
window = tk.Tk()
window.title('ELEC292 Final Project')
window.geometry('500x500')
window.configure(bg = 'lightblue')

#Title
title_label = tk.Label(master=window, text='Walking or Jumping???', font=('Times New Roman bold', 24), fg = 'gray', bg='lightblue')
title_label.pack()

#Input field
input_frame = tk.Frame(master=window, bg = 'lightblue', bd=0, highlightthickness = 0)
file_button = tk.Button(master = input_frame, text = 'File', command = open_file, highlightthickness = 0, borderwidth = 1)
check_button = tk.Button(master = input_frame, text = 'Check', command = check, highlightthickness = 0, borderwidth = 1)
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







def convert ():
    mile_input = entry_Int.get()
    km_output = mile_input * 1.60934
    output_string.set(km_output)


#window
window = tk.Tk()
window.title('Demo')
window.geometry('300x150')

#title
title_label = ttk.Label(master=window, text='Miles to kilometers', font=('Times New Roman bold', 24))
#places label on the window
title_label.pack()

#input field
input_frame = ttk.Frame(master=window)
entry_Int = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable=entry_Int)
button = ttk.Button(master = input_frame, text = 'Convert', command = convert)
entry.pack(side = 'left', padx = 10)
button.pack(side = 'left')
input_frame.pack(pady = 10)

#output
output_string = tk.StringVar()
output_label = ttk.Label(master=window,
                         text = 'Output',
                         font=('Times New Roman', 24),
                         textvariable = output_string)
output_label.pack()

button.pack()
input_frame.pack()

#run
window.mainloop()