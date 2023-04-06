import asyncio
import concurrent.futures
import json
import re
import urllib.request

import aiohttp
import requests  # this for testing purposes
from humanize.time import precisedelta, naturaldelta
from pytube import YouTube
from watchdog.events import FileSystemEventHandler
from version import __version__

repo_link = "https://github.com/AlbertSolomon/tubepy"
app_info = {
    "general_summary": "Quick Download: is an option that downloads' YouTube videos at the highest available resolution (MP4) quickly.\n\n Video: is an option for custom resolution and Please *note that some of the resolutions do not have audio (Quick Download is recomended).\n\n Audio: is an option for downloading the audio version of the video.",
    "about_app": f"Tubepy is a simple open source desktop app developed by Albert Solomon Phiri that allows easy downloading of Youtube Videos.\n\nTubepy is currently at version { __version__ } and is licensed under the MIT license hence you can modify and redistribute the software under the conditions of this license.\n\n CONTRIBUTIONS: Tubepy is a project which is tailored for the developer who are just getting started contributing to open source, it has a lot of 'good first issues' on Github.\n\n CONTRIBUTORS: ALBERT SOLOMON PHIRI, treecake10 \n\n WANNA CONTRIBUTE ? : Interested contributors should follow this link to the repository { repo_link } or scan the QR CODE below, cant wait, happy coding and OOOH! dont forget to star ⭐ the project.\n\n LETS CODE TOGETHER !!!",
}

downloadstatus = {
    "load": "loading... 😒",
    "download": "downloading... 😒",
    "audiodownload": "downloading audio 🎶 ...",
    "videodownload": "downloading video 📽️ ... ",
    "loadvideostreams": "loading video resolutions ... 🎥",
    "loadstreams": "loading audio frequencies... 🎶",
    "vstream_load_success": "video resolutions were successfully loaded 🎥",
    "stream_load_success": "audio frequencies were successfully loaded 🎶",
    "successful": "download successful 🥳",
    "unsuccessful": "download failed... 💔",
    "check_network": "checking network connection...🌐",
}

empty = {
    "empty_location": " empty default location",
}

error_message = {
    "invalid_length": "Invalid url length !. The URL length you have provided is invalid. Please try again 😥",
    "videoUnavailable": "Sorry, the video is not available at the moment. 💔",
    "url_issue": "The url you have provided is not valid. Please verify it and try again. 😊",
    "option_issue": "Please select an option... 😕",
    "network_error": "Sorry, bad network connection 🌐",
    "unavailable_options": "Options not available",
}

app_color = {
    "primary": "#EECF89",
    "secondary": "#24DCA2",
    "extra_color": "#1C2331",
    "text_color": "#9B2E51",
    "hover_color": "#c9941d",
}

event_color = {
    "danger": "#AA1B48",
    "success": "#1BAA7D",
    "warning": "orange",
    "dark": "black",
}

widget_state = ["disabled", "normal"]

download_location = "~/Downloads"
"""
    {
        "download_location": "~/Downloads"
    }
"""

url_input = "Enter Youtube Video URL here 👉🏾: "
sample_url = "https://www.youtube.com/shorts/mBqK_-L-GVp"  # "https://www.youtube.com/shorts/mBqK_-L-PVg" (this url works)

# refactoring for reading for reading from config.json file
def read_config_file():
    with open("utilities/config.json", "r") as config_location:
        location = json.load(config_location)

    return location


class CodeChangeHandler(FileSystemEventHandler):
    """This is a handler for the code change event during development."""

    def __init__(self, callback, exclude_dir=None, exclude_file=None):
        super().__init__()
        self.callback = callback
        self.exclude_dir = exclude_dir
        self.exclude_file = exclude_file

    def on_any_event(self, event):
        if (
            event.is_directory
            and self.exclude_dir
            and event.src_path.startswith(self.exclude_dir)
        ):
            return
        if event.src_path == self.exclude_file:
            return
        if event.event_type in ["modified", "created", "deleted"]:
            self.callback()


# function from https://github.com/JNYH/pytube/blob/master/pytube_sample_code.ipynb
def clean_filename(name) -> str:
    """Ensures each file name does not contain forbidden characters and is within the character limit"""
    # For some reason the file system (Windows at least) is having trouble saving files that are over 180ish
    # characters.  I'm not sure why this is, as the file name limit should be around 240. But either way, this
    # method has been adapted to work with the results that I am consistently getting.

    forbidden_chars = "\"*\\/'.|?:<>"
    filename = (
        ("".join([x if x not in forbidden_chars else "#" for x in name]))
        .replace("  ", " ")
        .strip()
    )
    if len(filename) >= 176:
        filename = filename[:170] + "..."
    return filename


def validate_youtube_url(url) -> bool:
    "This makes sure the url provided is valid and acceptable. No one likes regex so i asked CHATGPT 🤣."

    youtube_regex = re.compile(
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=|shorts/)?([^&=%\?]{11})"
    )

    acceptable_urls = [
        "youtube.com/",
        "www.youtube.com/",
        "m.youtube.com/",
        "youtu.be/",
        "youtube-nocookie.com/",
    ]

    return youtube_regex.match(url) is not None or any(
        domain in url for domain in acceptable_urls
    )


def file_existance(youtube_url) -> int:
    """This function is a available for testing purposes, thus to compare
    it's result with the search_file_Availability function."""

    request = requests.get(youtube_url, allow_redirects=False)
    return request.status_code


async def search_file_Availability(youtube_url) -> int:
    """The name of the function speaks volumes of it self, it does what it says it does 🤣."""

    async with aiohttp.ClientSession() as session:
        async with session.get(youtube_url, allow_redirects=False) as response:
            return response.status


async def file_verification(youtube_url) -> bool:
    """This relys on the search_file_availability function and the validate_youtube_url function to make sure the Youtube file is available."""

    validatd_url = validate_youtube_url(youtube_url)
    status = await search_file_Availability(youtube_url) if validatd_url else None

    if status == 200 or 302:
        return True
    return False


def youtubefile(function):
    """This is a decorator that returns a Youtube Object, why? because it was supposed to make the code DRY 💔."""

    def wrapper(youtube_url):
        youtube_file = YouTube(youtube_url)
        return function(youtube_file)

    return wrapper


# adding stream codes to a list
@youtubefile
async def add_audio_stream_codes(youtube_file) -> list:
    """This function tries to extract the audio stream codes from the youtube url.
    it returns a list of audio stream codes. Its simply a list of lists, it has two indices and this is it's format:

    stream[abr][itag] where
        ::streams[0] returns a list of audio abr.
        ::streams[1] returns a list of audio stream itags from a Stream object.

    :fulldetails is for testing purposes ..."""

    streams: list = []
    itag: list = []
    abr: list = []

    fulldetails: list = []  # for testing purposesyyy
    available_audiofiles = youtube_file.streams.filter(only_audio=True)

    for available_audiofile in available_audiofiles:
        itag.append(available_audiofile.itag)
        abr.append(available_audiofile.abr)
        # fulldetails.append(available_audiofile)

    streams.append(abr)
    streams.append(itag)
    # streams.append(fulldetails)
    return streams


@youtubefile
async def add_video_stream_code(youtube_file) -> list:
    """
    The use of a youtubefile decorator does not make this function any special, this gets video itags and video resolution from a Stream object.
    This is also a list of lists with two indices and should be implemented in the following format:
        :: stream[0] -> return list of video resolution.
        :: stream[1] -> return list of itags.
    """

    streams: list = []
    itag: list = []
    video_resolution: list = []

    available_videofiles = youtube_file.streams.filter(file_extension="mp4")

    for available_videofile in available_videofiles:
        itag.append(available_videofile.itag)
        resolution = available_videofile.resolution
        codec = available_videofile.video_codec

        if resolution != None:
            video_resolution.append(f"{resolution} | { codec }")

    streams.append(video_resolution)
    streams.append(itag)
    return streams


async def check_internet_connection(youtube_url) -> bool:
    """
    Check if an internet connection is available by attempting to open a URL within a specified timeout.

    Parameters:
    youtube_url (str): The URL to check for internet connection.

    Returns:
    bool: True if the URL can be opened within the timeout, False otherwise.

    Raises:
    None.

    Example:
    >>> is_connected = asyncio.run( check_internet_connection("https://www.youtube.com/") )
    >>> print(is_connected)
    True
    """

    try:
        await asyncio.to_thread(urllib.request.urlopen, youtube_url, timeout=5)
        return True
    except (urllib.error.URLError, asyncio.TimeoutError):
        return False


# this function will be revisited in the future.
def connection_checker(function, error_callback=None):
    async def wrapper(youtube_url):
        loop = asyncio.get_event_loop()
        coroutine = check_internet_connection(youtube_url)

        future = asyncio.run_coroutine_threadsafe(coroutine, loop=loop)
        network_check = future.result()

        if network_check:
            return await function(youtube_url)
        else:
            return error_callback

    return wrapper


@youtubefile
async def downloadfile_details(youtube_file) -> dict:
    """
    This function retrieves relevant information from a YouTube object.

    Returns:
    dict: A dictionary containing the details of the `youtube_file` object.

    Raises:
    None.

    Example:
    >>> file_details = asyncio.run( downloadfile_details(youtube_url) )
    >>> print(file_details)
    {'title': 'Rick Astley - Never Gonna Give You Up (Video)', 'author': 'Rick Astley', 'length': '00:03:33', 'thumbnail': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg', 'views': '1,373,364,201', 'date': '12 years ago'}
    """

    title = youtube_file.title
    author = youtube_file.author
    video_description = youtube_file.description
    video_info = youtube_file.vid_info

    lenght = youtube_file.length
    thumbnail = youtube_file.thumbnail_url
    channel = youtube_file.channel_url
    views = youtube_file.views

    upload_date = youtube_file.publish_date
    file_info: dict = {
        "title": title,
        "author": author,
        # "description": video_description,
        # "info": video_info,
        "length": precisedelta(lenght, suppress=['seconds', 'milliseconds', 'microseconds']),
        "thumbnail": thumbnail,
        # "channel": channel,
        "views": views,
        "date": precisedelta(upload_date), # naturaldelta(upload_date, months=True, minimum_unit='hours')
    }

    return file_info
