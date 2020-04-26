import os 
import pandas as pd 

for stuff in os.listdir('.'):
    if stuff.endswith(".csv"):
        df = pd.read_csv(stuff, low_memory=False)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        if stuff == "shortjokes.csv":
            df = df['Joke']
        
        df.to_json(f"{stuff[:-3]}.json", orient="records")