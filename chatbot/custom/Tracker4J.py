from py2neo import Graph, Node, NodeMatcher, matching, Schema, Relationship, Transaction
from neotime import DateTime
from typing import List, Iterable, Iterator
import pytz
asia = pytz.timezone('Asia/Kolkata')

# logging.getLogger("py2neo").setLevel(logging.WARNING)

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
        latest = (
            matcher.match("chat", sender_id=sender_id)
            .order_by("_.created_at desc")
            .limit(1)
            .first()
        )
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

        user = Node("user", sender_id=sender_id)
        print("0"*50)
        print(user)
        new_elem = Node("chat", **msg, created_at=DateTime.now(asia), sender_id=sender_id)
        print("L"*50)
        print(new_elem["timestamp"])
        previous = self._get_latest(tx, sender_id)
        tx.merge(user, "user", "sender_id")
        tx.create(new_elem)
        tx.create(
            Relationship(previous or user, "MSG", new_elem, since=new_elem["timestamp"])
        )
        tx.create(Relationship(user, "TO", new_elem, since=new_elem["timestamp"]))

        tx.commit()

        if previous is None:
            self._AddConstraint(sender_id)


# graph = Tracker4J("bolt://192.168.96.41:7687")
# graph.CreateNodeFromEvents(ex,"ddd")