from pymongo import MongoClient
from modules.utils import *
from modules.diagnose import encode_symptom, create_illness_vector, get_diagnosis
from modules.config import * 
import dateparser as ddp
import os, requests, base64, uuid, random
from os import environ
from sys import getsizeof
from datetime import datetime, date, time, timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType, SessionStarted, ActionExecuted, FollowupAction, BotUttered, Form, EventType, Restarted
from rasa_sdk.forms import FormAction
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
from rasa_sdk.knowledge_base.actions import ActionQueryKnowledgeBase
import random
from rasa_sdk.knowledge_base.utils import (
    SLOT_OBJECT_TYPE,
    SLOT_LAST_OBJECT_TYPE,
    SLOT_ATTRIBUTE,
    reset_attribute_slots,
    SLOT_MENTION,
    SLOT_LAST_OBJECT,
    SLOT_LISTED_OBJECTS,
    get_object_name,
    get_attribute_slots,
)
from rasa_sdk import utils
from typing import Text, Callable, Dict, List, Any, Optional
from rasa_sdk.knowledge_base.storage import KnowledgeBase
from py2neo import Graph,Node,Relationship
import pandas as pd

client = MongoClient(MONGODB_STRING)

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

p = 'data/medical/lookup/Diseases.txt'
disease_names = [i.strip() for i in open(p, 'r', encoding='UTF-8').readlines()]
# default neo4j account should be user="neo4j", password="neo4j"
try:
    graph = Graph(host="127.0.0.1", http_port=7474, user="neo4j", password="myneo")
except Exception as e:
    logger.error('Neo4j connection error: {}, check your Neo4j'.format(e))
    sys.exit(-1)
else:
    logger.debug('Neo4j Database connected successfully.')


def retrieve_disease_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    pattern = re.compile(name)
    for i in disease_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names


def make_button(title, payload):
    return {'title': title, 'payload': payload}


class ActionEcho(Action):
    def name(self) -> Text:
        return "action_echo"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        user_say = "You said: " + tracker.latest_message['text']
        dispatcher.utter_message(user_say)
        return []


class ActionFirst(Action):
    def name(self) -> Text:
        return "action_first"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # dispatcher.utter_template("utter_first", tracker)
        # print('ActionFirst'*10)
        dispatcher.utter_message(template="utter_first")
        # dispatcher.utter_template("utter_howcanhelp", tracker)
        # print('dispatcher.utter_message')
        dispatcher.utter_message(md("您可以这样向我提问: <br/>头痛怎么办<br/>\
                              什么人容易头痛<br/>\
                              头痛吃什么药<br/>\
                              头痛能治吗<br/>\
                              头痛属于什么科<br/>\
                              头孢地尼分散片用途<br/>\
                              如何防止头痛<br/>\
                              头痛要治多久<br/>\
                              糖尿病有什么并发症<br/>\
                              糖尿病有什么症状"))
        return []


class ActionDonKnow(Action):
    def name(self) -> Text:
        return "action_donknow"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        # dispatcher.utter_template("utter_donknow", tracker)
        dispatcher.utter_message(template="utter_donknow")
        # dispatcher.utter_template("utter_howcanhelp", tracker)
        dispatcher.utter_message(md("您可以这样向我提问: <br/>头痛怎么办<br/>\
                                      什么人容易头痛<br/>\
                                      头痛吃什么药<br/>\
                                      头痛能治吗<br/>\
                                      头痛属于什么科<br/>\
                                      头孢地尼分散片用途<br/>\
                                      如何防止头痛<br/>\
                                      头痛要治多久<br/>\
                                      糖尿病有什么并发症<br/>\
                                      糖尿病有什么症状"))
        return []


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
        # if len(possible_diseases) == 1 or sure == "true":
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
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 疾病相关的记录".format(disease))
        return []


class ActionSearchFood(Action):
    def name(self) -> Text:
        return "action_search_food"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        """ search_food db action here """
        food = dict()
        if disease == pre_disease or len(possible_diseases) == 1:
            m = [x['m.name'] for x in graph.run("match (a:Disease{name: {disease}})-[:can_eat]->(m:Food) return m.name",
                          disease=disease).data()]
            food['can_eat'] = "、".join(m) if m else "暂无记录"

            m = [x['m.name'] for x in graph.run("match (a:Disease{name: {disease}})-[:not_eat]->(m:Food) return m.name",
                          disease=disease).data()]

            food['not_eat'] = "、".join(m) if m else "暂无记录"

            retmsg = "在患 {0} 期间，可以食用：{1}，\n但不推荐食用：{2}".\
                            format(disease, food['can_eat'], food['not_eat'])

            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_food{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的饮食记录".format(disease))
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
            a = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: {disease}})-[r:has_symptom]->\
                                                (s:Symptom) RETURN s.name", disease=disease).data()]
            template = "{0}的症状可能有：{1}"
            retmsg = template.format(disease, "、".join(a))
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_symptom{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的症状记录".format(disease))

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
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的原因记录".format(disease))
        return []


class ActionSearchNeopathy(Action):
    def name(self) -> Text:
        return "action_search_neopathy"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: {disease}})-[r:has_neopathy]->\
                                                (s:Disease) RETURN s.name", disease=disease).data()]
            template = "{0}的并发症可能有：{1}"
            retmsg = template.format(disease, "、".join(a))
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_neopathy{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的并发症记录".format(disease))
        return []


class ActionSearchDrug(Action):
    def name(self) -> Text:
        return "action_search_drug"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: {disease}})-[r:can_use_drug]->\
                                                (s:Drug) RETURN s.name", disease=disease).data()]
            if a:
                template = "在患 {0} 时，可能会用药：{1}"
                retmsg = template.format(disease, "、".join(a))
            else:
                retmsg = "无 %s 的可能用药记录" % disease
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_drug{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的用药记录".format(disease))
        return []


class ActionSearchPrevention(Action):
    def name(self) -> Text:
        return "action_search_prevention"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        disease = tracker.get_slot("disease")
        pre_disease = tracker.get_slot("sure")
        print("pre_disease::::" + str(pre_disease))
        
        possible_diseases = retrieve_disease_name(disease)
        if disease == pre_disease or len(possible_diseases) == 1:
            a = graph.run("match (a:Disease{name: {disease}}) return a.prevent", disease=disease).data()[0]
            if 'a.prevent' in a:
                prevent = a['a.prevent']
                template = "以下是有关预防 {0} 的知识：{1}"
                retmsg = template.format(disease, md(prevent.replace('\n', '<br/>')))
            else:
                retmsg = disease + "暂无常见预防方法"
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_prevention{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的预防记录".format(disease))
        return []


class ActionSearchDrugFunc(Action):
    def name(self) -> Text:
        return "action_search_drug_func"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]):
        drug = tracker.get_slot("drug")
        if drug:
            a = [x['n.name'] for x in graph.run("match (n:Disease)-[:can_use_drug]->(a:Drug{name: {drug}})"
                                                "return n.name", drug=drug).data()]
            template = "{0} 可用于治疗疾病：{1}"
            retmsg = template.format(drug, "、".join(a))
        else:
            retmsg = drug + " 在疾病库中暂无可治疗的疾病"
        dispatcher.utter_message(retmsg)
        return []


class ActionSearchDiseaseTreatTime(Action):
    def name(self) -> Text:
        return "action_search_disease_treat_time" # treat_period

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
            if "treat_period" in a:
                treat_period = a['treat_period']
                template = "{0}需要的治疗时间：{1}"
                retmsg = template.format(disease, treat_period)
            else:
                retmsg = disease + "暂无治疗时间的记录"
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_disease_treat_time{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的治疗时间记录".format(disease))
        return []


class ActionSearchEasyGet(Action):
    def name(self) -> Text:
        return "action_search_easy_get"

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
            easy_get = a['easy_get']
            template = "{0}的易感人群是：{1}"
            retmsg = template.format(disease, easy_get)
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_easy_get{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 相关的易感人群记录".format(disease))
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
            a = graph.run("match (a:Disease{name: {disease}})-[:belongs_to]->(s:Department) return s.name",
                          disease=disease).data()[0]['s.name']
            template = "{0} 属于 {1}"
            retmsg = template.format(disease, a)
            dispatcher.utter_message(retmsg)
        elif len(possible_diseases) > 1:
            buttons = []
            for d in possible_diseases:
                buttons.append(make_button(d, '/search_disease_dept{{"disease":"{0}", "sure":"{1}"}}'.format(d, d)))
            dispatcher.utter_button_message("请点击选择想查询的疾病，若没有想要的，请忽略此消息", buttons)
        else:
            dispatcher.utter_message("知识库中暂无与 {0} 疾病相关的科室记录".format(disease))
        return []


