import urllib.request
from serpapi import GoogleSearch

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}


def format(date):
    y = date.year
    m = date.month
    d = date.day
    return f"{m}/{d}/{y}"


def sort_entries(entry):
    return entry.date.toordinal()


def get_cover(title, author):
    params = {
        "q": title + " by " + author,  # search query
        "tbm": "isch",  # image results
        "hl": "en",  # language of the search
        "gl": "us",  # country where search comes from
        "ijn": "0",  # page number
        "api_key": '8c41d449d143b3d6dd32853d00108ba2f42f0a98e0ed9a6a61b6434adb8b7b1f'
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
