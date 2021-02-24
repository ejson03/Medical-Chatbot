from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import rasa_core
from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.domain import Domain
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application
from rasa_core.tracker_store import RedisTrackerStore
from rasa_core.tracker_store import MongoTrackerStore


logger = logging.getLogger(__name__)
domain = Domain.load('domain.yml')
db 	= MongoTrackerStore(
    domain,
    host='mongodb://localhost:27017', 
    db='rasa', username=None, 
    password=None, collection='conversations', 
    event_broker=None)


def train_dialogue(domain = 'domain.yml',
				   model_path = './models/dialogue',
				   training_data_file = './data/stories.md'):
	"""Train a model"""
	nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/')
	action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")				
	agent = Agent( domain = domain, 
                                policies = [MemoizationPolicy(), KerasPolicy()],
				interpreter=nlu_interpreter, 
                                generator=None, 
                                tracker_store=db, 
				action_endpoint=action_endpoint,
                                fingerprint=None)
	data = agent.load_data(training_data_file)	
	agent.train(	data,
				epochs = 100,
				batch_size = 25,
				validation_split = 0.2
                          )		
	agent.persist(model_path)
	return agent
	
if __name__ == '__main__':
	agent = train_dialogue()
	rasa_core.run.serve_application(agent , channel='cmdline')		


	#extract list of events and print its names 
	events = db.retrieve("default").as_dialogue().events
	for event in events:
		print(event.as_story_string())