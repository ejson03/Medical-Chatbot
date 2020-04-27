import os
import json,requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid 
import sys
if '3.6.6' in sys.version:
    from googlesearch import search
else:
    import google

load_dotenv()
CONNECTION_STRING = os.getenv("MONGODB_STRING")
client = MongoClient(CONNECTION_STRING)

if 'analysis' not in client.list_database_names():
    _ = client['analysis'] 


def getWeb(name):
    url = search(name, tld="co.in", num=1)
    return next(url) #generator object get next value

def getRASADB():
    return client.get_database('rasa')

def getCollectionConversation(db):
    return db['conversations']

def getCollectionUsers(db):
    return db['users']

def getAnalysisDB():
    return client.get_database('analysis')


def getWeek(day):
    start = day - timedelta(days=day.weekday())
    end = start + timedelta(days=6)
    start = start.replace(hour=0, minute=0,second=0, microsecond=0).timestamp()
    end = end.replace(hour=23, minute=59,second=59, microsecond=59).timestamp()
    return start, end


def getDay(day):
    start = day.replace(hour=0, minute=0,second=0, microsecond=0).timestamp()
    end = day.replace(hour=23, minute=59,second=59, microsecond=59).timestamp()
    return start, end

def getAllUsers():
    rasaDB = getRASADB()
    conversation = getCollectionConversation(rasaDB)
    users = conversation.find()
    users = [user['sender_id'] for user in users]
    return users

class User:
    def __init__(self, user):
        analysisDB = getAnalysisDB()
        rasaDB = getRASADB()
        self.name = user
        self.conversation = getCollectionConversation(rasaDB)
        self.analysis = getCollectionUsers(analysisDB)
        self.date = datetime.now()

    def weeklyReport(self, date):
        date = datetime.strptime(date, '%Y-%m-%d')
        self.start, self.end = getWeek(date)
        query = {'sender_id': self.name} 
        user = self.conversation.find(query)
        events = user[0]['events']
        report = list(map(self.clean, events))
        report = list(filter(None, report))
        return report

    def clean(self, event):
        if event['event'] == 'user' and self.start < event['timestamp'] < self.end:
            entities= [x for x in event['parse_data']['entities'] if x['entity'] == 'emotion']
            if len(entities) >= 1 :
                return {
                    'time': event['timestamp'],
                    'emotion': entities[0]['value']
                }

    def generateStory(self):
        now = datetime.now()
        self.start, self.end = getDay(now)
        query = {'sender_id': self.name} 
        user = self.conversation.find(query)
        events = user[0]['events']
        self.file = f"## story no {uuid.uuid4()} \n"
        report = list(map(self.cleanDay, events))
        print(self.file)
        with open(f'{self.name}.md', 'w+') as f:
            f.write(self.file)

    def cleanDay(self, event):
        exclude = ["action_session_start", "action_listen", "action_restart"]
        if self.start < event['timestamp'] < self.end :
            print(event['event'])
            if event['event'] == 'user' :
                self.file += f"* {event['parse_data']['intent']['name']} \n"

            if event['event'] == 'action' and event['name'] not in exclude:
                self.file += f"\t - {event['name']} \n"
        return 1


    
          
        
    

        

    
