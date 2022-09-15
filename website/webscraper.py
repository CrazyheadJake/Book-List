import urllib.request
from serpapi import GoogleSearch

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}


def get_cover(title, author):
    params = {
        "q": title + " by " + author,  # search query
        "tbm": "isch",  # image results
        "hl": "en",  # language of the search
        "gl": "us",  # country where search comes from
        "ijn": "0",  # page number
        "api_key": '094198f325c21c3bb0b991bf56605ded5a698f7b24c91245825502cae03ee4f4'
    }

    search = GoogleSearch(params)

    results = search.get_dict()
    print(results)
    image = results["images_results"][0]["original"]
    return image

    # opener = urllib.request.build_opener()
    # opener.addheaders = [("User-Agent",
    #                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
    # urllib.request.install_opener(opener)
    #
    # urllib.request.urlretrieve(image, f"website/static/covers/{entry.id}.jpg")
