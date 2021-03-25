from py2neo import Graph, Node, NodeMatcher, matching, Schema, Relationship, Transaction
from neotime import DateTime
from typing import List, Iterable, Iterator


class Tracker4J:
    def __init__(self, profile=None, **args):
        self.graph = Graph(profile, **args)

    def _get_newest_event_by_timestamp(self, events: Iterable, name: str):
        return next(event for event in reversed(events) if event["event"] == name)

    def _message(self, events: Iterable):

        user = self._get_newest_event_by_timestamp(events, "user")
        bot = self._get_newest_event_by_timestamp(events, "bot")

        reply = bot["text"]
        msg = user["text"]
        user_parse_data = user["parse_data"]
        entities = [entity["entity"] for entity in user_parse_data["entities"]]
        intent = user_parse_data["intent"]["name"]
        timestamp = user["timestamp"]
        return {
            "reply": reply,
            "msg": msg,
            "intent": intent,
            "entities": entities,
            "timestamp": timestamp,
        }

    def _get_latest(self, tx: Transaction, sender_id: str):
        matcher = NodeMatcher(tx)
        query = (
            matcher.match(sender_id)
            .order_by("_.created_at desc")
            .limit(1)
            ._query_and_parameters()[0]
        )
        latest = tx.evaluate(query)
        return latest

    def _AddConstraint(self, sender_id: str):
        try:
            schema = Schema(self.graph)
            schema.create_uniqueness_constraint(sender_id, "timestamp")
        except:
            pass

    def CreateNodeFromEvents(self, events: Iterable, sender_id: str):
        self.CreateNode(self._message(events), sender_id)

    def CreateNode(self, msg, sender_id: str):
        sender_id = str(sender_id)
        tx = self.graph.begin()

        # Dict to kwaargs
        parent = self._get_latest(tx, sender_id)

        if parent == None:
            self._AddConstraint(sender_id)

        new_elem = Node(sender_id, **msg, created_at=DateTime.now())

        tx.create(new_elem)
        new_elem = (
            new_elem
            if (parent == None)
            else Relationship(parent, "TO", new_elem, since=new_elem["timestamp"])
        )
        tx.create(new_elem)
        tx.commit()
        tx.finish()
