import { MongoClient } from 'mongodb';

import fetch from 'node-fetch';
import * as config from '../config';

export const RASARequest = async (message: unknown, sender: string = 'elvis', metadata?: string) => {
   let data: any;
   if (metadata) {
      data = { message: message, sender: sender, metadata: metadata };
   } else {
      data = { message: message, sender: sender };
   }

   const response = await fetch(`${config.RASA_URL}/webhooks/rest/webhook`, {
      method: 'POST',
      body: JSON.stringify(data)
   });
   const reply = await response.json();
   if (reply) {
      return reply;
   } else {
      return {};
   }
};

export const getRasaHistory = async (username: string) => {
   const db = await MongoClient.connect(config.MONGO_URL);
   try {
      const result = await db.db('rasa').collection('conversations').findOne({ sender_id: username });

      const filteredEvents: any = [];
      let interEvents = {};
      for (const event of result.events) {
         if (event.event == 'user') {
            interEvents = {
               text: event.text,
               intent: event.parse_data.intent.name,
               entities: event.parse_data.entities,
               message_time: new Date(event.timestamp * 1000)
            };
         }
         if (event.event == 'bot') {
            interEvents = {
               ...interEvents,
               reply: event.text,
               reply_time: new Date(event.timestamp * 1000)
            };
            filteredEvents.push(interEvents);
            interEvents = {};
         }
      }
      return filteredEvents;
   } catch {
      return [];
   }
};

export const getRASACharts = async (username: string) => {
   const db = await MongoClient.connect(config.MONGO_URL);
   const result = await db.db('rasa').collection('conversations').findOne({ sender_id: username });
   const exclude = [
      'slot',
      'session_started',
      'action_session_start',
      'action_listen',
      'action_restart',
      'action',
      'bot'
   ];
   const filteredEvents: any = [];
   for (const event of result.events) {
      if (event.event == 'user' && !exclude.includes(event.name)) {
         for (const entity of event.parse_data.entities) {
            if (entity.entity === 'emotion') {
               filteredEvents.push({
                  time: new Date(event.timestamp),
                  emotion: entity.value
               });
            }
         }
      }
   }
   return filteredEvents;
};
