# from rasa_nlu.converters import load_data
# input_training_file = 'testing.json'
# output_md_file = 'training.md'

# with open(output_md_file,'w') as f:
#     f.write(load_data(input_training_file).as_markdown())
import json
with open("testing.json", "r") as data:
    rasa_data = json.load(data)



from rasa.nlu.convert import convert_training_data
convert_training_data(data_file="testing.json", out_file="out_file.md", output_format="md", language="")