import json
with open('music.json', 'r') as emotions:
    data = json.load(emotions)

import random
print(random.choice(data['sad']))

