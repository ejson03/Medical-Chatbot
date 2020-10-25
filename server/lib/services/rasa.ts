import { MongoClient } from 'mongodb';

import fetch from 'node-fetch';
import https from 'https';
import * as config from '../config';

export const RASARequest = async (message: unknown, sender: string, metadata?: string) => {
   let data: any;
   if (metadata) {
      data = { message: message, sender: sender, metadata: metadata };
   } else {
      data = { message: message, sender: sender };
   }
   const httpsAgent = new https.Agent({
      rejectUnauthorized: false
   });
   const response = await fetch(`${config.RASA_URL}/webhooks/rest/webhook`, {
      method: 'POST',
      body: JSON.stringify(data),
      agent: httpsAgent
   });
   return await response.json();
};

export const getRasaHistory = async (username: string) => {
   const db = await MongoClient.connect(config.MONGO_URL);
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
};
