from app import download, audio_download, DASH_download, quick_download
from settings import download_path_settings, change_download_location
import asyncio
from lang import url_input, validate_youtube_url, search_file_Availability, sample_url, file_verification, add_audio_stream_codes, file_existance

# this input variable will be used for testing purposes
def test_url_input() -> None:  
    return input(url_input)

# download_path_settings()
# download(test_url_input())

# audio_download(test_url_input())
# DASH_download(test_url_input())

# quick_download(test_url_input())
# print(validate_youtube_url(sample_url))

print(file_existance(sample_url))
print(asyncio.run(search_file_Availability(sample_url)))
print(asyncio.run(file_verification(sample_url)))

audio_streams: list = add_audio_stream_codes(test_url_input())
print(audio_streams[0])
fstring = str(audio_streams[0])
print(fstring[9:19])

def stripping_audio_streams(audio_streams) -> list:
    new_audio_list: list= []
    
    for audio_stream in audio_streams:
        temp_audio_file = str(audio_stream)
        new_audio_stream_file = temp_audio_file[9:19]
        new_audio_list.append(new_audio_stream_file)
        
    return new_audio_list

nwLists = stripping_audio_streams(audio_streams)    
print(nwLists)