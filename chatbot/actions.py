import logging
logger = logging.getLogger(__name__)
import secrets
import json
from rasa_core_sdk import Action, Tracker
from rasa_core_sdk.events import SlotSet, Restarted, UserUtteranceReverted, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
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
        return 'action_get_song'

    def run(self, dispatcher, tracker, domain):
        logger.debug()
        emotion = next(tracker.get_latest_entity_values("emotion"), None)
        print(emotion)
        if not emotion:
            dispatcher.utter_message("I couldnt contemplate what you are going thorugh. I'm sorry.")
            return [UserUtteranceReverted()]
        query = secrets.choice(data[emotion])
        url = get_url(query)
        dispatcher.utter_message("Here is something for your mood.")
        dispatcher.utter_custom_json({"payload":"video","data":url})

            

	

		
# class ActionSlotReset(Action): 	
#     def name(self): 		
#         return 'action_slot_reset' 	
#     def run(self, dispatcher, tracker, domain): 		
#         return[AllSlotsReset()]
		
