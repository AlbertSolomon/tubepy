import asyncio
import importlib
import linecache
import os
import sys
import threading
import time
import tkinter
import traceback
import urllib.parse

import customtkinter as ctk
import requests
from app import audio_download, download, quick_download
from lang import (
    CodeChangeHandler,
    add_audio_stream_codes,
    add_video_stream_code,
    app_color,
    app_info,
    check_internet_connection,
    connection_checker,
    downloadfile_details,
    downloadstatus,
    error_message,
    event_color,
    file_verification,
    playlist_details,
    widget_state,
)
from PIL import Image
from settings import download_path_settings
from watchdog.observers import Observer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("840x640")
app.title("Tubepy")
app.resizable(width=False, height=False)

if sys.platform.startswith("linux"):
    app.iconbitmap("@assets/icons/new_tubepy_logo128.xbm")

elif sys.platform.startswith("win"):
    app.iconbitmap("assets/icons/new_tubepy_logo128.ico")

# Mac OS implementation here

audio_itags: list = []
audio_abrs: list = []
audio_dict: dict = {}

video_itags: list = []
video_resolutions: list = []
video_dict: dict = {}

download_inprogress: bool = False


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


def displayUI(page_state: list = None):
    # right click context menu logic
    def do_popup(event, frame):
        try:
            frame.tk_popup(event.x_root, event.y_root)
        finally:
            frame.grab_release()

    def display_fileinfo(youtube_url):
        stringified_details = ""

        def youtube_file_information(stringified_details, file_details):
            for key, file_detail in file_details.items():
                if key == "thumbnail":
                    thumbnail_image.configure(
                        dark_image=Image.open(
                            requests.get(file_detail, stream=True).raw
                        )
                    )
                else:
                    stringified_details += f"{ key.capitalize() }: { file_detail } \n\n"
            infobox.configure(text=stringified_details)

        if "playlist" in youtube_url:
            playlist_information = asyncio.run(playlist_details(youtube_url))
            youtube_file_information(stringified_details, playlist_information)
        else:
            file_details = asyncio.run(downloadfile_details(youtube_url))
            youtube_file_information(stringified_details, file_details)

    def on_progress(stream, chunk, bytes_remaining):
        global download_inprogress
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
            download_inprogress = True
        else:
            download_inprogress = False
            global audio_abrs, video_resolutions
            print("Download complete!")

            progressbar.set(1)
            progress_label.configure(text="100 %")
            event_label(app, downloadstatus.get("successful"), app_color.get("primary"))

            entry.delete(0, ctk.END)
            audio_abrs.clear()
            video_resolutions.clear()

            time.sleep(5)
            progressbar.pack_forget()
            progress_label.pack_forget()

    class PlaylistDownloadProgress:
        """Displays playlist download progress information to the UI

        Initializes the instance of the class.
        Sets the standard output and error streams to be the instance of the class itself.

        This method is called whenever the CLI program prints something to the standard output or error streams.
        Captures the message and checks if it contains any information related to the playlist download progress.
        If it does, it uses the event_label() method to display the message to the user in a user-friendly way.
        If there is an exception during this process, the method displays an error message in red to indicate an error has occurred.

        Args:
            message (str): A string containing the message printed to the standard output or error streams by the CLI program.
        """

        def __init__(self):
            sys.stdout = self
            sys.stderr = self

        def write(self, message):
            try:
                if "Downloading video" in message:
                    event_label(app, message, app_color.get("primary"))
                if "!" in message:
                    event_label(app, message, app_color.get("primary"))
            except Exception:
                event_label(
                    app, error_message.get("playlist_error"), event_color.get("danger")
                )

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
            global audio_abrs, video_resolutions
            url = entry.get()

            state[0] = normal
            combobox.configure(state=state[0])

            state[0] = normal
            radiobutton_1.configure(state=state[0])
            radiobutton_2.configure(state=state[0])

            def load_formats(url):
                if len(audio_abrs) == 0:
                    event_label(
                        app, downloadstatus.get("loadstreams"), app_color.get("primary")
                    )

                    try:

                        def add_audiostreams(url):
                            global audio_abrs, audio_itags, audio_dict

                            audio_streams = asyncio.run(add_audio_stream_codes(url))
                            audio_abrs = audio_streams[0]
                            audio_itags = audio_streams[1]

                            audio_dict = {
                                audio_abrs: audio_itags
                                for (audio_abrs, audio_itags) in zip(
                                    audio_abrs, audio_itags
                                )
                            }

                            # combobox.configure(values=audio_abrs)
                            event_label(
                                app,
                                downloadstatus.get("stream_load_success"),
                                app_color.get("primary"),
                            )

                        stream_thread = threading.Thread(
                            target=add_audiostreams, args=(url,)
                        )
                        stream_thread.start()

                    except:
                        event_label(
                            app,
                            error_message.get("url_issue"),
                            event_color.get("danger"),
                        )
                else:
                    event_label(app, "", event_color.get("dark"))

                if len(video_resolutions) == 0:
                    event_label(
                        app,
                        downloadstatus.get("loadvideostreams"),
                        app_color.get("primary"),
                    )
                    try:

                        def add_video_resolutions(url):
                            global video_resolutions, video_itags, video_dict

                            video_streams = asyncio.run(add_video_stream_code(url))
                            video_resolutions = video_streams[0]
                            video_itags = video_streams[1]

                            video_dict = {
                                video_resolutions: video_itags
                                for (video_resolutions, video_itags) in zip(
                                    video_resolutions, video_itags
                                )
                            }
                            combobox.configure(values=video_resolutions)
                            event_label(
                                app,
                                downloadstatus.get("vstream_load_success"),
                                app_color.get("primary"),
                            )

                        _stream_thread = threading.Thread(
                            target=add_video_resolutions, args=(url,)
                        )
                        _stream_thread.start()

                    except:
                        event_label(
                            app,
                            error_message.get("url_issue"),
                            event_color.get("danger"),
                        )
                else:
                    event_label(app, "", event_color.get("dark"))

            if len(url) >= 20 and len(url) <= 2048:
                event_label(
                    app, downloadstatus.get("check_network"), app_color.get("primary")
                )

                async def verify_formats():
                    network_check = await check_internet_connection(url)
                    file_Availability = await file_verification(url)

                    if not network_check:
                        event_label(
                            app,
                            error_message.get("network_error"),
                            event_color.get("danger"),
                        )
                        return

                    if not file_Availability:
                        event_label(
                            app,
                            error_message.get("url_issue"),
                            event_color.get("danger"),
                        )
                        return

                    verifying_thread = threading.Thread(
                        target=load_formats, args=(url,)
                    )
                    verifying_thread.start()

                # verifying_thread = threading.Thread(target=verify_formats)
                # verifying_thread.start()

                def finalizing_verification():
                    asyncio.run(verify_formats())

                finalizing_thread = threading.Thread(target=finalizing_verification)
                finalizing_thread.start()

        return switch

    # radio buttons event handler
    def radiobutton_event() -> str:
        global audio_abrs, video_resolutions
        radio_value = radio_var.get()

        # print(f"you selected { radio_value }")

        if radio_value == "audio":
            combobox.configure(values=audio_abrs)
            combobox.update()
        else:
            combobox.configure(values=video_resolutions)
            combobox.update()
            print(video_resolutions)

        if not audio_abrs and not video_resolutions:
            empty_message: list = [error_message.get("unavailable_options")]
            combobox.configure(values=empty_message)
            return

        # if radio_value == "audio":
        return radio_value

    # Combo box event handler
    def combobox_callback(choice) -> str:
        return choice

    # Button event handler
    def button_event():
        url = entry.get()
        event_label(app, "", event_color.get("dark"))
        color = event_color.get("danger")

        if len(url) >= 20 and len(url) <= 2048:
            file_Availability = asyncio.run(file_verification(url))
            switch = switch_event()
            radiobutton_value = radiobutton_event()

            if file_Availability:
                info_thread = threading.Thread(target=display_fileinfo, args=(url,))
                info_thread.start()

                if switch == "on":
                    event_label(
                        app, downloadstatus.get("download"), app_color.get("primary")
                    )

                    download_thread = threading.Thread(
                        target=quick_download, args=(url, on_progress)
                    )
                    download_thread.start()

                elif radiobutton_value == "video":
                    global video_resolutions, video_dict

                    event_label(
                        app,
                        downloadstatus.get("videodownload"),
                        app_color.get("primary"),
                    )
                    if combobox.get() in video_resolutions:
                        itag = video_dict.get(combobox.get())
                        download_thread = threading.Thread(
                            target=download, args=(url, on_progress, itag)
                        )
                        download_thread.start()
                    else:
                        event_label(
                            app,
                            error_message.get("option_issue"),
                            event_color.get("danger"),
                        )

                else:
                    global audio_abrs, audio_dict
                    event_label(
                        app,
                        downloadstatus.get("audiodownload"),
                        app_color.get("primary"),
                    )
                    if combobox.get() in audio_abrs:
                        itag = audio_dict.get(combobox.get())
                        download_thread = threading.Thread(
                            target=audio_download, args=(url, on_progress, itag)
                        )
                        download_thread.start()
                    else:
                        event_label(
                            app,
                            error_message.get("option_issue"),
                            event_color.get("danger"),
                        )

            else:
                error = error_message.get("url_issue")
                event_label(app, error, color)

        else:
            error = error_message.get("invalid_length")
            event_label(app, error, color)

        if "playlist" in url:
            PlaylistDownloadProgress()

    def segmented_button_callback(value):
        if value == "Change download Location":
            # download_path_settings()
            settings_thread = threading.Thread(target=download_path_settings)
            settings_thread.start()
            return

        if value == "About":
            nextpage()
            return

    #! *****************************************************************************************************************************************************************************************************************************************
    #! *****************************************************************************************************************************************************************************************************************************************

    # ?                                                                                                    HOME PAGE UI COMPONENTS 🌳

    #! *****************************************************************************************************************************************************************************************************************************************
    #! *****************************************************************************************************************************************************************************************************************************************

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
    entry.pack(padx=20, pady=(30, 15))

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
    combobox_var = ctk.StringVar(value="select 👇🏾")  # set initial value
    combobox = ctk.CTkComboBox(
        master=app,
        button_color=app_color.get("hover_color"),
        state=state[0],
        command=combobox_callback,
        variable=combobox_var,
    )
    combobox.pack(padx=40, pady=10, side=tkinter.TOP)

    download_icon = ctk.CTkImage(
        # dark_image=Image.open(requests.get("https://previews.123rf.com/images/morphart/morphart2008/morphart200804535/152569857-cute-apple-pie-illustration-vector-on-white-background.jpg", stream=True).raw),  # "assets/TUBEPY LOGO SKETCH small.png"
        dark_image=Image.open("assets/icons/cloud-download.png"),
        size=(
            18,
            19,
        ),
    )

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
        image=download_icon,
        compound="right",
    )
    button.pack(padx=10, pady=(10, 5))

    frame = ctk.CTkFrame(master=app, width=500, height=200)
    frame.pack(padx=5, pady=(10, 5))

    thumbnail_image = ctk.CTkImage(
        # dark_image=Image.open(requests.get("https://previews.123rf.com/images/morphart/morphart2008/morphart200804535/152569857-cute-apple-pie-illustration-vector-on-white-background.jpg", stream=True).raw),  # "assets/TUBEPY LOGO SKETCH small.png"
        dark_image=Image.open("assets/new_tubepy_logo.png"),
        size=(
            160,
            155,
        ),
    )

    image_label = ctk.CTkLabel(
        master=frame,
        width=50,
        height=150,
        corner_radius=10,
        text="",
        image=thumbnail_image,
    )
    image_label.grid(row=0, column=0, padx=0, pady=0)

    infobox = ctk.CTkLabel(
        master=frame,
        width=400,
        height=150,
        # text_color=app_color.get("primary"),
        text=app_info.get("general_summary"),
        anchor="nw",
        justify="left",
        wraplength=490,
    )
    infobox.grid(row=0, column=1, padx=10, pady=(15, 0))

    tiny_frame = ctk.CTkFrame(master=app, width=500, height=50)
    tiny_frame.pack(padx=0, pady=(5, 5))

    segemented_button = ctk.CTkSegmentedButton(
        master=tiny_frame,
        height=20,
        selected_color=app_color.get("extra_color"),
        text_color=app_color.get("primary"),
        values=["Change download Location", "About"],
        command=segmented_button_callback,
    )
    segemented_button.grid(row=1, column=1, padx=0, pady=(0, 5))

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
        entry,
        tearoff=False,
        activebackground=app_color.get("primary"),
        background="#565b5e",
        fg=app_color.get("primary"),
        borderwidth=0,
        bd=0,
    )

    RightClickMenu.add_command(
        label="Paste", command=lambda: entry.insert(tkinter.END, app.clipboard_get())
    )

    RightClickMenu.add_command(
        label="Copy", command=lambda: app.clipboard_append(entry.get())
    )

    entry.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu))
    entry.bind("<1>", lambda event: event.widget.focus_set())


#! *****************************************************************************************************************************************************************************************************************************************
#! *****************************************************************************************************************************************************************************************************************************************

# ?                                                                                                   ABOUT PAGE SECTION 📃

#! *****************************************************************************************************************************************************************************************************************************************
#! *****************************************************************************************************************************************************************************************************************************************


def aboutTubepy(app):
    page = ctk.CTkFrame(master=app, width=400, corner_radius=25)
    page.pack(pady=10)

    heading_label = ctk.CTkLabel(master=page, text="ABOUT TUBEPY ", justify="center")
    heading_label.grid(row=0, column=1, padx=[200, 350], pady=10, ipadx=0)

    back_image_icon = ctk.CTkImage(
        dark_image=Image.open(
            "assets/icons/left-arrow.png"
        ),  # <a href="https://www.flaticon.com/free-icons/back" title="back icons">Back icons created by Roundicons - Flaticon</a>
        size=(
            10,
            10,
        ),
    )

    back_btn = ctk.CTkButton(
        master=page,
        width=80,
        height=40,
        border_width=0,
        text_color=app_color.get("extra_color"),
        corner_radius=50,
        hover_color=app_color.get("hover_color"),
        fg_color=app_color.get("primary"),
        text="Back",
        command=nextpage,
        image=back_image_icon,
    )
    back_btn.grid(row=0, column=0, padx=15, pady=10)

    tubepy_infoLabel = ctk.CTkLabel(
        master=app,
        text=app_info.get("about_app"),
        anchor="nw",
        justify="left",
        wraplength=510,
    )
    tubepy_infoLabel.pack(pady=20)

    QRCODE_image = ctk.CTkImage(
        dark_image=Image.open(
            "assets/qr-code.png"
        ),  # from https://www.qrcode-monkey.com/
        size=(
            160,
            150,
        ),
    )

    QRCODE_label = ctk.CTkLabel(
        master=app,
        width=50,
        height=150,
        corner_radius=10,
        text="",
        image=QRCODE_image,
    )
    QRCODE_label.pack(padx=0, pady=10)


def nextpage():
    global page_number, app, download_inprogress

    for widget in app.winfo_children():
        # widget.destroy()
        event_label(
            app, "", event_color.get("dark")
        )  # show downloading when there is a download in progress
        widget.forget()

    if page_number == 1:
        aboutTubepy(app)
        page_number = 2
    else:
        if download_inprogress:
            event_label(app, downloadstatus.get("download"), app_color.get("primary"))

        displayUI()
        page_number = 1


page_number = 1


if __name__ == "__main__":
    exclude_dir = "../utilities"
    exclude_file = "../utilities/config.json"

    event_handler = CodeChangeHandler(
        lambda: os.execv(sys.executable, ["python"] + sys.argv),
        exclude_dir=exclude_dir,
        exclude_file=exclude_file,
    )

    observer = Observer()
    observer.schedule(event_handler, "./tubepy", recursive=True)
    observer.start()

    try:
        displayUI()
        app.mainloop()
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
