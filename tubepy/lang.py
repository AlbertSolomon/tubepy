import json

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