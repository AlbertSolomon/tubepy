import os
import subprocess
import time

from ffmpeg import FFmpeg, Progress, ffmpeg
from lang import clean_filename, error_message, read_config_file
from pytube import YouTube

current_time = time.time()

location = read_config_file()
preferred_location = location["download_location"]

# TODO lETS TRY TO USED A YOUTUBE FILE DECORETOR SO THAT WE MAKE THE CODE D.R.Y
def quick_download(youtube_url, on_progress):     
    """Download a YouTube video or playlist and save it to the given output directory."""
    if 'playlist' in youtube_url:
        playlist = Playlist(youtube_url)
        video_count = len(playlist.video_urls)
        for i, video_url in enumerate(playlist.video_urls):
            print(f"Downloading video {i+1} of {video_count}")
            youtube_file = YouTube(video_url, on_progress_callback=on_progress)
            youtube_file.streams.get_highest_resolution().download(preferred_location)
    else:
        youtube_file = YouTube(youtube_url, on_progress_callback=on_progress)
        youtube_file.streams.get_highest_resolution().download(preferred_location)


def data_save_download(youtube_url, on_progress):
    youtube_file = YouTube(youtube_url, on_progress_callback=on_progress)
    youtube_file.streams.get_lowest_resolution().download(preferred_location)


def download(youtube_url, on_progress, itag):
    youtube_file = YouTube(youtube_url, on_progress_callback=on_progress)

    # downloading progressive videos ( allowing users to choose theie desird resolutions)yo
    progressive_res = youtube_file.streams.get_by_itag(itag=itag)
    progressive_res.download(preferred_location)


# ? download audio files from youtube
def audio_download(youtube_url, on_progress, itag):
    """
    added exception handler for convessionall purposes
    """
    try:
        youtube_file = YouTube(youtube_url, on_progress_callback=on_progress)

    # this is yet to be tested
    except VideoUnavailable:
        print(error_message.get("VideoUnavailable"))
    else:
        audio_file = youtube_file.streams.get_by_itag(itag)
        audio_file.download(preferred_location)


# ? download Dynamic Adaptive Streaming over HTTP (DASH) and merge them with ffmpeg from youtube
def DASH_download(youtube_url):
    youtube_file = YouTube(youtube_url)

    try:
        youtube_file.streams.filter(res="1080p", progressive=False).first().download(
            preferred_location, filename="video.mp4"
        )
        youtube_file.streams.filter(abr="160kbps", progressive=False).first().download(
            preferred_location, filename="audio.mp3"
        )
    except:
        youtube_file.streams.filter(res="720p", progressive=False).first().download(
            preferred_location, filename="video.mp4"
        )
        youtube_file.streams.filter(abr="128kbps", progressive=False).first().download(
            preferred_location, filename="audio.mp3"
        )

    # audio = FFmpeg().option("y").input(audio_url, 'audio.mp3')
    # video = FFmpeg().option("y").input(audio_url, 'video.mp4')
    # video = FFmpeg.input(video_url, 'video.mp4')
    #
    # FFmpeg.output(audio, video, filename).run(overwrite_output=True)
    # # tracking the time
    # print('Time taken:'.format(time.time() - current_time))

    # ? TRYING TO SELECT VIDEO AND AUDIO FILES FROM PREFERRED DIRECTORY
    # ? KEPT GETTING FILE NOT FOUND ERROR WHEN TRYING TO MERGE THE VIDEO AND AUDIO FILES USING FFMP
    video = "video.mp4"
    audio = "audio.mp3"
    output_file = preferred_location + "\\\output.mp4"

    folder = []
    for files in os.scandir(preferred_location):
        if files.name == video or files.name == audio:
            folder.append(files.path)
            print(files.path)
    print(folder)
    print(output_file)

    # subprocess.run(['ffmpeg', '-i', folder[1], '-i', folder[0], '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file])


# ? download video files from youtube with other formats
