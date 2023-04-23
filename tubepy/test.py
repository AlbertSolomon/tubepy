import asyncio

from app import DASH_download, audio_download, download, quick_download, test_download
from lang import (
    add_audio_stream_codes,
    add_video_stream_code,
    check_internet_connection,
    downloadfile_details,
    file_existance,
    file_verification,
    sample_url,
    search_file_Availability,
    url_input,
    validate_youtube_url,
    playlist_details,
)
from settings import change_download_location, download_path_settings


# this input variable will be used for testing purposes
def test_url_input() -> None:
    return input(url_input)


# download_path_settings()
# download(test_url_input())

# audio_download(test_url_input())
# DASH_download(test_url_input())

# quick_download(test_url_input())
# print(validate_youtube_url(sample_url))

# print(file_existance(sample_url))
# print(asyncio.run(search_file_Availability(sample_url)))
# print(asyncio.run(file_verification(sample_url)))

# audio_streams: list = []
# audio_streams = asyncio.run( add_audio_stream_codes(test_url_input()) )
# print(f"audio streams| { audio_streams[0] }")
#
# # print(asyncio.run(add_video_stream_code("https://www.youtube.com/watch?v=LRQJsm1uGJU")))
# print(asyncio.run(check_internet_connection("https://www.youtube.com/watch?v=LRQJsm1uGJU")))

# streams_test(test_url_input())

#print(asyncio.run(downloadfile_details(test_url_input())))
#print(asyncio.run(playlist_details(test_url_input())))

test_download(test_url_input())