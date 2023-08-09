import pytest
from .lang import validate_youtube_url

def test_url_validation():
    assert(validate_youtube_url("https://www.youtube.com/watch?v=r6tH55syq0o")) == True