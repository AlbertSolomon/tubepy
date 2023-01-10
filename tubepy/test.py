from app import download, change_download_location
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


custon_settings:str = ''
# this input variable will be used for testing purposes
def test_url_input():
    url_input = "Enter Youtube Video URL here 👉🏾: " 
    return input(url_input)
# 
def download_path():
    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askdirectory()
    change_download_location(filepath)

# download_path()