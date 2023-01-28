import tkinter
import customtkinter as ctk
from app import audio_download
from settings import download_path_settings

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green") 

app = ctk.CTk()
app.geometry("840x640")

app.mainloop()