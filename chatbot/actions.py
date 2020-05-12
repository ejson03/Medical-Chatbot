from pymongo import MongoClient

import typing
from typing import Dict, Text, Any, List, Union, Optional, Tuple
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
import base64
from sys import getsizeof

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType, SessionStarted, ActionExecuted, FollowupAction, BotUttered, Form, EventType
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
# from modules.ehr import User
# from modules.vault import Config
VAULT_URL = environ.get("VAULT_URL", "192.168.33.150:8002")
VAULT_KEY = environ.get("VAULT_KEY", "myroot")
from datetime import datetime, date, time, timedelta
from modules.encryption import encrypt, ipfs_add
import base64

class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("filedesc", None)]

class ActionGetCredentials(Action):
    def name(self):
        return "action_get_credentials"

    @staticmethod
    def fetch_slots(tracker):
        slots = []
        for key in ["username", "password", "age", "height", "weight"]:
            value = tracker.get_slot(key)
            if value is not None:
                slots.append(SlotSet(key=key, value=value))
        return slots

    def run(self, dispatcher, tracker, domain):
        username = tracker.sender_id
        slots = self.fetch_slots(tracker)
        if not any("password" in slot for slot in slots):
            db = client.get_database('authenticate')
            collection = db['users']
            user = collection.find_one({'name' : username})
            if (user):
                password = user['password'].decode().encode('utf-8')
                slots.extend([SlotSet(key="username", value=username), SlotSet(key="password", value=password)])
            else: 
                raise Exception("Did not find user...")
        return slots

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
            print(data)
            dispatcher.utter_message(text=" I hope this helps you out ")
            dispatcher.utter_message(json_message={"payload":"symptom","data":data})
        except:
            dispatcher.utter_message(text="Sorry couldn't find the data for the given symptom.")

class ActionUpload(Action):

    def name(self):
        return "action_upload"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(json_message={"payload":"fileupload"})

class EHRForm(FormAction):

    def name(self):
        return "ehr_form"

    @staticmethod
    def required_slots(tracker):
        return["age", "excercise", "height", "smoking", "weight", "bp", "filedesc"]#, "filedesc"

    def slot_mappings(self):

        return {
            "age": [self.from_entity(entity="age"),
                                    self.from_text()],
            "excercise": [self.from_entity(entity="excercise"), 
                                    self.from_text()],
            "height": [self.from_entity(entity="height"),
                         self.from_text()],
            "smoking": [self.from_entity(entity="smoking"),
                                    self.from_text()],
            "weight": [self.from_entity(entity="weight"),
                         self.from_text()],
            "bp": [self.from_entity(entity="bp"),
                         self.from_text()],
            "filedesc": [self.from_text()]
        }

    @staticmethod 
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def validate_height(self, value,  dispatcher, tracker, domain):
        """Validate num_people value."""

        if self.is_float(value) and float(value) > 0 and float(value) < 8.50 :
            return {"height": value}
        else:
            dispatcher.utter_message(template="utter_wrong_height")
            # validation failed, set slot to None
            return {"height": None}

    def validate_weight(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip())):
            dispatcher.utter_message(text=" Kindly fill in your proper weight")
            return{"weight":None}
        else:
            return{"weight":value}
    
    def validate_filedesc(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip()) or value==None):
            dispatcher.utter_message(text=" Kindly fill in your proper file description")
            return{"filedesc":None}
        else:
            return{"filedesc":value}

    def validate_age(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip())):
            dispatcher.utter_message(text=" Kindly fill in your proper age ")
            return{"age":None}
        else:
            return{"age":value}

    def validate_bp(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip())):
            dispatcher.utter_message(text=" Kindly fill in your proper blood pressure in the given format ")
            return{"bp":None}
        else:
            return{"bp":value}

    def validate_smoking(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip())):
            dispatcher.utter_message(text=" Kindly fill in your proper smoking details")
            return{"smoking":None}
        else:
            return{"smoking":value}

    def validate_excercise(self, value,  dispatcher, tracker, domain):
        if(not (value and value.strip())):
            dispatcher.utter_message(text=" Kindly fill in your proper excercise details")
            return{"excercise":None}
        else:
            return{"excercise":value}

    def submit(self, dispatcher, tracker, domain ):
        # dispatcher.utter_message(template="utter_ask_confirm")
        # dispatcher.utter_message(template="utter_ask_conform")
        # slot_to_fill = tracker.get_slot('conform')
        # print(slot_to_fill)
        # if slot_to_fill == "Yes" :
        #     dispatcher.utter_message(template="utter_submit")
        #     return []
        # else :
        #     return[self.deactivate()]
        # dispatcher.utter_message(template="utter_submit")
        return[]

class FileForm(FormAction):

    def name(self):
        return "file_form"

    @staticmethod
    def required_slots(tracker):
        return["filedesc"]

    def slot_mappings(self):

        return {
            "filedesc": [self.from_text()]
        }

    def validate_filedesc(self, value,  dispatcher, tracker, domain):
        if (not (value and value.strip()) or value==None):
            dispatcher.utter_message(text=" File description cannot be empty ")
            return{"filedesc":None}
        else:
            return{"filedesc":value}

    def submit(self, dispatcher, tracker, domain ):
        #dispatcher.utter_message(template="utter_submit")
        dispatcher.utter_message(template="utter_ask_file")
        return []

class ActionSetFile(Action):

    def name(self):
        return "action_set_file"

    def run(self, dispatcher, tracker, domain):
        file = tracker.latest_message['text']
        print(type(file))
        buttons = []
        buttons.append({"payload": "/conform_yes", "title":"Do you want to submit?"})
        buttons.append({"payload": "/conform_no", "title":"Do you want to reject?"})
        dispatcher.utter_message(text="Choose Option", buttons=buttons)
        file = file.encode('ascii')
        file = base64.b64decode(file)
        file = encrypt(file, "key")
        url = ipfs_add(file)
        return [SlotSet(key='file', value=url)]

class ActionBigChain(Action):

    def name(self):
        return "action_bigchaindb"

    def run(self, dispatcher, tracker, domain):
        conform = tracker.get_slot('conform')
        print(conform)
        dispatcher.utter_message(text="You have entered the bigchaindb part")  


# class ActionSessionStart(Action):
#     def name(self):
#         return "action_session_start"

#     @staticmethod
#     def fetch_slots(tracker):
#         slots = []
#         for key in ("name", "username", "password", "age", "height", "weight"):
#             value = tracker.get_slot(key)
#             if value is not None:
#                 slots.append(SlotSet(key=key, value=value))
#         return slots

#     def run(self, dispatcher, tracker, domain):
#         print("Inside session started.....")
#         events = [SessionStarted()]
#         events.extend(self.fetch_slots(tracker))
#         events.append(FollowupAction("action_listen"))
#         name = tracker.get_slot("name")
#         print("Events are....",name,  events)
#         dispatcher.utter_message(f"Hello {name}, how is the day treating you !!")
#         return events




