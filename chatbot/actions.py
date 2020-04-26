from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Type, Optional

import typing
import logging
import requests
import json
import csv
import random
import urllib.request
import urllib.parse
import re

import os
import infermedica_api

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime, date, time, timedelta
from fetchable import FetchableClient
from fetchable import configuration

with open('data/extdata/music.json', 'r') as emotions:
    data = json.load(emotions)

try: 
    client = FetchableClient(api_version=configuration.api_version.latest,auth_file='fetchable_auth_keys.json') 
except:
    print("something went wrong.................")

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
        emotion = None
        entities = tracker.latest_message['entities']
        for entity in entities:
            if entity['entity'] == "emotion":
                emotion = entity['value']
        if emotion:
            query = random.choice(data[emotion])
            url = get_url(query)
            print(emotion, query, url)
            dispatcher.utter_message("Here is something for your mood.")
            dispatcher.utter_message(json_message={"payload":"video","data":url})
        else:
            dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")


class ActionGetQuote(Action):
    def name(self):
        return "action_get_quote"

    def run(self, dispatcher, tracker, domain):
        response = client.fetch_quote()
        if response['status_code'] == 200:
            dispatcher.utter_message(f"{response['quote']} by {response['author']}")
        elif response['status_code'] == 1001:
            dispatcher.utter_message("I cannot connect to internet right now !!")
        else:
            dispatcher.utter_message("Sorry, if i couldnt help you")


class ActionGetJoke(Action):
    def name(self):
        return "action_get_joke"

    def run(self, dispatcher, tracker, domain):
        response = client.fetch_joke()
        print(response)
        if response['status_code'] == 200:
            dispatcher.utter_message(f"{response['setup']} {response['punchline']}")
            print(response)
        elif response['status_code'] == 1001:
            dispatcher.utter_message("I cannot connect to internet right now !!")
        else:
            dispatcher.utter_message("Sorry, if i couldnt help you")


class ActionGetFunFact(Action):
    def name(self):
        return "action_get_fun_fact"

    def run(self, dispatcher, tracker, domain):
        response = client.fetch_fun_fact()
        if response['status_code'] == 200:
            dispatcher.utter_message(f"{response['fun_fact']}")
        elif response['status_code'] == 1001:
            dispatcher.utter_message("I cannot connect to internet right now !!")
        else:
            dispatcher.utter_message("Sorry, if i couldnt help you")

# '''Get "action_weather" data'''
# class ActionWeather(Action):
#     def name(self):
#         return 'action_weather'

#     def run(self, dispatcher, tracker, domain):
#         app_id = "JnnC8L7yA6ebC44rCiuj"
#         app_key = "twQ8s3NiYo2MCBZfj1pZAQ"
#         base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
#         location = tracker.get_slot('location')
#         Final_url = base_url + "app_id=" + app_id + "&app_code=" + app_key + "&product=observation&name=" + location 
 
#         weather_data = requests.get(Final_url).json()

#         if (len(weather_data) > 2):
#             # JSON data works just similar to python dictionary and you can access the value using [].
#             current_temperature =  weather_data['observations']['location'][0]['observation'][0]['temperature']
#             wind=weather_data['observations']['location'][0]['observation'][0]['windSpeed']
#             desc=weather_data['observations']['location'][0]['observation'][0]['description']

#             response = """ It is {} in {} at this moment. The temperature is {} degree and the wind speed is {} m/s. """. format(desc, location, current_temperature, wind)
#             dispatcher.utter_message(response)
#         else:
#             dispatcher.utter_message("City Not Found ")
 

# '''Get "action_temp" data'''
# class ActionTemperature(Action):
#     def name(self):
#         return 'action_temp'
      
#     def run(self, dispatcher, tracker, domain):
#         app_id = "JnnC8L7yA6ebC44rCiuj"
#         app_key = "twQ8s3NiYo2MCBZfj1pZAQ"
#         base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
#         location = tracker.get_slot('location')
#         Final_url = base_url + "app_id=" + app_id + "&app_code=" + app_key + "&product=observation&name=" + location 
 
#         weather_data = requests.get(Final_url).json()

#         if (len(weather_data) > 2):
#             # JSON data works just similar to python dictionary and you can access the value using [].
#             current_temperature =  weather_data['observations']['location'][0]['observation'][0]['temperature']

#             response = """ The temperature in {} is now {} degree currently """. format(location, current_temperature)
#             dispatcher.utter_message(response)
#         else:
#             dispatcher.utter_message("City Not Found ")
    



