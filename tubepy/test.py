from app import download, audio_download
from settings import download_path_settings, change_download_location
from lang import url_input

# this input variable will be used for testing purposes
def test_url_input():  
    return input(url_input)

# download_path_settings()
# download(test_url_input)
audio_download(test_url_input())