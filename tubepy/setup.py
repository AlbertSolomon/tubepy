import tkinter
import customtkinter as ctk
from app import audio_download
from settings import download_path_settings

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green") 

app = ctk.CTk()
app.geometry("840x640")
app.title("Tubepy")

# #009999 is a placeholder color for the app
entry = ctk.CTkEntry(master=app, border_color="#009999", text_color="#009999", placeholder_text="Enter Youtube URL here", width=500, height=50, border_width=2, corner_radius=50)
entry.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

url = entry.get()
def button_event():
    print(url)
    
button = ctk.CTkButton(master=app, text="Fetch", command=button_event, width=150, height=50, border_width=0, corner_radius=50)
button.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

app.mainloop()