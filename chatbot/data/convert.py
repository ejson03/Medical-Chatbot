from rasa.nlu.training_data import load_data
import os
import glob
output_md_file = './nlu.md'
training = glob.glob("./training_*.json", recursive=True )

for file in training:
    with open(output_md_file,'a') as f:
        f.write("\n")
        f.write(load_data(file).nlu_as_markdown())
    os.remove(file)


