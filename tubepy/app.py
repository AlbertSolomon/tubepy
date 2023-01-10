from pytube import YouTube
import ffmpeg
import json
from lang import read_config_file, download_location, empty, progressive_vtags

# with importlib.resources.
# using new_location for testing purposes
new_location:str = "~/Music"
def change_download_location(new_location):
    try:
        # default_location = read_config_file
        default_location = read_config_file()
        default_location["download_location"] = new_location

        with open('utilities/config.json', 'w') as file_location:
            json.dump(default_location, file_location, indent=4 )
        
    except Exception:
        print(empty.get("empty_location"))
    else:
        default_location["download_location"] = download_location
        
# change_download_location(new_location)


# try to read from config.json file where to store the downloaded video
location:str = ''
video_res = progressive_vtags.get("720p")
def download(youtube_url):
    
    location = read_config_file()
    preferred_location = location["download_location"]
    # print(preferred_location)
    
    youtube_file = YouTube(youtube_url)
    available_youtube_files = youtube_file.streams.filter(progressive=True)
    
    for yt_stream in available_youtube_files:
        print(yt_stream)
    
    # downloading progressive videos ( allowing users to choose theie desird resolutions)yo
    progressive_res = youtube_file.streams.get_by_itag(video_res)
    progressive_res.download(preferred_location)
          