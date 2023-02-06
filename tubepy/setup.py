import tkinter
import customtkinter as ctk
from app import audio_download
from settings import download_path_settings
from lang import error_message, event_color, app_color

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
# ctk.set_widget_scaling(float_value)  # widget dimensions and text size
# ctk.set_window_scaling(float_value)  # window geometry dimensions 

app = ctk.CTk()
app.geometry("840x640")
app.title("Tubepy")

# #009999 is a placeholder color for the app
entry = ctk.CTkEntry(master=app, border_color=app_color.get("primary"), text_color=app_color.get("text_color"), placeholder_text="Enter Youtube URL here", width=500, height=50, border_width=2, corner_radius=50)
entry.place(relx=0.5, rely=0.125, anchor=tkinter.CENTER)

def event_label(app, message, color):
    text_var = tkinter.StringVar(value= message)
    label = ctk.CTkLabel(master=app, textvariable=text_var, width=500, height=25, text_color= color, corner_radius= 0)
    label.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

def button_event():
    url = entry.get()   
    event_label(app, "", event_color.get("dark"))
    if len(url) >= 20 and len(url) <= 2048:
        
        print(url)
        print(len(url))
    else:
       event_label(app, error_message.get("invalid_length"), event_color.get("danger")) 
    
button = ctk.CTkButton(master=app, text="Download", command=button_event, width=150, height=50, border_width=0,text_color= app_color.get("text_color"), 
                       corner_radius=50, hover_color=event_color.get("danger"), fg_color=app_color.get("primary"), font=("", 16))
button.place(relx=0.5, rely=0.28, anchor=tkinter.CENTER)

# progress bar
progressbar = ctk.CTkProgressBar(master=app, width=250, height=25, corner_radius=50, progress_color=app_color.get("primary"))
progressbar.pack(padx=20, pady=10)
progressbar.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

#progress label
label_text = tkinter.StringVar(value="50%")
label = ctk.CTkLabel(master=app, textvariable=label_text, width=25, height=25, corner_radius=50, text_color=app_color.get("text_color"), font=("", 16))
label.place(relx=0.7, rely=0.9, anchor=tkinter.CENTER)

app.mainloop()