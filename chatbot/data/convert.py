from rasa.nlu.training_data import load_data

input_training_file = './training.json'
output_md_file = './nlu.md'

with open(output_md_file,'a') as f:
    f.write(load_data(input_training_file).nlu_as_markdown())