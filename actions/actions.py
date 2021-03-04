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

class MyKB(KnowledgeBase):

    async def get_attributes_of_object(self, object_type: Text) -> List[Text]:
        """
        Returns a list of all attributes that belong to the provided object type.
        Args:
            object_type: the object type
        Returns: list of attributes of object_type
        """
        print("Get Attributes Called")    
        print("OBJECT TYPE=", object_type)
  
        object_type = object_type.title()
        graph = Graph(
            host=NEO4J_STRING,
            http_port=7474,
            user=NEO4J_USERNAME,
            password= NEO4J_PASSWORD)
        hotels = list(graph.run("MATCH (r:{}) RETURN r".format(object_type)))
        # hotels = list(graph.run("MATCH (r:{} {name: {}}) RETURN r".format(object_type, object_identifier)))
        extracted_hotels = []
        for index, hotel in enumerate(hotels):
            extracted_hotels.append(list(hotels[index])[0])
           
        first_object = extracted_hotels[0]
        print("EXTRACTED IN GET ATTRIBUTES = {}".format(list(first_object.keys()) ))
        return list(first_object.keys())    
    
    async def get_objects(
        self, object_type: Text, attributes: List[Dict[Text, Text]], limit: int = 5
    ) -> List[Dict[Text, Any]]:
        """
        Query the knowledge base for objects of the given type. Restrict the objects
        by the provided attributes, if any attributes are given.
        Args:
            object_type: the object type
            attributes: list of attributes
            limit: maximum number of objects to return
        Returns: list of objects
        """
        
        for attribute in attributes:
            attribute['value'] = "'{}'".format(attribute['value'].title()) 
                
        print("OBJECT TYPE in GET OBJECTS={}, ATTRIBUTES={}".format(object_type, attributes))
        object_type = object_type.title()
        graph = Graph(
            host=NEO4J_STRING,
            http_port=7474,
            user=NEO4J_USERNAME,
            password= NEO4J_PASSWORD)
        hotels = list(graph.run("MATCH (r:{}) RETURN r".format(object_type)))
        extracted_hotels = []
        for index, hotel in enumerate(hotels):
            extracted_hotels.append(list(hotels[index])[0])
            
        objects = extracted_hotels 
        print("ALL EXTRACTED Objects={}".format(objects))
        # filter objects by attributes
        if attributes:
            objects = list(
                filter(
                    lambda obj: [
                        obj[a["name"]] == a["value"] for a in attributes
                    ].count(False)
                    == 0,
                    objects,
                )
            )

        random.shuffle(objects)

        return objects[:limit]

        

    async def get_object(
        self, object_type: Text, object_identifier: Text
    ) -> Dict[Text, Any]:
        """
        Returns the object of the given type that matches the given object identifier.
        Args:
            object_type: the object type
            object_identifier: value of the key attribute or the string
            representation of the object
        Returns: the object of interest
        """
        object_type = object_type.title()
        graph = Graph(NEO4J_STRING, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        hotels = list(graph.run("MATCH (r:{}) RETURN r".format(object_type)))
        # hotels = list(graph.run("MATCH (r:{} {name: {}}) RETURN r".format(object_type, object_identifier)))
        extracted_hotels = []
        for index, hotel in enumerate(hotels):
            extracted_hotels.append(list(hotels[index])[0])
            
            
        if utils.is_coroutine_action(self.get_key_attribute_of_object):
            key_attribute = await self.get_key_attribute_of_object(object_type)
        else:
            key_attribute = self.get_key_attribute_of_object(object_type)
        
        objects = extracted_hotels 

        # filter the objects by its key attribute, for example, 'id'
        objects_of_interest = list(
            filter(
                lambda obj: str(obj[key_attribute]).lower()
                == str(object_identifier).lower(),
                objects,
            )
        )    
        
        # if the object was referred to directly, we need to compare the representation
        # of each object with the given object identifier
        if not objects_of_interest:
            if utils.is_coroutine_action(self.get_representation_function_of_object):
                repr_function = await self.get_representation_function_of_object(
                    object_type
                )
            else:
                repr_function = self.get_representation_function_of_object(object_type)

            objects_of_interest = list(
                filter(
                    lambda obj: str(object_identifier).lower()
                    in str(repr_function(obj)).lower(),
                    objects,
                )
            )
        object_dict = {}
        print("Object of Interest={}".format(objects_of_interest[0]['name']))    
        print("Get Object Called with IDENTIFIER={} and Key Attribute={}".format(object_identifier, key_attribute))
        for key, value in  objects_of_interest[0].items():
            object_dict[key] = value
        return object_dict
    

    
class ActionMyKB(ActionQueryKnowledgeBase):
    def __init__(self):
        # load knowledge base with data from the given file
        # knowledge_base = InMemoryKnowledgeBase("knowledge_base_data.json")
        knowledge_base = MyKB()

        # print("Noman")
        # knowledge_base.set_representation_function_of_object(
        #     "hotel", lambda obj: obj["name"] + " (" + obj["city"] + ")"
        # )

        super().__init__(knowledge_base)
        
        
    async def utter_objects(
        self,
        dispatcher: CollectingDispatcher,
        object_type: Text,
        objects: List[Dict[Text, Any]],
    ) -> None:
        """
        Utters a response to the user that lists all found objects.
        Args:
            dispatcher: the dispatcher
            object_type: the object type
            objects: the list of objects
        """
        if objects:
            dispatcher.utter_message(
                text=f"Found the following objects of type '{object_type}':"
            )

            if utils.is_coroutine_action(
                self.knowledge_base.get_representation_function_of_object
            ):
                repr_function = (
                    await self.knowledge_base.get_representation_function_of_object(
                        object_type
                    )
                )
            else:
                repr_function = (
                    self.knowledge_base.get_representation_function_of_object(
                        object_type
                    )
                )

            for i, obj in enumerate(objects, 1):
                dispatcher.utter_message(text=f"{i}: {repr_function(obj)}")
            # print("List of Hotels: /n {}".format(objects))    
            # dispatcher.utter_message("List of Hotels: /n {}".format(objects))
        else:
            dispatcher.utter_message(
                text=f"I could not find any objects of type '{object_type}'."
            )
    
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """
        Executes this action. If the user ask a question about an attribute,
        the knowledge base is queried for that attribute. Otherwise, if no
        attribute was detected in the request or the user is talking about a new
        object type, multiple objects of the requested type are returned from the
        knowledge base.

        Args:
            dispatcher: the dispatcher
            tracker: the tracker
            domain: the domain

        Returns: list of slots

        """
        print("\n\n SLOT_OBJECT_TYPE={}".format(SLOT_OBJECT_TYPE))
        object_type = tracker.get_slot(SLOT_OBJECT_TYPE)
        last_object_type = tracker.get_slot(SLOT_LAST_OBJECT_TYPE)
        attribute = tracker.get_slot(SLOT_ATTRIBUTE)

        new_request = object_type != last_object_type
        
        print("Object Type={}, Attribute={} in Run".format(object_type, attribute))
        
        if not object_type:
            # object type always needs to be set as this is needed to query the
            # knowledge base
            dispatcher.utter_message(template="utter_ask_rephrase")
            return []

        if not attribute or new_request:
            print("Going to call _query_objects in Run")
            return await self._query_objects(dispatcher, tracker)
        elif attribute:
            print("Going to call _query_attribute in Run")
            # logger.debug("Going to call _query_attribute in Run")
            return await self._query_attribute(dispatcher, tracker)

        print("Going to dispatch Utter Rephrase in Run")
        logger.debug("Going to dispatch Utter Rephrase in Run")
        dispatcher.utter_message(template="utter_ask_rephrase")
        return []

    async def _query_objects(
        self, dispatcher: CollectingDispatcher, tracker: Tracker
    ) -> List[Dict]:
        """
        Queries the knowledge base for objects of the requested object type and
        outputs those to the user. The objects are filtered by any attribute the
        user mentioned in the request.

        Args:
            dispatcher: the dispatcher
            tracker: the tracker

        Returns: list of slots
        """
        object_type = tracker.get_slot(SLOT_OBJECT_TYPE)
        if utils.is_coroutine_action(self.knowledge_base.get_attributes_of_object):
            object_attributes = await self.knowledge_base.get_attributes_of_object(
                object_type
            )
        else:
            object_attributes = self.knowledge_base.get_attributes_of_object(
                object_type
            )

        # get all set attribute slots of the object type to be able to filter the
        # list of objects
        attributes = get_attribute_slots(tracker, object_attributes)
        # query the knowledge base
        if utils.is_coroutine_action(self.knowledge_base.get_objects):
            objects = await self.knowledge_base.get_objects(object_type, attributes)
        else:
            objects = self.knowledge_base.get_objects(object_type, attributes)

        if utils.is_coroutine_action(self.utter_objects):
            await self.utter_objects(dispatcher, object_type, objects)  # type: ignore
        else:
            self.utter_objects(dispatcher, object_type, objects)

        if not objects:
            return reset_attribute_slots(tracker, object_attributes)

        if utils.is_coroutine_action(self.knowledge_base.get_key_attribute_of_object):
            key_attribute = await self.knowledge_base.get_key_attribute_of_object(
                object_type
            )
        else:
            key_attribute = self.knowledge_base.get_key_attribute_of_object(object_type)

        last_object = None if len(objects) > 1 else objects[0][key_attribute]

        slots = [
            SlotSet(SLOT_OBJECT_TYPE, object_type),
            SlotSet(SLOT_MENTION, None),
            SlotSet(SLOT_ATTRIBUTE, None),
            SlotSet(SLOT_LAST_OBJECT, last_object),
            SlotSet(SLOT_LAST_OBJECT_TYPE, object_type),
            SlotSet(
                SLOT_LISTED_OBJECTS, list(map(lambda e: e[key_attribute], objects))
            ),
        ]

        return slots + reset_attribute_slots(tracker, object_attributes)
    
    
    async def _query_attribute(
        self, dispatcher: CollectingDispatcher, tracker: Tracker
    ) -> List[Dict]:
        """
        Queries the knowledge base for the value of the requested attribute of the
        mentioned object and outputs it to the user.

        Args:
            dispatcher: the dispatcher
            tracker: the tracker

        Returns: list of slots
        """
        object_type = tracker.get_slot(SLOT_OBJECT_TYPE)
        attribute = tracker.get_slot(SLOT_ATTRIBUTE)

        object_name = get_object_name(
            tracker,
            self.knowledge_base.ordinal_mention_mapping,
            self.use_last_object_mention,
        )
        print("Object Name={}, Attribute={} in Query Attribute".format(object_name, attribute))
        
        if not object_name or not attribute:
            print("CASE 1")
            dispatcher.utter_message(template="utter_ask_rephrase")
            return [SlotSet(SLOT_MENTION, None)]

        if utils.is_coroutine_action(self.knowledge_base.get_object):
            print("Calling get_object in Query Attributes If")
            object_of_interest = await self.knowledge_base.get_object(
                object_type, object_name  # type: ignore
            )
        else:
            print("Calling get_object in Query Attributes Else")
            object_of_interest = self.knowledge_base.get_object(
                object_type, object_name
            )
        print("Object of Interest={}".format(object_of_interest))
        attribute = attribute.replace("-", "_")
        if not object_of_interest or attribute not in object_of_interest:
            print("CASE 0")
            dispatcher.utter_message(template="utter_ask_rephrase")
            return [SlotSet(SLOT_MENTION, None)]

        value = object_of_interest[attribute]
        print("VALUE of ATTRIBUTE={}".format(value))
        if utils.is_coroutine_action(
            self.knowledge_base.get_representation_function_of_object
        ):
            repr_function = await self.knowledge_base.get_representation_function_of_object(
                object_type  # type: ignore
            )
        else:
            repr_function = self.knowledge_base.get_representation_function_of_object(
                object_type
            )
        object_representation = repr_function(object_of_interest)
        if utils.is_coroutine_action(self.knowledge_base.get_key_attribute_of_object):
            key_attribute = await self.knowledge_base.get_key_attribute_of_object(
                object_type
            )
        else:
            key_attribute = self.knowledge_base.get_key_attribute_of_object(object_type)
        object_identifier = object_of_interest[key_attribute]

        if utils.is_coroutine_action(self.utter_attribute_value):
            await self.utter_attribute_value(
                dispatcher, object_representation, attribute, value  # type: ignore
            )
        else:
            self.utter_attribute_value(
                dispatcher, object_representation, attribute, value
            )

        slots = [
            SlotSet(SLOT_OBJECT_TYPE, object_type),
            SlotSet(SLOT_ATTRIBUTE, None),
            SlotSet(SLOT_MENTION, None),
            SlotSet(SLOT_LAST_OBJECT, object_identifier),
            SlotSet(SLOT_LAST_OBJECT_TYPE, object_type),
        ]

        return slots


