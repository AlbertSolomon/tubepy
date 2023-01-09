import json

downloadstatus = {
    "load": "loading... 😒",
    "successful": " download successful 🥳",
    "unsuccessful": "download failed... 💔", 
}

download_location = '~/Downloads'
'''
    {
        "download_location": "~/Downloads"
    }
'''

# refactoring for reading for reading from config.json file
def read_config_file():
    with open('utilities/config.json', 'r') as config_location:
        loction = json.load(config_location)
        
    return loction

# print(read_config_file())