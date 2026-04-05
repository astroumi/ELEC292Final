import tkinter as tk
from tkinter import filedialog
import joblib
import pandas as pd
from pathlib import Path

from hdf import model_path, features_path
from preprocessing import process_app
from extraction import extract_features, extract_mxyz
from split import split_df_in_memory
from visualization import plot_app_results_embedded

#Global Variables
selected_filename = ""
classifier_model = None

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
        print('INFO: Please select a .csv file')
    return None

#Runs the check for whether file contains walking or jumping info, executed when 'Check' button is pushed
def check ():
    global selected_filename
    #Check if a file was selected
    if not selected_filename:
        file_string.set("Select a .csv file")
        print('INFO: Please select a .csv file first')
        return None

    # Try to load the model from the appdata folder

    if not model_path.exists():
        answer_string.set("No Model Found")
        print("ERROR: 'trained_model.pkl' not found. Please train a model first!")
        return None

    #Use 'try' to gracefully handle errors
    try:
        classifier_model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        answer_string.set("Model Error")
        return None

    try:
        answer_string.set("Processing...")
        print(f"INFO: Processing {selected_filename}.")

        # Preprocess data
        processed_df = process_app(selected_filename)

        # Split df into 5s windows
        windows = split_df_in_memory(processed_df)

        # Check file length
        if len(windows) == 0:
            answer_string.set("Error: File < 5s")
            print("Error: CSV file must contain at least 5 seconds of data.")
            return None

        # Extract features with appropriate shape (based on extraction method)
        all_features = []
        if (features_path).exists():
            for window_data in windows:
                features = extract_features(window_data.values)
                all_features.append(features)
        else:
            print("ERROR: No feature extraction file found to determine mode.")
            return None

        # Predict using preloaded model
        predictions = classifier_model.predict(all_features)

        # Export results and plot in app
        save_results_to_csv(predictions)
        plot_app_results_embedded(selected_filename, predictions, plot_frame)
        answer_string.set("Analysis Complete:")

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

        #Save as  filename_predictions
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
        #Restricts file browser to only show CSV files so users can't save wrong format
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

def launch_app():
    # THIS FUNCTION CONFIGURES THE TKINTER APP WINDOW AND LAUNCHES IT

    global file_string, answer_string, plot_frame

    #Window
    window = tk.Tk()
    window.title('ELEC292 Final Project')
    window.geometry('1000x1000')
    window.configure(bg='#0d0d0d')
    window.resizable(True, True)

    # MAKES APP LAUNCH IN FOREGROUND
    window.lift()
    window.attributes('-topmost', True)
    window.after(50, lambda: window.attributes('-topmost', False))
    window.focus_force()

    # Nicely close and return to the terminal menu
    def on_closing():
        print("Closing application...")
        window.quit()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)


    #  HEADER
    header = tk.Frame(master=window, bg='#0d0d0d')
    header.pack(fill='x', pady=(30,0))

    tk.Label(master=header, text='MOTION CLASSIFIER',
             font=('Helvetica', 34, 'bold'),
             fg='#ff003c', bg='#0d0d0d').pack()

    tk.Label(master=header, text='ELEC292 Final Project',
             font=('Helvetica', 16),
             fg='#ff003c', bg='#0d0d0d').pack()

    tk.Label(master=header, text='------------------------------------------------------------',
             fg='#ff003c', bg='#0d0d0d').pack(pady=8)

    tk.Label(master=header, text='Are you walking or jumping?',
             font=('Helvetica', 16),
             fg='white', bg='#0d0d0d').pack()


    #  CARD
    card_border = tk.Frame(master=window, bg='#ff003c', padx=2, pady=2)
    card_border.pack(pady=10, padx=40, fill='x')

    card = tk.Frame(master=card_border, bg='#111111', padx=30, pady=15)
    card.pack(fill='x')

    #File button
    file_button = tk.Button(master=card, text='B R O W S E  F I L E S',
                            font=('Helvetica', 16, 'bold'),
                            command=open_file,
                            bg='#1a1a1a', fg='#0d0d0d',
                            activebackground='#ff003c', activeforeground='#0d0d0d',
                            relief='raised', borderwidth=0,
                            padx=20, pady=12,
                            width=24)
    file_button.pack()

    #File label
    file_string = tk.StringVar()
    file_label = tk.Label(master=card, font=('Helvetica', 14),
                          textvariable=file_string,
                          fg='white', bg='#111111',
                          wraplength=420)
    file_label.pack(pady=8)
    file_string.set('(File Path)')

    #Check button
    check_button = tk.Button(master=card, text='R U N   A N A L Y S I S',
                             font=('Helvetica', 20, 'bold'),
                             command=check,
                             bg='#ff003c', fg='#ff003c',
                             activebackground='#cc0030', activeforeground='#0d0d0d',
                             relief='flat', borderwidth=0,
                             padx=20, pady=16,
                             width=24)
    check_button.pack()

    #Clear button
    clear_button = tk.Button(master=card, text='C L E A R',
                             font=('Helvetica', 12, 'bold'),
                             command=clear,
                             bg='#1a1a1a', fg='#ff003c',
                             activebackground='#ff003c', activeforeground='#0d0d0d',
                             relief='flat', borderwidth=0,
                             padx=20, pady=8,
                             width=14)
    clear_button.pack(pady=6)



    #  OUTPUT

    output_frame = tk.Frame(master=window, bg='#0d0d0d')
    output_frame.pack(pady=5)

    # tk.Label(master=output_frame, text='=====  OUTPUT  =====',
    #          font=('Helvetica', 18),
    #          fg='#333333', bg='#0d0d0d').pack()


    answer_string = tk.StringVar()
    answer_string.set('Waiting for file...')
    answer_label = tk.Label(master=output_frame,
                            font=('Helvetica', 20, 'bold'),
                            textvariable=answer_string,
                            fg='#ffffff', bg='#0d0d0d')
    answer_label.pack(pady=8)


    #### PLOT
    plot_frame = tk.Frame(master=window, bg='#0d0d0d')
    plot_frame.pack(fill='x', expand=True, padx = 20, pady=(0, 20))

    # footer
    footer = tk.Frame(master=window, bg='#0d0d0d')
    footer.pack(side='bottom', fill='x', pady=10)

    tk.Label(master=footer, text='Made by Umair and Kipras',
             fg='#ff003c', bg='#0d0d0d').pack()

    window.mainloop()
