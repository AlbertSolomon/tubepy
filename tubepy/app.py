from pytube import YouTube
import ffmpeg
from lang import read_config_file, progressive_vtags

# try to read from config.json file where to store the downloaded video
video_res = progressive_vtags.get("720p")

location = read_config_file()
preferred_location = location["download_location"]
# print(preferred_location)

def download(youtube_url):
    youtube_file = YouTube(youtube_url)
    available_youtube_files = youtube_file.streams.filter(progressive=True)
    
    # for testing purposes
    for yt_stream in available_youtube_files:
        print(yt_stream)

    # downloading progressive videos ( allowing users to choose theie desird resolutions)yo
    progressive_res = youtube_file.streams.get_by_itag(video_res)
    progressive_res.download(preferred_location) 
    
#? download audio files from youtube
def audio_download(youtube_url):
    pass 

#? download Dynamic Adaptive Streaming over HTTP (DASH) and merge them with ffmpeg from youtube

#? download video files from youtube with other formats