from app import download, change_download_location
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fdlog


custon_settings:str = ''
# this input variable will be used for testing purposes
def test_url_input():
    url_input = "Enter Youtube Video URL here 👉🏾: " 
    return input(url_input)


test_input = test_url_input()
# download(test_input)

# Create an instance of tkinter window
win = tk.Tk()
win.geometry("700x350")

# Create an instance of style class
style=ttk.Style(win)

def open_dialog_box():
    filename = fdlog.askdirectory()
    custon_settings = filename
    change_download_location(custon_settings)
    
button=ttk.Button(win, text="Open", command=open_dialog_box)
button.pack(pady=5)

win.mainloop()

