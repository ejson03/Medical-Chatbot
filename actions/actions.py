from pymongo import MongoClient

from modules.utils import *
from modules.diagnose import encode_symptom, create_illness_vector, get_diagnosis
from modules.config import * 
import os, requests, base64, uuid, random
from os import environ
from sys import getsizeof
from datetime import datetime, date, time, timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType, SessionStarted, ActionExecuted, FollowupAction, BotUttered, Form, EventType, Restarted
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, Callable, Dict, List, Any, Optional
from py2neo import Graph,Node,Relationship
import pandas as pd

client = MongoClient(MONGODB_STRING)
disease_file = './assets/disease.txt'
disease_names = [i.strip() for i in open(disease_file, 'r', encoding='UTF-8').readlines()]

try:
    graph = Graph(
            host=NEO4J_STRING,
            http_port=7474,
            user=NEO4J_USERNAME,
            password= NEO4J_PASSWORD)
except Exception as e:
    import sys
    sys.exit(-1)


def retrieve_disease_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    import re
    pattern = re.compile(name)
    for i in disease_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names


def make_button(title, payload):
    return {'title': title, 'payload': payload}

class ActionRestart(Action):
    def name(self):
        return "action_restart"

    async def run(self,dispatcher, tracker, domain):
        return [Restarted(), FollowupAction("action_session_start")]

class ActionSessionStart(Action):
    def name(self):
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(tracker):
        return [
            SlotSet(key=event.get("name"), value=event.get("value"),)
            for event in tracker.events
            if event.get("event") == "slot"
        ]

    async def run(self,dispatcher, tracker, domain):
        events = [SessionStarted()]
        events.extend(self._slot_set_events_from_tracker(tracker))
        username = tracker.get_slot('name') if tracker.get_slot("name") else tracker.current_state()["sender_id"]    
        dispatcher.utter_message(text=f"Hello {username}")
        events.append(ActionExecuted("action_listen"))
        return events

class ResetSlot(Action):

    def name(self):
        return "action_reset_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('filedesc', None)]


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
            dispatcher.utter_message("I couldn't contemplate what you are going thorugh. I'm sorry.")

class ActionGetQuote(Action):
    def name(self):
        return "action_get_quote"

    def run(self, dispatcher, tracker, domain):
        image = get_quotes()
        dispatcher.utter_message(image=image)

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
        base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
        location = tracker.get_slot('location')
        Final_url = base_url + "app_id=" + WEATHER_ID + "&app_code=" + WEATHER_KEY + "&product=observation&name=" + location 
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
        base_url = "https://weather.api.here.com/weather/1.0/report.json?" 
 
        location = tracker.get_slot('location')
        Final_url = base_url + "app_id=" + WEATHER_ID + "&app_code=" + WEATHER_KEY + "&product=observation&name=" + location 
 
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

class ActionSearchTreat(Action):
    def name(self) -> Text:
        return "action_search_treat"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = graph.run("match (a:Disease{name: {disease}}) return a", disease=disease).data()[0]['a']
            if "intro" in a:
                intro = a['intro']
                template = "{0}的简介：{1}"
                retmsg = template.format(disease, intro)
            else:
                retmsg = disease + "暂无简介"
            dispatcher.utter_message(retmsg)
            if "treat" in a:
                treat = a['treat']
                template = "{0}的治疗方式有：{1}"
                retmsg = template.format(disease, "、".join(treat))
            else:
                retmsg = disease + "暂无常见治疗方式"
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_treat{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("Please click to select the disease you want to inquire, if there is nothing you want, please ignore this message", buttons)
        else:
            dispatcher.utter_message("Nothing in the knowledge base {0}".format(disease))
        return []

class ActionSearchSymptom(Action):
    def name(self) -> Text:
        return "action_search_symptom"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            retmsg = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: {disease}})-[r:has_symptom]->\
                                                (s:Symptom) RETURN s.name", disease=disease).data()]
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_symptom{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("Please click to select the disease you want to inquire, if there is nothing you want, please ignore this message", buttons)
        else:
            dispatcher.utter_message("Nothing in the knowledge base {0} 相关的症状记录".format(disease))

        return []


class ActionSearchCause(Action):
    def name(self) -> Text:
        return "action_search_cause"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = graph.run("match (a:Disease{name: {disease}}) return a.cause", disease=disease).data()[0]['a.cause']
            if "treat" in a:
                treat = a['treat']
                template = "{0}的治疗方式有：{1}"
                retmsg = template.format(disease, "、".join(treat))
            else:
                retmsg = disease + "暂无该疾病的病因的记录"
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_cause{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("Please click to select the disease you want to inquire, if there is nothing you want, please ignore this message", buttons)
        else:
            dispatcher.utter_message("Nothing in the knowledge base {0} 相关的原因记录".format(disease))
        return []


class ActionSearchDiseaseDept(Action):
    def name(self) -> Text:
        return "action_search_disease_dept"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            result = graph.run("match (a:Disease{name: {disease}})-[:belongs_to]->(s:Department) return s.name",
                          disease=disease).data()[0]['s.name']
            template = f"{disease} belongs {result}"
            dispatcher.utter_message(text = template)

        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_disease_dept{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("Please click to select the disease you want to inquire,if there is nothing you want, please ignore this message", buttons)
        else:
            dispatcher.utter_message("Nothing in the knowledge base {0} Disease-related department records".format(disease))
        return []


