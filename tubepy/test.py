from app import download

# this input variable will be used for testing purposes
def test_url_input():
    url_input = "Enter Youtube Video URL here 👉🏾: " 
    return input(url_input)


test_input = test_url_input()
download(test_input)