from py2neo import Graph, Node, NodeMatcher, matching, Schema, Relationship, Transaction
from neotime import DateTime
from typing import List, Iterable, Iterator
ex = [
    {
        "event": "action",
        "timestamp": 1616675918.5803747,
        "name": "action_session_start",
        "policy": None,
        "confidence": None,
    },
    {
        "event": "user",
        "timestamp": 1616675918.8820746,
        "text": "What is up",
        "parse_data": {
            "intent": {
                "name": "smalltalk_greetings_whatsup",
                "confidence": 0.9814417958259583,
            },
            "entities": [],
            "intent_ranking": [
                {
                    "name": "smalltalk_greetings_whatsup",
                    "confidence": 0.9814417958259583,
                },
                {
                    "name": "smalltalk_agent_residence",
                    "confidence": 0.016044309362769127,
                },
                {"name": "greet", "confidence": 0.0006020160508342087},
                {
                    "name": "smalltalk_agent_birth_date",
                    "confidence": 0.00047379895113408566,
                },
                {"name": "smalltalk_agent_sure",
                    "confidence": 0.00036718594492413104},
                {"name": "smalltalk_agent_age", "confidence": 0.0002741797943599522},
                {"name": "ask_whoami", "confidence": 0.0002574676473159343},
                {
                    "name": "smalltalk_dialog_what_do_you_mean",
                    "confidence": 0.0001878119946923107,
                },
                {"name": "smalltalk_agent_right",
                    "confidence": 0.00017906675930134952},
                {"name": "affirm", "confidence": 0.00017236405983567238},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "What is up",
        },
        "input_channel": "rest",
        "message_id": "eea340274fd1448aa26171d452565239",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675918.8855593,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8108109831809998,
    },
    {
        "event": "user",
        "timestamp": 1616675920.6201644,
        "text": "What is up",
        "parse_data": {
            "intent": {
                "name": "smalltalk_greetings_whatsup",
                "confidence": 0.9814417958259583,
            },
            "entities": [],
            "intent_ranking": [
                {
                    "name": "smalltalk_greetings_whatsup",
                    "confidence": 0.9814417958259583,
                },
                {
                    "name": "smalltalk_agent_residence",
                    "confidence": 0.016044309362769127,
                },
                {"name": "greet", "confidence": 0.0006020160508342087},
                {
                    "name": "smalltalk_agent_birth_date",
                    "confidence": 0.00047379895113408566,
                },
                {"name": "smalltalk_agent_sure",
                    "confidence": 0.00036718594492413104},
                {"name": "smalltalk_agent_age", "confidence": 0.0002741797943599522},
                {"name": "ask_whoami", "confidence": 0.0002574676473159343},
                {
                    "name": "smalltalk_dialog_what_do_you_mean",
                    "confidence": 0.0001878119946923107,
                },
                {"name": "smalltalk_agent_right",
                    "confidence": 0.00017906675930134952},
                {"name": "affirm", "confidence": 0.00017236405983567238},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "What is up",
        },
        "input_channel": "rest",
        "message_id": "8fb7d652a71c4a0e82fcc3eae2389fa2",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675920.6385593,
        "name": "utter_smalltalk_greetings_whatsup",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8127857446670532,
    },
    {
        "event": "bot",
        "timestamp": 1616675920.638576,
        "text": "Just here, waiting to help someone. What can I do for you?",
        "data": {
            "elements": None,
            "quick_replies": None,
            "buttons": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675920.6491182,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9901170134544373,
    },
    {
        "event": "user",
        "timestamp": 1616675923.7973921,
        "text": "What is up",
        "parse_data": {
            "intent": {
                "name": "smalltalk_greetings_whatsup",
                "confidence": 0.9814417958259583,
            },
            "entities": [],
            "intent_ranking": [
                {
                    "name": "smalltalk_greetings_whatsup",
                    "confidence": 0.9814417958259583,
                },
                {
                    "name": "smalltalk_agent_residence",
                    "confidence": 0.016044309362769127,
                },
                {"name": "greet", "confidence": 0.0006020160508342087},
                {
                    "name": "smalltalk_agent_birth_date",
                    "confidence": 0.00047379895113408566,
                },
                {"name": "smalltalk_agent_sure",
                    "confidence": 0.00036718594492413104},
                {"name": "smalltalk_agent_age", "confidence": 0.0002741797943599522},
                {"name": "ask_whoami", "confidence": 0.0002574676473159343},
                {
                    "name": "smalltalk_dialog_what_do_you_mean",
                    "confidence": 0.0001878119946923107,
                },
                {"name": "smalltalk_agent_right",
                    "confidence": 0.00017906675930134952},
                {"name": "affirm", "confidence": 0.00017236405983567238},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "What is up",
        },
        "input_channel": "rest",
        "message_id": "9cd23a53f6b94621aed1db2f9bf2ca9b",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675923.8018482,
        "name": "utter_smalltalk_greetings_whatsup",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8130842447280884,
    },
    {
        "event": "bot",
        "timestamp": 1616675923.8018572,
        "text": "Not a whole lot. What's going on with you?",
        "data": {
            "elements": None,
            "quick_replies": None,
            "buttons": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675923.806976,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9900680780410767,
    },
    {
        "event": "user",
        "timestamp": 1616675932.4290679,
        "text": "What is up",
        "parse_data": {
            "intent": {
                "name": "smalltalk_greetings_whatsup",
                "confidence": 0.9814417958259583,
            },
            "entities": [],
            "intent_ranking": [
                {
                    "name": "smalltalk_greetings_whatsup",
                    "confidence": 0.9814417958259583,
                },
                {
                    "name": "smalltalk_agent_residence",
                    "confidence": 0.016044309362769127,
                },
                {"name": "greet", "confidence": 0.0006020160508342087},
                {
                    "name": "smalltalk_agent_birth_date",
                    "confidence": 0.00047379895113408566,
                },
                {"name": "smalltalk_agent_sure",
                    "confidence": 0.00036718594492413104},
                {"name": "smalltalk_agent_age", "confidence": 0.0002741797943599522},
                {"name": "ask_whoami", "confidence": 0.0002574676473159343},
                {
                    "name": "smalltalk_dialog_what_do_you_mean",
                    "confidence": 0.0001878119946923107,
                },
                {"name": "smalltalk_agent_right",
                    "confidence": 0.00017906675930134952},
                {"name": "affirm", "confidence": 0.00017236405983567238},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "What is up",
        },
        "input_channel": "rest",
        "message_id": "e6515c76b53e441ebf9fec2fee04db37",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675932.4508433,
        "name": "utter_smalltalk_greetings_whatsup",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8141078948974609,
    },
    {
        "event": "bot",
        "timestamp": 1616675932.4508655,
        "text": "Not a whole lot. What's going on with you?",
        "data": {
            "elements": None,
            "quick_replies": None,
            "buttons": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675932.4706597,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9900395274162292,
    },
    {
        "event": "user",
        "timestamp": 1616675950.2043567,
        "text": "How are you?",
        "parse_data": {
            "intent": {
                "name": "smalltalk_greetings_how_are_you",
                "confidence": 0.9984859228134155,
            },
            "entities": [],
            "intent_ranking": [
                {
                    "name": "smalltalk_greetings_how_are_you",
                    "confidence": 0.9984859228134155,
                },
                {"name": "smalltalk_agent_clever",
                    "confidence": 0.0006242030067369342},
                {"name": "smalltalk_agent_age", "confidence": 0.0002958130498882383},
                {"name": "smalltalk_agent_sure",
                    "confidence": 0.00019065968808718026},
                {
                    "name": "smalltalk_agent_origin",
                    "confidence": 0.00014693287084810436,
                },
                {"name": "smalltalk_agent_boring",
                    "confidence": 6.978981400607154e-05},
                {
                    "name": "smalltalk_user_likes_agent",
                    "confidence": 6.361620035022497e-05,
                },
                {"name": "smalltalk_agent_boss",
                    "confidence": 4.392426126287319e-05},
                {"name": "goodbye", "confidence": 4.3530017137527466e-05},
                {"name": "smalltalk_agent_real", "confidence": 3.56112104782369e-05},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "How are you?",
        },
        "input_channel": "rest",
        "message_id": "1f5072e3a5b64d2084430e6f92d90720",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675950.2241943,
        "name": "utter_smalltalk_greetings_whatsup",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.26178038120269775,
    },
    {
        "event": "bot",
        "timestamp": 1616675950.2242181,
        "text": "Just here, waiting to help someone. What can I do for you?",
        "data": {
            "elements": None,
            "quick_replies": None,
            "buttons": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675950.2416918,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.990136981010437,
    },
    {
        "event": "user",
        "timestamp": 1616675964.2270176,
        "text": "I have a headache",
        "parse_data": {
            "intent": {"name": "describe_symptoms", "confidence": 0.9982737302780151},
            "entities": [
                {
                    "entity": "symptom",
                    "start": 9,
                    "end": 17,
                    "value": "headache",
                    "extractor": "DIETClassifier",
                }
            ],
            "intent_ranking": [
                {"name": "describe_symptoms", "confidence": 0.9982737302780151},
                {"name": "ask_name", "confidence": 0.0002765711396932602},
                {
                    "name": "smalltalk_user_misses_agent",
                    "confidence": 0.0002556703984737396,
                },
                {
                    "name": "smalltalk_user_likes_agent",
                    "confidence": 0.00024125355412252247,
                },
                {
                    "name": "smalltalk_user_does_not_want_to_talk",
                    "confidence": 0.00021515855041798204,
                },
                {
                    "name": "smalltalk_agent_annoying",
                    "confidence": 0.000163412289111875,
                },
                {
                    "name": "smalltalk_user_wants_to_talk",
                    "confidence": 0.00015218256157822907,
                },
                {
                    "name": "smalltalk_user_looks_like",
                    "confidence": 0.00014677870785817504,
                },
                {"name": "smalltalk_dialog_hug",
                    "confidence": 0.0001452019641874358},
                {"name": "ask_languagesbot", "confidence": 0.0001300082221860066},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "I have a headache",
        },
        "input_channel": "rest",
        "message_id": "977320bc6d85403d86f21076f004ee2a",
        "metadata": {},
    },
    {
        "event": "slot",
        "timestamp": 1616675964.227038,
        "name": "symptom",
        "value": ["headache"],
    },
    {
        "event": "action",
        "timestamp": 1616675964.2377982,
        "name": "action_diagnose_symptoms",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9114933609962463,
    },
    {
        "event": "action",
        "timestamp": 1616675964.242233,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8746688961982727,
    },

    {
        "event": "slot",
        "timestamp": 1616675965.7875702,
        "name": "symptom",
        "value": ["headache"],
    },
    {
        "event": "action",
        "timestamp": 1616675965.8168905,
        "name": "action_diagnose_symptoms",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9124966859817505,
    },
    {
        "event": "action",
        "timestamp": 1616675965.8211231,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8649342060089111,
    },
    {
        "event": "user",
        "timestamp": 1616675972.1152594,
        "text": "I have ache",
        "parse_data": {
            "intent": {"name": "describe_symptoms", "confidence": 0.5257101058959961},
            "entities": [],
            "intent_ranking": [
                {"name": "describe_symptoms", "confidence": 0.5257101058959961},
                {"name": "ask_whatismyname", "confidence": 0.0965825691819191},
                {
                    "name": "smalltalk_user_wants_to_talk",
                    "confidence": 0.07554157078266144,
                },
                {"name": "smalltalk_user_busy", "confidence": 0.05783925950527191},
                {
                    "name": "smalltalk_agent_my_friend",
                    "confidence": 0.055163316428661346,
                },
                {"name": "smalltalk_user_back", "confidence": 0.04796499386429787},
                {
                    "name": "smalltalk_agent_marry_user",
                    "confidence": 0.04636649042367935,
                },
                {
                    "name": "smalltalk_user_does_not_want_to_talk",
                    "confidence": 0.036395423114299774,
                },
                {
                    "name": "smalltalk_user_testing_agent",
                    "confidence": 0.029440147802233696,
                },
                {"name": "smalltalk_user_looks_like",
                    "confidence": 0.0289960615336895},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "I have ache",
        },
        "input_channel": "rest",
        "message_id": "52aeb7a114c444dc887be7bcac5c9161",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675972.1264791,
        "name": "action_diagnose_symptoms",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9484474062919617,
    },
    {
        "event": "action",
        "timestamp": 1616675972.1312578,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8978271484375,
    },
    {
        "event": "user",
        "timestamp": 1616675981.9722009,
        "text": "Make me laugh",
        "parse_data": {
            "intent": {
                "name": "smalltalk_agent_funny",
                "confidence": 0.9781172871589661,
            },
            "entities": [],
            "intent_ranking": [
                {"name": "smalltalk_agent_funny", "confidence": 0.9781172871589661},
                {"name": "telljoke", "confidence": 0.016711102798581123},
                {"name": "greet", "confidence": 0.0013122530654072762},
                {
                    "name": "smalltalk_agent_talk_to_me",
                    "confidence": 0.000733789405785501,
                },
                {"name": "smalltalk_user_sleepy",
                    "confidence": 0.0006967277149669826},
                {
                    "name": "smalltalk_user_wants_to_talk",
                    "confidence": 0.0006362360436469316,
                },
                {
                    "name": "smalltalk_dialog_hold_on",
                    "confidence": 0.0006088679074309766,
                },
                {
                    "name": "smalltalk_agent_marry_user",
                    "confidence": 0.00046241842210292816,
                },
                {"name": "smalltalk_user_tired",
                    "confidence": 0.00044262511073611677},
                {
                    "name": "smalltalk_greetings_whatsup",
                    "confidence": 0.00027877173852175474,
                },
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "Make me laugh",
        },
        "input_channel": "rest",
        "message_id": "768b147ffb3d47319aa5c97854c721ea",
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675982.0035968,
        "name": "utter_smalltalk_agent_funny",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.8718829154968262,
    },
    {
        "event": "bot",
        "timestamp": 1616675982.0036755,
        "text": "Glad you think I'm funny.",
        "data": {
            "elements": None,
            "quick_replies": None,
            "buttons": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        "metadata": {},
    },
    {
        "event": "action",
        "timestamp": 1616675982.035909,
        "name": "action_listen",
        "policy": "policy_1_TEDPolicy",
        "confidence": 0.9899671077728271,
    },
    {
        "event": "user",
        "timestamp": 2255685965.7873676,
        "text": "I eat paratha",
        "parse_data": {
            "intent": {"name": "describe_symptoms", "confidence": 0.9982737302780151},
            "entities": [
                {
                    "entity": "symptom",
                    "start": 9,
                    "end": 17,
                    "value": "headache",
                    "extractor": "DIETClassifier",
                }
            ],
            "intent_ranking": [
                {"name": "describe_symptoms", "confidence": 0.9982737302780151},
                {"name": "ask_name", "confidence": 0.0002765711396932602},
                {
                    "name": "smalltalk_user_misses_agent",
                    "confidence": 0.0002556703984737396,
                },
                {
                    "name": "smalltalk_user_likes_agent",
                    "confidence": 0.00024125355412252247,
                },
                {
                    "name": "smalltalk_user_does_not_want_to_talk",
                    "confidence": 0.00021515855041798204,
                },
                {
                    "name": "smalltalk_agent_annoying",
                    "confidence": 0.000163412289111875,
                },
                {
                    "name": "smalltalk_user_wants_to_talk",
                    "confidence": 0.00015218256157822907,
                },
                {
                    "name": "smalltalk_user_looks_like",
                    "confidence": 0.00014677870785817504,
                },
                {"name": "smalltalk_dialog_hug",
                    "confidence": 0.0001452019641874358},
                {"name": "ask_languagesbot", "confidence": 0.0001300082221860066},
            ],
            "response_selector": {
                "default": {
                    "response": {"name": None, "confidence": 0.0},
                    "ranking": [],
                    "full_retrieval_intent": None,
                }
            },
            "text": "I have a headache",
        },
        "input_channel": "rest",
        "message_id": "b7c6b01943c34a63a0c034639861b43d",
        "metadata": {},
    },
]

class Neo4J:
    def __init__(self, **args):
        super().__init__()
        self.graph = Graph(**args)

    def _get_newest_event_by_timestamp(self, events: Iterable, name: str):
        return next(event for event in reversed(events) if event["event"] == name)

    def _message(self, events: Iterable):

        user = self._get_newest_event_by_timestamp(events, "user")
        bot = self._get_newest_event_by_timestamp(events, "bot")

        reply = bot['text']
        msg = user['text']
        user_parse_data = user['parse_data']
        entities = [entity['entity']
                    for entity in user_parse_data['entities']]
        intent = user_parse_data['intent']['name']
        timestamp = user['timestamp']
        return {"reply": reply, "msg": msg, "intent": intent, "entities": entities, "timestamp": timestamp, "bot": bot, "user": user}

    def _get_latest(self, tx: Transaction, sender_id: str):
        matcher = NodeMatcher(tx)
        query = matcher.match(sender_id).order_by(
            "_.created_at desc").limit(1)._query_and_parameters()[0]
        latest = tx.evaluate(query)
        return latest

    def _AddConstraint(self, tx: Transaction, sender_id: str):
        try:
            schema = Schema(tx)
            schema.create_uniqueness_constraint(sender_id, "timestamp")
        except:
            pass
        return tx

    def CreateNodeFromEvents(self, events: Iterable, sender_id: str):
        return self.CreateNode(self._message(events), sender_id)

    def CreateNode(self, msg, sender_id: str):
        sender_id = str(sender_id)
        tx = self.graph.begin()

        # Dict to kwaargs
        parent = self._get_latest(tx, sender_id)

        if(parent == None):
            tx = self._AddConstraint(tx, sender_id)

        if(tx.finished()):
            tx = graph.begin()

        new_elem = Node(sender_id, **msg, created_at=DateTime.now())

        tx.create(new_elem)
        new_elem = new_elem if (parent == None) else Relationship(
            parent, "TO", new_elem, since=new_elem['timestamp'])
        tx.create(new_elem)
        tx.commit()

    def getAllBySenderId(self, sender_id: str) -> list:
        tx = self._.begin()
        matcher = NodeMatcher(tx)
        elems = matcher.match(sender_id).order_by("_.created_at desc").limit(1)
        print(elems._query_and_parameters()[0])
        elems = elems.all()
        tx.commit()
        print(elems)
        elems = [elem.get("reply") for elem in elems]
        return elems
