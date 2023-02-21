import tkinter
import customtkinter as ctk
import os
import sys
import traceback
import linecache
import importlib
from watchdog.observers import Observer
from PIL import Image
from app import audio_download
from settings import download_path_settings
from lang import error_message, event_color, app_color, widget_state, CodeChangeHandler, file_verification


def displayUI():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green") 

    app = ctk.CTk()
    app.geometry("840x640")
    app.title("Tubepy")


    def event_label(app, message, color):
        text_var = tkinter.StringVar(value= message)
        label = ctk.CTkLabel(master=app, textvariable=text_var, width=500, height=25, text_color= color, corner_radius= 0)
        label.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)
        #label.pack(padx=10, pady=5, ipadx=8, ipady=5 ,side=tkinter.TOP)
        #label.pack(padx=10, pady=0)

    # button event handler
    def button_event():
        url = entry.get()   
        event_label(app, "", event_color.get("dark"))
        if len(url) >= 20 and len(url) <= 2048:
            
            print(url)
            print(len(url))
            
            print(switch_event())
            print( radiobutton_event() )
        else:
            event_label(app, error_message.get("invalid_length"), event_color.get("danger"))


    # switch button event handler
    state: list = ["disabled"]
    def switch_event() -> str:
        switch = switch_var.get()
        disabled = widget_state[0]
        normal = widget_state[1]
        
        if switch == "on":
            # disabling the combobox
            state[0] = disabled        
            combobox.configure(state= state[0])
            
            # disabling the radio button
            state[0] = disabled
            radiobutton_1.configure(state= state[0])
            radiobutton_2.configure(state= state[0])
        else:        
            state[0] = normal
            combobox.configure(state= state[0])
            
            state[0] = normal
            radiobutton_1.configure(state= state[0])
            radiobutton_2.configure(state= state[0])
        
        return switch


    # radio buttons event handler
    def radiobutton_event() -> str:
        radio_value = radio_var.get()
        print(f"you selected { radio_value }")
        return radio_value

   
    # Combo box event handler
    def combobox_callback(choice):
        print("combobox dropdown clicked:", choice)
   
   
    entry = ctk.CTkEntry(master=app, border_color=app_color.get("primary"), text_color=app_color.get("primary"), 
                        placeholder_text="Enter Youtube URL here", width=500, height=50, border_width=2, corner_radius=50)
    entry.pack(padx=20, pady=30)
        
        
    button = ctk.CTkButton(master=app, text="Download", command=button_event, width=150, height=50, border_width=0, text_color= app_color.get("extra_color"), 
                        corner_radius=50, hover_color=app_color.get("hover_color"), fg_color=app_color.get("primary"), font=("", 16))
    button.pack(padx=10, pady=5)


    switch_var = ctk.StringVar(value="on")
    switch_1 = ctk.CTkSwitch(master=app, button_color=app_color.get("primary"), button_hover_color=app_color.get("hover_color"), 
                            progress_color=app_color.get("primary"),text="Quick Download", command=switch_event,variable=switch_var, 
                            onvalue="on", offvalue="off")
    switch_1.pack(padx=0, pady=10, side=tkinter.TOP)


    radio_var = tkinter.StringVar(value="video")
    radiobutton_1 = ctk.CTkRadioButton(master=app, height=20, radiobutton_width=20, radiobutton_height=20, fg_color=app_color.get("primary"), hover_color= app_color.get("hover_color"), text="Video",
                                                command=radiobutton_event, variable= radio_var, value="video", state=state[0])
    radiobutton_2 = ctk.CTkRadioButton(master=app, height=20, radiobutton_width=20, radiobutton_height=20, fg_color=app_color.get("primary"), hover_color= app_color.get("hover_color"), text="Audio",
                                                command=radiobutton_event, variable= radio_var, value="audio", state=state[0])
    radiobutton_1.pack(padx=10, pady=5)
    radiobutton_2.pack(padx=10, pady=5)


    combobox_var = ctk.StringVar(value="option 1")  # set initial value
    combobox = ctk.CTkComboBox(master=app, button_color=app_color.get("hover_color"),
                                        # vaules will take in a a list of streams
                                        values=["option 1", "option 2", "option 3", "option 4"],
                                        state= state[0],
                                        command=combobox_callback,
                                        variable=combobox_var)
    combobox.pack(padx=40, pady=10, side=tkinter.TOP)


    # progress bar
    progressbar = ctk.CTkProgressBar(master=app, width=320, height=25, corner_radius=50,
                                    progress_color=app_color.get("primary"))
    progressbar.pack(padx=20, pady=10, side=tkinter.BOTTOM)
    progressbar.set(0)
    progressbar.start()


    #progress label
    label_text = tkinter.StringVar(value="0%")
    label = ctk.CTkLabel(master=app, textvariable=label_text, width=25, height=25, corner_radius=50, 
                        text_color=app_color.get("primary"), font=("", 16))
    label.pack(side=tkinter.BOTTOM)

    '''
    my_image = ctk.CTkImage(light_image=Image.open("c:/Users/solom/OneDrive/Documents/projects/tubepy/assets/wave.svg"),        
                                    dark_image=Image.open("c:/Users/solom/OneDrive/Documents/projects/tubepy/assets/wave.svg"),
                                    size=(30, 30)) '''

    app.mainloop()    


if __name__ == "__main__":
    event_handler = CodeChangeHandler(lambda: os.execv(sys.executable, ['python'] + sys.argv))
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    
    try:
        displayUI()
    except Exception as e:
        traceback.print_exc()
        tb = e.__traceback__
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno
        
        print("Error occurred at line:", lineno)
        for i in range(lineno-2, lineno+3):
            line = linecache.getline(filename, i)
            print(f"{i:4d} {line.strip()}")
    
    observer.stop()
    observer.join()