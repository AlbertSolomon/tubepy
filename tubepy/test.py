from app import download, audio_download, DASH_download, quick_download
from settings import download_path_settings, change_download_location
from lang import url_input, validate_youtube_url, file_Availability, sample_url

# this input variable will be used for testing purposes
def test_url_input():  
    return input(url_input)

# download_path_settings()
# download(test_url_input())

# audio_download(test_url_input())
# DASH_download(test_url_input())

#quick_download(test_url_input())

print(validate_youtube_url(sample_url))
print(file_Availability(sample_url))