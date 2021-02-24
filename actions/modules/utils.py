import os
import json
import json
import random
import urllib.request
import urllib.parse
import re
from .quotes import get_base64


path = "assets/json"

def get_url(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'url\":\"\/watch\?v=(.{11})', html_content.read().decode())
    url = f"https://www.youtube.com/embed/{search_results[0]}?autoplay=1"
    return url


def get_music(emotion):
    with open(os.path.join(path, 'music.json'), 'r') as f:
        music = json.load(f)
    query = random.choice(music[emotion])
    url = get_url(query)
    return url

def get_jokes():
    with open(os.path.join(path, 'jokes.txt'), 'r') as f:
        jokes = json.load(f)
    return random.choice(jokes)

def get_quotes():
    with open(os.path.join(path, 'quotes.json'), 'r', encoding="utf8") as f:
        quotes = json.load(f)
    quote = random.choice(quotes)
    image = get_base64(f'{quote["Quote"]}   \n  --  {quote["Author"]}  -- ')
    return image

if __name__ == "__main__":
    print(get_music('happy'))
    print(get_jokes())
    print(get_quotes())