import sys
from rasa.nlu.convert import convert_training_data
convert_training_data(data_file=sys.argv[1], out_file=sys.argv[2], output_format="md", language="")