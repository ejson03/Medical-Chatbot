from rasa.nlu.training_data import load_data
import os
import glob
output_md_file = './NLU-Data.md'
training = glob.glob("./output/*training*.json", recursive=True )
for file in training:
    print(file)
    with open(output_md_file,'a') as f:
        f.write("\n\n")
        f.write(load_data(file).nlu_as_markdown())


