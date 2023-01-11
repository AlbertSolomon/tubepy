from app import download
from settings import download_path_settings, change_download_location

# this input variable will be used for testing purposes
def test_url_input():
    url_input = "Enter Youtube Video URL here 👉🏾: " 
    return input(url_input)


# download_path_settings()
# download(test_url_input)