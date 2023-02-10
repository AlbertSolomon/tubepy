import tkinter
import customtkinter as ctk
from app import audio_download
from settings import download_path_settings
from lang import error_message, event_color, app_color, file_verification

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
# ctk.set_widget_scaling(1.0)  # widget dimensions and text size
# ctk.set_window_scaling(0.9)  # window geometry dimensions 

app = ctk.CTk()
app.geometry("840x640")
app.title("Tubepy")

# #009999 is a placeholder color for the app
entry = ctk.CTkEntry(master=app, border_color=app_color.get("primary"), text_color=app_color.get("primary"), 
                     placeholder_text="Enter Youtube URL here", width=500, height=50, border_width=2, corner_radius=50)
entry.pack(padx=20, pady=30)
    
def event_label(app, message, color):
    text_var = tkinter.StringVar(value= message)
    label = ctk.CTkLabel(master=app, textvariable=text_var, width=500, height=25, text_color= color, corner_radius= 0)
    label.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)
    #label.pack(padx=10, pady=5, ipadx=8, ipady=5 ,side=tkinter.TOP)
    #label.pack(padx=10, pady=0)

def button_event():
    url = entry.get()   
    event_label(app, "", event_color.get("dark"))
    if len(url) >= 20 and len(url) <= 2048:
        
        print(url)
        print(len(url))
    else:
       event_label(app, error_message.get("invalid_length"), event_color.get("danger")) 
    
button = ctk.CTkButton(master=app, text="Download", command=button_event, width=150, height=50, border_width=0,text_color= app_color.get("extra_color"), 
                       corner_radius=50, hover_color=app_color.get("hover_color"), fg_color=app_color.get("primary"), font=("", 16))
#button.place(relx=0.5, rely=0.28, anchor=tkinter.CENTER)
button.pack(padx=10, pady=5)

# progress bar
progressbar = ctk.CTkProgressBar(master=app, width=320, height=25, corner_radius=50,
                                 progress_color=app_color.get("primary"))
progressbar.pack(padx=20, pady=10, side=tkinter.BOTTOM)
# progressbar.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
progressbar.set(0)
progressbar.start()

#progress label
label_text = tkinter.StringVar(value="0%")
label = ctk.CTkLabel(master=app, textvariable=label_text, width=25, height=25, corner_radius=50, 
                     text_color=app_color.get("primary"), font=("", 16))
# label.place(relx=0.5, rely=0.94, anchor=tkinter.CENTER)
label.pack(side=tkinter.BOTTOM)

# switch button
def switch_event():
    print("switch toggled, current value:", switch_var.get())

switch_var = ctk.StringVar(value="on")
switch_1 = ctk.CTkSwitch(master=app, button_color=app_color.get("primary"), button_hover_color=app_color.get("hover_color"), 
                        progress_color=app_color.get("primary"),text="Quick Download", command=switch_event,variable=switch_var, 
                        onvalue="on", offvalue="off")
switch_1.pack(padx=0, pady=10, side=tkinter.TOP)

# Combo box
def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

combobox_var = ctk.StringVar(value="option 2")  # set initial value
combobox = ctk.CTkComboBox(master=app, button_color=app_color.get("hover_color"),
                                     values=["option 1", "option 2", "option 3", "option 4"],
                                     command=combobox_callback,
                                     variable=combobox_var)
combobox.pack(padx=40, pady=10, side=tkinter.TOP)

if __name__ == "__main__":
    app.mainloop()