import random
import json
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import urllib.request
import urllib.parse
import re

with open('music.json', 'r') as emotions:
    data = json.load(emotions)

def get_url(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url = f"https://www.youtube.com/embed/{search_results[0]}?autoplay=1"
    return url

class ActionGetSong(Action):
    def name(self):
        return "action_get_song"

    def run(self, dispatcher, tracker, domain):
        emotion = tracker.latest_message['entities'][0]
        emotion = emotion['value']
        if len(emotion) == 0:
            dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")
        query = random.choice(data[emotion])
        url = get_url(query)
        print(emotion, query, url)
        dispatcher.utter_message("Here is something for your mood.")
        dispatcher.utter_message(json_message={"payload":"video","data":url})

# class ActionGetQuote(Action):
#     def name(self):
#         return "action_get_quote"

#     def run(self, dispatcher, tracker, domain):
#         emotion = tracker.latest_message['entities'][0]
#         emotion = emotion['value']
#         if len(emotion) == 0:
#             dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")
#         query = random.choice(data[emotion])
#         url = get_url(query)
#         print(emotion, query, url)
#         dispatcher.utter_message("Here is something for your mood.")
#         dispatcher.utter_message(json_message={"payload":"video","data":url})

# class ActionGetImage(Action):
#     def name(self):
#         return "action_get_image"

#     def run(self, dispatcher, tracker, domain):
#         emotion = tracker.latest_message['entities'][0]
#         emotion = emotion['value']
#         if len(emotion) == 0:
#             dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")
#         query = random.choice(data[emotion])
#         url = get_url(query)
#         print(emotion, query, url)
#         dispatcher.utter_message("Here is something for your mood.")
#         dispatcher.utter_message(json_message={"payload":"video","data":url})

