import os
import json,requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
CONNECTION_STRING = "mongodb://localhost:27017"#os.getenv("MONGODB_STRING")
client = MongoClient(CONNECTION_STRING)

if 'analysis' not in client.list_database_names():
    _ = client['analysis'] 


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


class User:
    def __init__(self, user):
        analysisDB = getAnalysisDB()
        rasaDB = getRASADB()
        self.name = user
        self.conversation = getCollectionConversation(rasaDB)
        self.analysis = getCollectionUsers(analysisDB)
        self.date = datetime.now()

    def weeklyReport(self, date):
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
    
          
        
    

        

    
