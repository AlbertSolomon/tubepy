import asyncio
import importlib
import linecache
import os
import sys
import threading
import tkinter
import traceback

import customtkinter as ctk
from app import audio_download, quick_download
from lang import (
    CodeChangeHandler,
    app_color,
    error_message,
    event_color,
    file_verification,
    widget_state,
)
from PIL import Image
from settings import download_path_settings
from watchdog.observers import Observer


def displayUI():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.geometry("840x640")
    app.title("Tubepy")

    def event_label(app, message, color):
        text_var = tkinter.StringVar(value=message)
        label = ctk.CTkLabel(
            master=app,
            textvariable=text_var,
            width=500,
            height=25,
            text_color=color,
            corner_radius=0,
        )
        label.place(relx=0.5, rely=0.02, anchor=tkinter.CENTER)
        # label.pack(padx=10, pady=5, ipadx=8, ipady=5 ,side=tkinter.TOP)
        # label.pack(padx=10, pady=0)

    # right click context menu logic
    def do_popup(event, frame):
        try:
            frame.tk_popup(event.x_root, event.y_root)
        finally:
            frame.grab_release()
            

    def on_progress(stream, chunk, bytes_remaining):
        youtube_filesize = stream.filesize
        print(f"youtube file size : { youtube_filesize }")

        downloaded_chunk = youtube_filesize - bytes_remaining
        print(f"downloaded chunk size : { downloaded_chunk }")

        progress_label.pack(padx=20, pady=(5, 10), side=tkinter.BOTTOM)
        progressbar.pack(padx=20, pady=(5, 5), side=tkinter.BOTTOM)

        if bytes_remaining > 0:
            download_percentage = downloaded_chunk / youtube_filesize * 100
            print(f"download percentage : { download_percentage }")
            completion_percentage = str(int(download_percentage))

            progress_label.configure(text=completion_percentage + " %")
            progress_label.update()

            # progress bar
            progressbar.set(float(download_percentage) / 100)
            print(float(download_percentage) / 100)
        else:
            print("Download complete!")
            progressbar.set(1)
            progress_label.configure(text="100 %")

        # download_percentage = downloaded_chunk / youtube_filesize * 100
        # print(f"download percentage : { download_percentage }")

    # button event handler
    def button_event():
        url = entry.get()
        event_label(app, "", event_color.get("dark"))
        color = event_color.get("danger")

        if len(url) >= 20 and len(url) <= 2048:
            file_Availability = asyncio.run(file_verification(url))
            switch = switch_event()
            radiobutton_value = radiobutton_event()

            if file_Availability:
                if switch == "on":

                    print("Quick download")

                    download_thread = threading.Thread(
                        target=quick_download, args=(url, on_progress)
                    )
                    download_thread.start()

                elif radiobutton_value == "video":
                    print("Download video")
                else:
                    print("Download audio")
            else:
                error = error_message.get("url_issue")
                event_label(app, error, color)

        else:
            error = error_message.get("invalid_length")
            event_label(app, error, color)

        entry.delete(0, ctk.END)

    # switch button event handler
    state: list = ["disabled"]

    def switch_event() -> str:
        switch = switch_var.get()
        disabled = widget_state[0]
        normal = widget_state[1]

        if switch == "on":
            # disabling the combobox
            state[0] = disabled
            combobox.configure(state=state[0])

            # disabling the radio button
            state[0] = disabled
            radiobutton_1.configure(state=state[0])
            radiobutton_2.configure(state=state[0])
        else:
            state[0] = normal
            combobox.configure(state=state[0])

            state[0] = normal
            radiobutton_1.configure(state=state[0])
            radiobutton_2.configure(state=state[0])

        return switch

    # radio buttons event handler
    def radiobutton_event() -> str:
        radio_value = radio_var.get()
        print(f"you selected { radio_value }")
        return radio_value

    # Combo box event handler
    def combobox_callback(choice) -> str:
        print("combobox dropdown clicked:", choice)
        return choice

    #! UI COMPONENTS ----------------------------------------------------------------------------------------------------------------------

    # entry button
    entry = ctk.CTkEntry(
        master=app,
        border_color=app_color.get("primary"),
        text_color=app_color.get("primary"),
        placeholder_text="Enter Youtube URL here",
        width=500,
        height=50,
        border_width=2,
        corner_radius=50,
    )
    entry.pack(padx=20, pady=30)

    # swich button
    switch_var = ctk.StringVar(value="on")
    switch_1 = ctk.CTkSwitch(
        master=app,
        button_color=app_color.get("primary"),
        button_hover_color=app_color.get("hover_color"),
        progress_color=app_color.get("primary"),
        text="Quick Download",
        command=switch_event,
        variable=switch_var,
        onvalue="on",
        offvalue="off",
    )
    switch_1.pack(padx=0, pady=5, side=tkinter.TOP)

    # radio button
    radio_var = tkinter.StringVar(value="video")
    radiobutton_1 = ctk.CTkRadioButton(
        master=app,
        height=20,
        radiobutton_width=20,
        radiobutton_height=20,
        fg_color=app_color.get("primary"),
        hover_color=app_color.get("hover_color"),
        text="Video",
        command=radiobutton_event,
        variable=radio_var,
        value="video",
        state=state[0],
    )

    radiobutton_2 = ctk.CTkRadioButton(
        master=app,
        height=20,
        radiobutton_width=20,
        radiobutton_height=20,
        fg_color=app_color.get("primary"),
        hover_color=app_color.get("hover_color"),
        text="Audio",
        command=radiobutton_event,
        variable=radio_var,
        value="audio",
        state=state[0],
    )
    radiobutton_1.pack(padx=10, pady=5)
    radiobutton_2.pack(padx=10, pady=5)

    # combo box
    combobox_var = ctk.StringVar(value="option 1")  # set initial value
    combobox = ctk.CTkComboBox(
        master=app,
        button_color=app_color.get("hover_color"),
        # vaules will take in a a list of streams
        values=["option 1", "option 2", "option 3", "option 4"],
        state=state[0],
        command=combobox_callback,
        variable=combobox_var,
    )
    combobox.pack(padx=40, pady=10, side=tkinter.TOP)

    # download button
    button = ctk.CTkButton(
        master=app,
        text="Download",
        command=button_event,
        width=150,
        height=50,
        border_width=0,
        text_color=app_color.get("extra_color"),
        corner_radius=50,
        hover_color=app_color.get("hover_color"),
        fg_color=app_color.get("primary"),
        font=("", 16),
    )
    button.pack(padx=10, pady=20)

    # progress bar
    progressbar = ctk.CTkProgressBar(
        master=app,
        width=400,
        height=20,
        corner_radius=50,
        progress_color=app_color.get("primary"),
    )

    progressbar.set(0)
    progressbar.pack_forget()

    # progress label
    progress_label = ctk.CTkLabel(
        master=app,
        width=25,
        height=25,
        corner_radius=50,
        text_color=app_color.get("primary"),
        text="",
        font=("", 16),
    )
    progress_label.pack_forget()

    RightClickMenu = tkinter.Menu(
        entry, tearoff=False,activebackground=app_color.get("primary") ,background="#565b5e", fg=app_color.get("primary"), borderwidth=0, bd=0, 
    )
    RightClickMenu.add_command(
        label="Paste", command=lambda: entry.insert(tkinter.END, app.clipboard_get())
    )
    RightClickMenu.add_command(
        label="Copy", command=lambda: app.clipboard_append(entry.get())
    )

    entry.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu))
    app.bind("<1>", lambda event: event.widget.focus_set())

    app.mainloop()


if __name__ == "__main__":

    event_handler = CodeChangeHandler(
        lambda: os.execv(sys.executable, ["python"] + sys.argv)
    )
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        displayUI()
    except Exception as e:

        traceback.print_exc()
        tb = e.__traceback__
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno

        print("Error occurred at line:", lineno)
        for i in range(lineno - 2, lineno + 3):
            line = linecache.getline(filename, i)
            print(f"{i:4d} {line.strip()}")

    observer.stop()
    observer.join()
