import json
import re
import requests

downloadstatus = {
    "load": "loading... 😒",
    "successful": " download successful 🥳",
    "unsuccessful": "download failed... 💔", 
}

empty = {
    "empty_location":  " empty default location",
}

download_location = '~/Downloads'
'''
    {
        "download_location": "~/Downloads"
    }
'''

url_input = "Enter Youtube Video URL here 👉🏾: "
sample_url = "https://www.youtube.com/shorts/mBqK_-L-GVp" #https://www.youtube.com/shorts/mBqK_-L-PVg (this url works) 

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
def clean_filename(name):
        """Ensures each file name does not contain forbidden characters and is within the character limit"""
        # For some reason the file system (Windows at least) is having trouble saving files that are over 180ish
        # characters.  I'm not sure why this is, as the file name limit should be around 240. But either way, this
        # method has been adapted to work with the results that I am consistently getting.
        forbidden_chars = '"*\\/\'.|?:<>'
        filename = (''.join([x if x not in forbidden_chars else '#' for x in name])).replace('  ', ' ').strip()
        if len(filename) >= 176:
            filename = filename[:170] + '...'
        return filename
    
def validate_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    return youtube_regex.match(url) is not None

def file_Availability(youtube_url):
    request = requests.get(youtube_url, allow_redirects=False)
    return request.status_code