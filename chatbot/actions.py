from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function

from typing import Dict, Text, Any, List, Union, Type, Optional
from pymongo import MongoClient

import typing
import logging
from modules.utils import *
from modules.diagnose import encode_symptom, create_illness_vector, get_diagnosis
from modules.scrapper import *
import os
import requests
from os import environ
import uuid
CONNECTION_STRING = environ.get("MONGODB_STRING")
client = MongoClient(CONNECTION_STRING)

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType, SessionStarted, ActionExecuted
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

from datetime import datetime, date, time, timedelta

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def fetch_slots(tracker):
        slots = []
        for key in ("name", "username", "password", "age", "height", "weight"):
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=value))
        return slots

    async def run(self, dispatcher, tracker, domain):
        events = [SessionStarted()]
        events.extend(self.fetch_slots(tracker))
        events.append(ActionExecuted("action_listen"))
        name = tracker.get_slot("name")
        print(name,  events)
        if len(name) >0:
            dispatcher.utter_message(f"Hello {name}, how is the day treating you !!")
        else:
            dispatcher.utter_message("Hi, can i know your name")
        return events

class ActionGetCredentials(Action):
    def name(self):
        return "action_get_credentials"
    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot('username')
        db = client.get_database('authenticate')
        collection = db['users']
        user = collection.find_one({'name' : username})
        if (user):
            password = user['password'].decode().encode('utf-8')
            return [SlotSet("password", password)]
        else:
            dispatcher.utter_message("Are you sure you have uttered the right username...try again...")

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
            url = get_music(emotion)
            dispatcher.utter_message("Here is something for your mood.")
            dispatcher.utter_message(json_message={"payload":"video","data":url})
        else:
            dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")

class ActionGetQuote(Action):
    def name(self):
        return "action_get_quote"

    def run(self, dispatcher, tracker, domain):
        image = get_quotes()
        dispatcher.utter_message(image=image)

class ActionShowMap(Action):
    def name(self):
        return "action_show_map"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(json_message={"payload":"map"})

class ActionGetJoke(Action):
    def name(self):
        return "action_get_joke"

    def run(self, dispatcher, tracker, domain):
        joke = get_jokes()
        dispatcher.utter_message(f"{joke}")

'''Get "action_weather" data'''
class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        app_id = environ.get("WEATHER_ID")
        app_key = environ.get("WEATHER_KEY")
        base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
        location = tracker.get_slot('location')
        Final_url = base_url + "app_id=" + app_id + "&app_code=" + app_key + "&product=observation&name=" + location 
        weather_data = requests.get(Final_url).json()

        if (len(weather_data) > 2):
            # JSON data works just similar to python dictionary and you can access the value using [].
            current_temperature =  weather_data['observations']['location'][0]['observation'][0]['temperature']
            wind=weather_data['observations']['location'][0]['observation'][0]['windSpeed']
            desc=weather_data['observations']['location'][0]['observation'][0]['description']

            response = """ It is {} in {} at this moment. The temperature is {} degree and the wind speed is {} m/s. """. format(desc, location, current_temperature, wind)
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("City Not Found ")
 

'''Get "action_temp" data'''
class ActionTemperature(Action):
    def name(self):
        return 'action_temp'
      
    def run(self, dispatcher, tracker, domain):
        app_id = environ.get("WEATHER_ID")
        app_key = environ.get("WEATHER_KEY")
        base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
        location = tracker.get_slot('location')
        Final_url = base_url + "app_id=" + app_id + "&app_code=" + app_key + "&product=observation&name=" + location 
 
        weather_data = requests.get(Final_url).json()

        if (len(weather_data) > 2):
            # JSON data works just similar to python dictionary and you can access the value using [].
            current_temperature =  weather_data['observations']['location'][0]['observation'][0]['temperature']

            response = """ The temperature in {} is now {} degree currently """. format(location, current_temperature)
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message("City Not Found ")

class ActionDiagnoseSymptoms(Action):

    def name(self):
        return "action_diagnose_symptoms"

    def run(self, dispatcher, tracker, domain):

        symptoms = tracker.get_slot("symptom")
        encoded_symptoms = [encode_symptom(symptom) for symptom in symptoms]
        illness_vector = create_illness_vector(encoded_symptoms)
        diagnosis_string = get_diagnosis(illness_vector)
        dispatcher.utter_message(text=diagnosis_string)

class ActionSymptoms(Action):

    def name(self):
        return "action_symptoms"

    def run(self, dispatcher, tracker, domain):

        symptoms = tracker.get_slot("symptom")
        try:  
            data=get_details(symptoms)
            dispatcher.utter_message(json_message={"payload":"symptom","data":data})
        except:
            dispatcher.utter_message(text="Sorry couldn't find the data for the given symptom.")


class EHR(FormAction):

    def name(self):
        return "ehr"

    @staticmethod
    def required_slots(tracker):
        return["username", "password", "age", "height", "weight", ""]

    def slot_mappings(self):

        return {
            "cuisine": self.from_entity(entity="cuisine", not_intent="chitchat"),
            "num_people": [
                self.from_entity(
                    entity="number", intent=["inform", "request_restaurant"]
                ),
            ],
            "outdoor_seating": [
                self.from_entity(entity="seating"),
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "preferences": [
                self.from_intent(intent="deny", value="no additional preferences"),
                self.from_text(not_intent="affirm"),
            ],
            "feedback": [self.from_entity(entity="feedback"), self.from_text()],
        }

    @staticmethod
    def cuisine_db():

        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]

    @staticmethod
    def is_int(string):
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if value.lower() in self.cuisine_db():
            return {"cuisine": value}
        else:
            dispatcher.utter_message(template="utter_wrong_cuisine")
            return {"cuisine": None}

    def validate_num_people(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate num_people value."""

        if self.is_int(value) and int(value) > 0:
            return {"num_people": value}
        else:
            dispatcher.utter_message(template="utter_wrong_num_people")
            # validation failed, set slot to None
            return {"num_people": None}

    def validate_outdoor_seating(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate outdoor_seating value."""

        if isinstance(value, str):
            if "out" in value:
                # convert "out..." to True
                return {"outdoor_seating": True}
            elif "in" in value:
                # convert "in..." to False
                return {"outdoor_seating": False}
            else:
                dispatcher.utter_message(template="utter_wrong_outdoor_seating")
                # validation failed, set slot to None
                return {"outdoor_seating": None}

        else:
            return {"outdoor_seating": value}

    def submit(self,dispatcher,tracker, domain):
        dispatcher.utter_message(template="utter_submit")
        return []


