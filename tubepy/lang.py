import json
import re
import requests # this has been abundonned since its not asynchronous
import asyncio
import aiohttp
from pytube import YouTube

downloadstatus = {
    "load": "loading... 😒",
    "successful": " download successful 🥳",
    "unsuccessful": "download failed... 💔", 
}

empty = {
    "empty_location":  " empty default location",
}

error_message ={
    "invalid_length": "Invalid url length !. The URL length you have provided might be too short or too long 😥"
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

download_location = '~/Downloads'
'''
    {
        "download_location": "~/Downloads"
    }
'''

url_input = "Enter Youtube Video URL here 👉🏾: "
sample_url = "https://www.youtube.com/shorts/mBqK_-L-GVp" #"https://www.youtube.com/shorts/mBqK_-L-PVg" (this url works) 

# refactoring for reading for reading from config.json file
def read_config_file():
    with open('utilities/config.json', 'r') as config_location:
        location = json.load(config_location)
        
    return location

# print(read_config_file())

# progressive tags for video formats
progressive_vtags = {
    "144p": 17,
    "360p": 18,
    "720p": 22,
}

# function from https://github.com/JNYH/pytube/blob/master/pytube_sample_code.ipynb
def clean_filename(name) -> str:
        """Ensures each file name does not contain forbidden characters and is within the character limit"""
        # For some reason the file system (Windows at least) is having trouble saving files that are over 180ish
        # characters.  I'm not sure why this is, as the file name limit should be around 240. But either way, this
        # method has been adapted to work with the results that I am consistently getting.
        forbidden_chars = '"*\\/\'.|?:<>'
        filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
        if len(filename) >= 176:
            filename = filename[:170] + '...'
        return filename
    
def validate_youtube_url(url) -> bool:
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    return youtube_regex.match(url) is not None

async def search_file_Availability(youtube_url) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(youtube_url, allow_redirects=False) as response:
            return response.status

async def file_verification(youtube_url) -> bool:
    validatd_url = validate_youtube_url(youtube_url)
    status = await search_file_Availability(youtube_url) if validatd_url else None
    if status == 200:
        return True
    return False

# adding stream codes to a list 
def add_audio_stream_codes(youtube_url) -> list:
    youtube_file = YouTube(youtube_url)
    streams: list = []
    
    available_audiofiles = youtube_file.streams.filter(only_audio=True)
    for available_audiofile in available_audiofiles:
        streams.append(available_audiofile)
        
    return streams