import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#Allows user to choose file from computer, executed when "File" button is pushed
def open_file():
    #Opens file browser so that user can pick csv file
    filename = filedialog.askopenfilename()

    #Check if .csv file was selected
    if not filename.endswith('.csv'):
        print('Please select a .csv file')
        return

#Runs the check for whether file contains walking or jumping info, executed when 'Check' button is pushed
def check ():
    if run_or_jump(filename) == 'walking':
        print('Walking!!!!!')
    else:
        print('Jumping!!!!!')




#window
window = tk.Tk()
window.title('ELEC292 Final Project')
window.geometry('500x500')

#title
title_label = ttk.Label(master=window, text='Walking or Jumping???', font=('Times New Roman bold', 24))
title_label.pack()

#input field
input_frame = ttk.Frame(master=window)
file_button = ttk.Button(master = input_frame, text = 'File', command = open_file)
check_button = ttk.Button(master = input_frame, text = 'Check', command = check)
file_button.pack(padx = 10)
check_button.pack(padx = 10)
check_button.pack()
input_frame.pack(pady = 10)

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