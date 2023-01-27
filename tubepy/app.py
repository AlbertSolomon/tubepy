from pytube import YouTube
from ffmpeg import FFmpeg, Progress, ffmpeg
from lang import read_config_file, progressive_vtags, clean_filename
import time
import subprocess

# try to read from config.json file where to store the downloaded video
video_res = progressive_vtags.get("720p")
audio_fq:int = 140
current_time = time.time()

location = read_config_file()
preferred_location = location["download_location"]
# print(preferred_location)

def download(youtube_url):
    youtube_file = YouTube(youtube_url)
    
    # for testing purposes
    available_youtube_files = youtube_file.streams.filter(progressive=True)
    for yt_stream in available_youtube_files:
        print(yt_stream)

    # downloading progressive videos ( allowing users to choose theie desird resolutions)yo
    progressive_res = youtube_file.streams.get_by_itag(video_res)
    progressive_res.download(preferred_location) 
    
#? download audio files from youtube
def audio_download(youtube_url):
    youtube_file = YouTube(youtube_url)
    
    # for testing purposes
    available_audiofiles = youtube_file.streams.filter(only_audio=True)
    for available_audiofile in available_audiofiles:
        print(available_audiofile)
        
    audio_file = youtube_file.streams.get_by_itag(audio_fq)
    audio_file.download(preferred_location)

#? download Dynamic Adaptive Streaming over HTTP (DASH) and merge them with ffmpeg from youtube
def DASH_download(youtube_url):
    youtube_file = YouTube(youtube_url)
    
    try:        
        youtube_file.streams.filter(res='1080p', progressive= False).first().download(preferred_location, filename="video.mp4")
        youtube_file.streams.filter(abr='160kbps', progressive= False).first().download(preferred_location, filename="audio.mp3")
    except:
        youtube_file.streams.filter(res='720p', progressive= False).first().download(preferred_location, filename="video.mp4")
        youtube_file.streams.filter(abr='128kbps', progressive= False).first().download(preferred_location, filename="audio.mp3")
        
    # audio = FFmpeg().option("y").input(audio_url, 'audio.mp3')
    # video = FFmpeg().option("y").input(audio_url, 'video.mp4')
    # video = FFmpeg.input(video_url, 'video.mp4')
    # 
    # FFmpeg.output(audio, video, filename).run(overwrite_output=True)
    # # tracking the time
    # print('Time taken:'.format(time.time() - current_time))
        

#? download video files from youtube with other formats
