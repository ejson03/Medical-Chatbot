import json
import random

with open('jokes.txt') as data_file:
    data = json.load(data_file)
    print(random.choice(data))
#     new_jokes = []
#     count = 0
#     for joke in data:
#         if joke.find("FUCK") != -1 or \
#         joke.find("ass") != -1 or \
#         joke.find("vagina") != -1 or \
#         joke.find("pussy") != -1 or \
#         joke.find("abort") != -1 or \
#         joke.find("sex") != -1 or \
#         joke.find("rape") != -1 or \
#         joke.find("fetus") != -1 or \
#         joke.find("MILF") != -1 or \
#         joke.find("spit ") != -1 or \
#         joke.find("feminist") != -1:
#             count +=1
#         else:
#             new_jokes.append(joke)
#     print(count, len(new_jokes))
# with open("jokes.txt", "w") as data_file:
#     json.dump(new_jokes, data_file)
