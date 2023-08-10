import pytest
from .lang import validate_youtube_url

def test_url_validation():
    assert(validate_youtube_url("https://www.youtube.com/watch?v=r6tH55syq0o")) == True
    assert(validate_youtube_url("https://www.youtube.com/shorts/mBqK_-L-PVg")) == True
    assert(validate_youtube_url("http://linuxcommand.org/lc3_writing_shell_scripts.php")) == False