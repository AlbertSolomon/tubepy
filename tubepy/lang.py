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

# this input variable will be used for testing purposes
def test_url_input():
    url_input = "Enter Youtube Video URL here 👉🏾: " 
    return input(url_input)

# refactoring for reading for reading from config.json file
def read_config_file():
    with open('utilities/config.json', 'r') as config_location:
        loction = json.load(config_location)
        
    return loction

# print(read_config_file())