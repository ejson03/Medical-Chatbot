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
with open('music.json', 'r') as emotions:
    data = json.load(emotions)

def get_url(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    url = f"https://www.youtube.com/embed/{search_results[0]}?autoplay=1"
    return url


class ActionMed(Action):
    def name(self):
        return 'action_medicine'

    def run(self, dispatcher, tracker, domain):
        api = infermedica_api.API(app_id='f1acb630', app_key='41b6c31e0d5158d1dbab51958f216cfc')
        print(api.info()) 
        choices = {}
        buttons = []
        symp = tracker.get_slot('symptom')
        request = infermedica_api.Diagnosis(sex='male', age='25')

        symp = api.parse(symp).to_dict()
        symp_id = symp['mentions'][0]['id']
        request.add_symptom(symp_id, 'present')

        request = api.diagnosis(request)
        items = request.question.items

        for choice in items:
            choices[choice['id']] = choice['name']

        response = request.question.text

        for key, value in choices.items():
            title = value
            request.add_symptom(key, 'present')
            request = api.diagnosis(request)
            text = request.question.text
            buttons.append({"title": title, "payload": text})
        #  response = "Let's try this medicine"

        dispatcher.utter_button_message(response, buttons)
        #  return [SlotSet('symptom', symp)]
        return []

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

