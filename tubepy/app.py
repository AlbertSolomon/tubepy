from pytube import YouTube
import ffmpeg
from lang import read_config_file, progressive_vtags

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