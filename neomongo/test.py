import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

mydb.talks.insert_one( {
	"sender_id": "vedant",
	"slots": {
		"age": None,
		"bp": None,
		"conform": None,
		"excercise": None,
		"file": None,
		"filedesc": "sad",
		"height": None,
		"is_form": None,
		"location": None,
		"name": None,
		"password": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO.",
		"requested_slot": None,
		"smoking": None,
		"symptom": None,
		"username": "vedant",
		"weight": None
	},
	"events": [{
		"event": "action",
		"timestamp": 1590231701.3558173,
		"name": "action_session_start",
		"policy": None,
		"confidence": None
	}, {
		"event": "session_started",
		"timestamp": 1590231701.3558173
	}, {
		"event": "action",
		"timestamp": 1590231701.3558173,
		"name": "action_listen",
		"policy": None,
		"confidence": None
	}, {
		"event": "action",
		"timestamp": 1590231703.4416306,
		"name": "action_get_credentials",
		"policy": "MappingPolicy",
		"confidence": "0.98"
	}, {
		"event": "slot",
		"timestamp": 1590231703.4416306,
		"name": "username",
		"value": "vedant"
	}, {
		"event": "slot",
		"timestamp": 1590231703.4416306,
		"name": "password",
		"value": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO."
	}, {
		"event": "user",
		"timestamp": 1590231813.4085984,
		"text": "hi",
		"parse_data": {
			"intent": {
				"name": "smalltalk_greetings_hello",
				"confidence": 0.8411073684692383
			},
			"entities": [],
			"intent_ranking": [{
				"name": "smalltalk_greetings_hello",
				"confidence": 0.8411073684692383
			}, {
				"name": "greet",
				"confidence": 0.14750149846076965
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0021518785506486893
			}, {
				"name": "smalltalk_user_needs_advice",
				"confidence": 0.0017109574982896447
			}, {
				"name": "smalltalk_greetings_goodevening",
				"confidence": 0.001521394238807261
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.0014465793501585722
			}, {
				"name": "smalltalk_user_loves_agent",
				"confidence": 0.0013881137128919363
			}, {
				"name": "ask_howdoing",
				"confidence": 0.001183311571367085
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.0010117569472640753
			}, {
				"name": "smalltalk_greetings_goodmorning",
				"confidence": 0.000977124902419746
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "hi"
		},
		"input_channel": "rest",
		"message_id": "250231a82bc74d17a4f300fb5c6ef9d5",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231814.173645,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9415639042854309
	}, {
		"event": "user",
		"timestamp": 1590231847.104971,
		"text": "i am happy",
		"parse_data": {
			"intent": {
				"name": "get_emotion",
				"confidence": 0.9994997978210449
			},
			"entities": [{
				"entity": "emotion",
				"start": 5,
				"end": 10,
				"value": "happy",
				"extractor": "DIETClassifier"
			}],
			"intent_ranking": [{
				"name": "get_emotion",
				"confidence": 0.9994997978210449
			}, {
				"name": "ask_whoami",
				"confidence": 0.00019819065346382558
			}, {
				"name": "smalltalk_user_lonely",
				"confidence": 0.00011189244105480611
			}, {
				"name": "smalltalk_user_excited",
				"confidence": 0.00008020534733077511
			}, {
				"name": "smalltalk_agent_happy",
				"confidence": 0.00002821886482706759
			}, {
				"name": "out_of_scope",
				"confidence": 0.00002596447302494198
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.000025335206373711117
			}, {
				"name": "smalltalk_greetings_whatsup",
				"confidence": 0.000012223459634697065
			}, {
				"name": "deny",
				"confidence": 0.000009762321496964432
			}, {
				"name": "smalltalk_user_wants_to_talk",
				"confidence": 0.000008454540875391103
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i am happy"
		},
		"input_channel": "rest",
		"message_id": "d24e3ed06a35423bbdec029d03f93555",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231850.3647656,
		"name": "action_get_song",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.6559958457946777
	}, {
		"event": "bot",
		"timestamp": 1590231850.3647656,
		"text": "Here is something for your mood.",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": None
		},
		"metadata": {}
	}, {
		"event": "bot",
		"timestamp": 1590231850.3647656,
		"text": None,
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": {
				"payload": "video",
				"data": "https://www.youtube.com/embed/afhAqMeeQJk?autoplay=1"
			}
		},
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231850.3916996,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9487152695655823
	}, {
		"event": "user",
		"timestamp": 1590231936.3426356,
		"text": "i want to upload a file",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9826920032501221
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9826920032501221
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.00413976376876235
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.004087887704372406
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.0023806490935385227
			}, {
				"name": "ask_weather_location",
				"confidence": 0.0016602104296907783
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0013728808844462037
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.001060911687090993
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.00101483054459095
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0009011466754600406
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.0006897257990203798
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload a file"
		},
		"input_channel": "rest",
		"message_id": "e9b24c0997654122bf173dedd37c9158",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231936.436981,
		"name": "utter_ask_is_form",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.4577173590660095
	}, {
		"event": "bot",
		"timestamp": 1590231936.436981,
		"text": "Do you wanna fill health form first or upload directly ?",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": [{
				"payload": "/ask_ehr_form",
				"title": "Yes"
			}, {
				"payload": "/ask_upload",
				"title": "No"
			}],
			"attachment": None,
			"image": None,
			"custom": None
		},
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231936.4639027,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9609787464141846
	}, {
		"event": "user",
		"timestamp": 1590231944.1531775,
		"text": "/ask_upload",
		"parse_data": {
			"text": "/ask_upload",
			"intent": {
				"name": "ask_upload",
				"confidence": 1
			},
			"intent_ranking": [{
				"name": "ask_upload",
				"confidence": 1
			}],
			"entities": []
		},
		"input_channel": "rest",
		"message_id": "8255264b50994fa7959b9dd1907783dd",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231946.2130225,
		"name": "action_reset_slot",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.5622389316558838
	}, {
		"event": "slot",
		"timestamp": 1590231946.2130225,
		"name": "filedesc",
		"value": None
	}, {
		"event": "action",
		"timestamp": 1590231948.2688181,
		"name": "file_form",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.7860856056213379
	}, {
		"event": "bot",
		"timestamp": 1590231948.2688181,
		"metadata": {
			"password": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO.",
			"username": "vedant"
		},
		"text": " Enter the file description",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": None
		}
	}, {
		"event": "form",
		"timestamp": 1590231948.2688181,
		"name": "file_form"
	}, {
		"event": "slot",
		"timestamp": 1590231948.2688181,
		"name": "requested_slot",
		"value": "filedesc"
	}, {
		"event": "action",
		"timestamp": 1590231948.2977426,
		"name": "action_listen",
		"policy": "policy_3_FormPolicy",
		"confidence": 1
	}, {
		"event": "user",
		"timestamp": 1590231957.776099,
		"text": "kahs",
		"parse_data": {
			"intent": {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.9015176892280579
			},
			"entities": [],
			"intent_ranking": [{
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.9015176892280579
			}, {
				"name": "ask_howdoing",
				"confidence": 0.04858364537358284
			}, {
				"name": "affirm",
				"confidence": 0.027947843074798584
			}, {
				"name": "smalltalk_greetings_whatsup",
				"confidence": 0.0070844655856490135
			}, {
				"name": "smalltalk_agent_right",
				"confidence": 0.005349078681319952
			}, {
				"name": "greet",
				"confidence": 0.003622109303250909
			}, {
				"name": "smalltalk_user_here",
				"confidence": 0.001801867038011551
			}, {
				"name": "smalltalk_greetings_how_are_you",
				"confidence": 0.0015741686802357435
			}, {
				"name": "smalltalk_greetings_hello",
				"confidence": 0.0012742305407300591
			}, {
				"name": "ask_weather_location",
				"confidence": 0.001244927872903645
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "kahs"
		},
		"input_channel": "rest",
		"message_id": "5c69f3d39c84420ea4e86997d8ca7428",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231959.8258839,
		"name": "file_form",
		"policy": "policy_3_FormPolicy",
		"confidence": 1
	}, {
		"event": "bot",
		"timestamp": 1590231959.8258839,
		"text": None,
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": {
				"payload": "fileupload"
			}
		},
		"metadata": {}
	}, {
		"event": "slot",
		"timestamp": 1590231959.8258839,
		"name": "filedesc",
		"value": "kahs"
	}, {
		"event": "form",
		"timestamp": 1590231959.8258839,
		"name": None
	}, {
		"event": "slot",
		"timestamp": 1590231959.8258839,
		"name": "requested_slot",
		"value": None
	}, {
		"event": "action",
		"timestamp": 1590231959.8558156,
		"name": "utter_file",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.7742182612419128
	}, {
		"event": "bot",
		"timestamp": 1590231959.8558156,
		"text": "Entered file description is :\n -  File Description : kahs\n",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": None
		},
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590231959.884739,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9634532928466797
	}, {
		"event": "action",
		"timestamp": 1590232482.5296395,
		"name": "action_get_credentials",
		"policy": "MappingPolicy",
		"confidence": "0.98"
	}, {
		"event": "slot",
		"timestamp": 1590232482.5296395,
		"name": "username",
		"value": "vedant"
	}, {
		"event": "slot",
		"timestamp": 1590232482.5296395,
		"name": "password",
		"value": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO."
	}, {
		"event": "slot",
		"timestamp": 1590232482.5296395,
		"name": "username",
		"value": "vedant"
	}, {
		"event": "slot",
		"timestamp": 1590232482.5296395,
		"name": "password",
		"value": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO."
	}, {
		"event": "user",
		"timestamp": 1590232514.1593676,
		"text": "i want to upload a file",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9826920032501221
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9826920032501221
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.004139760043472052
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.004087880253791809
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.0023806490935385227
			}, {
				"name": "ask_weather_location",
				"confidence": 0.0016602089162915945
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0013728771591559052
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.0010609105229377747
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.0010148294968530536
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0009011449874378741
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.0006897251005284488
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload a file"
		},
		"input_channel": "rest",
		"message_id": "2bd24fd7773f43afa5aea7a39eb05e46",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232514.1793027,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9143103361129761
	}, {
		"event": "user",
		"timestamp": 1590232525.3786998,
		"text": "i want to upload a fille",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9797670841217041
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9797670841217041
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.0051735867746174335
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.0036217928864061832
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.0033753253519535065
			}, {
				"name": "ask_weather_location",
				"confidence": 0.002986521925777197
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.0015023521846160293
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.0012823244323953986
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0010189787717536092
			}, {
				"name": "describe_symptoms",
				"confidence": 0.0006421615835279226
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0006298776715993881
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload a fille"
		},
		"input_channel": "rest",
		"message_id": "8ccbff6eb03b4ea7a06cc546ad8b801e",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232527.7558386,
		"name": "action_set_file",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.39589643478393555
	}, {
		"event": "action",
		"timestamp": 1590232527.7797754,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.8563870191574097
	}, {
		"event": "user",
		"timestamp": 1590232549.4257786,
		"text": "i want to upload  afile",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9725667834281921
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9725667834281921
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.005475715268403292
			}, {
				"name": "ask_weather_location",
				"confidence": 0.005134131759405136
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.004886498209089041
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.0036210697144269943
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.0028971293941140175
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.0016724689630791545
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0016032903222367167
			}, {
				"name": "affirm",
				"confidence": 0.001075297244824469
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0010675756493583322
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload  afile"
		},
		"input_channel": "rest",
		"message_id": "b7d3c7916f0a4d039c4d1a59221f5533",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232549.4467232,
		"name": "utter_ask_is_form",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.4494977593421936
	}, {
		"event": "bot",
		"timestamp": 1590232549.4467232,
		"text": "Do you wanna fill health form first or upload directly ?",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": [{
				"payload": "/ask_ehr_form",
				"title": "Yes"
			}, {
				"payload": "/ask_upload",
				"title": "No"
			}],
			"attachment": None,
			"image": None,
			"custom": None
		},
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232549.469695,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9597872495651245
	}, {
		"event": "user",
		"timestamp": 1590232553.696422,
		"text": "/ask_upload",
		"parse_data": {
			"text": "/ask_upload",
			"intent": {
				"name": "ask_upload",
				"confidence": 1
			},
			"intent_ranking": [{
				"name": "ask_upload",
				"confidence": 1
			}],
			"entities": []
		},
		"input_channel": "rest",
		"message_id": "d81c95874a5e4feab8f7747fb00e5b8d",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232555.7412195,
		"name": "action_reset_slot",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.6006882786750793
	}, {
		"event": "slot",
		"timestamp": 1590232555.7412195,
		"name": "filedesc",
		"value": None
	}, {
		"event": "action",
		"timestamp": 1590232557.8013668,
		"name": "file_form",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.7904602885246277
	}, {
		"event": "bot",
		"timestamp": 1590232557.8013668,
		"metadata": {
			"password": "$2b$12$BQXIDNBV3lMIJusG5CJqu.YNOMZTuPo.8XXV3dHO2LSBLwzBDhzO.",
			"username": "vedant"
		},
		"text": " Enter the file description",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": None
		}
	}, {
		"event": "form",
		"timestamp": 1590232557.8013668,
		"name": "file_form"
	}, {
		"event": "slot",
		"timestamp": 1590232557.8013668,
		"name": "requested_slot",
		"value": "filedesc"
	}, {
		"event": "action",
		"timestamp": 1590232557.8332822,
		"name": "action_listen",
		"policy": "policy_3_FormPolicy",
		"confidence": 1
	}, {
		"event": "user",
		"timestamp": 1590232564.5835392,
		"text": "sad",
		"parse_data": {
			"intent": {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.9530683755874634
			},
			"entities": [],
			"intent_ranking": [{
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.9530683755874634
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.019668644294142723
			}, {
				"name": "greet",
				"confidence": 0.01314043253660202
			}, {
				"name": "smalltalk_agent_right",
				"confidence": 0.003611996304243803
			}, {
				"name": "smalltalk_dialog_wrong",
				"confidence": 0.0022966712713241577
			}, {
				"name": "smalltalk_greetings_hello",
				"confidence": 0.0022128133568912745
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.0019050843548029661
			}, {
				"name": "goodbye",
				"confidence": 0.0018041414441540837
			}, {
				"name": "smalltalk_greetings_goodevening",
				"confidence": 0.001189577393233776
			}, {
				"name": "affirm",
				"confidence": 0.0011022198013961315
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "sad"
		},
		"input_channel": "rest",
		"message_id": "b7f0a61af2f84dfcb7c41f3fa081002a",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232566.626012,
		"name": "file_form",
		"policy": "policy_3_FormPolicy",
		"confidence": 1
	}, {
		"event": "bot",
		"timestamp": 1590232566.626012,
		"text": None,
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": {
				"payload": "fileupload"
			}
		},
		"metadata": {}
	}, {
		"event": "slot",
		"timestamp": 1590232566.626012,
		"name": "filedesc",
		"value": "sad"
	}, {
		"event": "form",
		"timestamp": 1590232566.626012,
		"name": None
	}, {
		"event": "slot",
		"timestamp": 1590232566.626012,
		"name": "requested_slot",
		"value": None
	}, {
		"event": "action",
		"timestamp": 1590232566.6479537,
		"name": "utter_file",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.7742182612419128
	}, {
		"event": "bot",
		"timestamp": 1590232566.6479537,
		"text": "Entered file description is :\n -  File Description : sad\n",
		"data": {
			"elements": None,
			"quick_replies": None,
			"buttons": None,
			"attachment": None,
			"image": None,
			"custom": None
		},
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232566.67189,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.9634532928466797
	}, {
		"event": "user",
		"timestamp": 1590232987.9819584,
		"text": "i want to upload a file",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9826920032501221
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9826920032501221
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.0041397674940526485
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.004087887704372406
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.0023806490935385227
			}, {
				"name": "ask_weather_location",
				"confidence": 0.001660215319134295
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0013728796038776636
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.001060911687090993
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.00101483054459095
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0009011476649902761
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.0006897257990203798
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload a file"
		},
		"input_channel": "rest",
		"message_id": "8442b3332f2749bb944e935fd822d175",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590232990.107755,
		"name": "action_set_file",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.8096664547920227
	}, {
		"event": "action",
		"timestamp": 1590232990.1389463,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.8756511211395264
	}, {
		"event": "user",
		"timestamp": 1590233005.4812963,
		"text": "i want to upload a file",
		"parse_data": {
			"intent": {
				"name": "ask_form",
				"confidence": 0.9826920032501221
			},
			"entities": [],
			"intent_ranking": [{
				"name": "ask_form",
				"confidence": 0.9826920032501221
			}, {
				"name": "smalltalk_user_going_to_bed",
				"confidence": 0.0041397674940526485
			}, {
				"name": "smalltalk_user_wants_to_see_agent_again",
				"confidence": 0.004087887704372406
			}, {
				"name": "smalltalk_confirmation_no",
				"confidence": 0.002380651654675603
			}, {
				"name": "ask_weather_location",
				"confidence": 0.0016602136893197894
			}, {
				"name": "smalltalk_greetings_bye",
				"confidence": 0.0013728808844462037
			}, {
				"name": "smalltalk_user_can_not_sleep",
				"confidence": 0.001060911687090993
			}, {
				"name": "smalltalk_confirmation_yes",
				"confidence": 0.0010148314759135246
			}, {
				"name": "smalltalk_dialog_hold_on",
				"confidence": 0.0009011476649902761
			}, {
				"name": "smalltalk_user_busy",
				"confidence": 0.0006897264393046498
			}],
			"response_selector": {
				"default": {
					"response": {
						"name": None,
						"confidence": 0
					},
					"ranking": [],
					"full_retrieval_intent": None
				}
			},
			"text": "i want to upload a file"
		},
		"input_channel": "rest",
		"message_id": "59760d0a592e491f81ca78a5e4453e57",
		"metadata": {}
	}, {
		"event": "action",
		"timestamp": 1590233007.5865948,
		"name": "action_set_file",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.34740889072418213
	}, {
		"event": "action",
		"timestamp": 1590233007.61751,
		"name": "action_listen",
		"policy": "policy_1_TEDPolicy",
		"confidence": 0.8679957985877991
	}]

});


