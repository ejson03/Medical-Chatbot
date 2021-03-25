import json
import logging
import pickle
import typing
from typing import Iterator, Optional, Text, Iterable, Union, Dict, List
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
import os
from . import Tracker4J


class GridTrackerStore(TrackerStore):
    def __init__(
        self,
        domain,
        host=os.environ.get("MONGO_URL") or "mongodb://mongodb:27017",
        db="rasa",
        username=None,
        password=None,
        auth_source="admin",
        collection="conversations",
        neo4j_url="bolt://localhost:7687",
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

        self.Tracker4J = Tracker4J.Tracker4J(neo4j_url)

        self.db = Database(self.client, db)
        self.collection = collection
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

        additional_events = self._additional_events(tracker)
        sender_id = tracker.sender_id
        events = tracker.current_state(EventVerbosity.ALL)["events"]
        self.conversations.update_one(
            {"sender_id": tracker.sender_id},
            {
                "$set": self._current_tracker_state_without_events(tracker),
                "$push": {
                    "events": {"$each": [e.as_dict() for e in additional_events]}
                },
            },
            upsert=True,
        )

        try:
            self.Tracker4J.CreateNodeFromEvents(events, sender_id)
        except:
            pass

    def _additional_events(self, tracker: DialogueStateTracker) -> Iterator:
        """Return events from the tracker which aren't currently stored.

        Args:
            tracker: Tracker to inspect.

        Returns:
            List of serialised events that aren't currently stored.

        """

        stored = self.conversations.find_one({"sender_id": tracker.sender_id}) or {}
        all_events = self._events_from_serialized_tracker(stored)
        number_events_since_last_session = len(
            self._events_since_last_session_start(all_events)
        )

        return itertools.islice(
            tracker.events, number_events_since_last_session, len(tracker.events)
        )

    @staticmethod
    def _events_from_serialized_tracker(serialised: Dict) -> List[Dict]:
        return serialised.get("events", [])

    @staticmethod
    def _events_since_last_session_start(events: List[Dict]) -> List[Dict]:
        """Retrieve events since and including the latest `SessionStart` event.

        Args:
            events: All events for a conversation ID.

        Returns:
            List of serialised events since and including the latest `SessionStarted`
            event. Returns all events if no such event is found.

        """

        events_after_session_start = []
        for event in reversed(events):
            events_after_session_start.append(event)
            if event["event"] == SessionStarted.type_name:
                break

        return list(reversed(events_after_session_start))

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """
        Args:
            sender_id: the message owner ID

        Returns:
            `DialogueStateTracker`
        """
        stored = self.conversations.find_one({"sender_id": sender_id})

        # look for conversations which have used an `int` sender_id in the past
        # and update them.
        if not stored and sender_id.isdigit():
            from pymongo import ReturnDocument

            stored = self.conversations.find_one_and_update(
                {"sender_id": int(sender_id)},
                {"$set": {"sender_id": str(sender_id)}},
                return_document=ReturnDocument.AFTER,
            )

        if not stored:
            return

        events = self._events_from_serialized_tracker(stored)
        if not self.load_events_from_previous_conversation_sessions:
            events = self._events_since_last_session_start(events)

        return DialogueStateTracker.from_dict(sender_id, events, self.domain.slots)

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the Mongo Tracker Store"""
        return [c["sender_id"] for c in self.conversations.find()]
