import json, logging, pickle, typing
from typing import Iterator, Optional, Text, Iterable, Union, Dict
import itertools
import traceback
from time import sleep
from rasa.core.brokers.event_channel import EventChannel
from rasa.core.trackers import ActionExecuted, DialogueStateTracker, EventVerbosity
from rasa.core.tracker_store import TrackerStore
from rasa.core.domain import Domain
from rasa.core.events import SessionStarted
from datetime import datetime
from termcolor import colored
import inspect


class GridTrackerStore(TrackerStore):

    def __init__(
        self,
        domain,
        host = "mongodb://localhost:27017",
        db = "rasa",
        username = None,
        password = None,
        auth_source = "admin",
        collection="conversations",
        event_broker=None,
    ):
        from pymongo.database import Database
        from pymongo import MongoClient

        self.client = MongoClient(
            host,
            username=username,
            password=password,
            authSource=auth_source,
            connect=False,
        )

        self.db = Database(self.client, db)
        self.collection = collection
        self.today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        super().__init__(domain, event_broker)

        self._ensure_indices()

    @property
    def conversations(self):
        return self.db[self.collection]

    def _ensure_indices(self):
        self.conversations.create_index("sender_id")

    @staticmethod
    def _current_tracker_state_without_events(tracker):
        state = tracker.current_state(EventVerbosity.ALL)
        state.pop("events", None)
        return state

    def save(self, tracker, timeout=None):
        if self.event_broker:
            self.stream_events(tracker)

        self.conversations.update_one(
            {"sender_id":tracker.sender_id, "col":"1"}, 
            {"$set": self._current_tracker_state_without_events(tracker)}, 
            upsert=True
        )

        additional_events = self._additional_events(tracker)
        printable = [e.as_dict() for e in additional_events]
        status = self.conversations.update_one(
            {"sender_id": tracker.sender_id, "col": self.today},
            {
                "$set": {"col" : self.today},
                "$push": {
                    "events": {"$each": printable}
                },
            },
            upsert=True
        )
        # additional_events = self._additional_events(tracker)

        # self.conversations.update_one(
        #     {"sender_id": tracker.sender_id},
        #     {
        #         "$set": self._current_tracker_state_without_events(tracker),
        #         "$push": {
        #             "events": {"$each": [e.as_dict() for e in additional_events]}
        #         },
        #     },
        #     upsert=True,
        # )

    def _additional_events(self, tracker):

        stored = self.conversations.find_one( {"sender_id": tracker.sender_id, "col": self.today}) or {}
        # stored = self.conversations.find_one({"sender_id": tracker.sender_id}) or {}
        number_events_since_last_session = len(
            self._events_since_last_session_start(stored)
        )

        return itertools.islice(
            tracker.events, number_events_since_last_session, len(tracker.events)
        )

    @staticmethod
    def _events_since_last_session_start(serialised_tracker):
        events = []
        for event in reversed(serialised_tracker.get("events", [])):
            events.append(event)
            if event["event"] == SessionStarted.type_name:
                break
        return list(reversed(events))

    def retrieve(self, sender_id):
 
        stored = self.conversations.find_one({"sender_id": sender_id, "col": self.today})
        # stored = self.conversations.find_one({"sender_id": sender_id, "col": "1"})

        # look for conversations which have used an `int` sender_id in the past
        # and update them.
        if stored is None and sender_id.isdigit():
            from pymongo import ReturnDocument

            stored = self.conversations.find_one_and_update(
                {"sender_id": int(sender_id)},
                {"$set": {"sender_id": str(sender_id)}},
                return_document=ReturnDocument.AFTER,
            )

        # if stored is None:
        #     stored = self.conversations.find_one({"sender_id": sender_id, "col": "1"})

        if stored is not None:
            events = self._events_since_last_session_start(stored)
            return DialogueStateTracker.from_dict(sender_id, events, self.domain.slots)
        else:
            return None

    def keys(self):
        """Returns sender_ids of the Mongo Tracker Store"""
        return [c["sender_id"] for c in self.conversations.find()]
         
    


