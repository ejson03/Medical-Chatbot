import logging
import pandas as pd
import numpy as np
import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load('en_core_web_md')
diagnosis_df = pd.read_pickle("assets/pickle/diagnosis_data.pkl")
symptoms_df = pd.read_pickle("assets/pickle/symptoms.pkl")

def encode_symptom(symptom):
    '''
    Convert symptom string to vector using spacy

    :param symptom:
    :return: 256-D vector
    '''
    encoded_symptom = nlp(symptom).vector.tolist()
    return encoded_symptom


def create_illness_vector(encoded_symptoms):
    '''
    Compares the list of encoded symptoms to a list of encoded symptoms. Any symptom above threshold (0.85) will be
    flagged.

    :param encoded_symptoms: A list of encoded symptoms
    :return: A single vector flagging each symptoms appearence in the user message (based on vector similarity)
    '''

    threshold = 0.85
    symptoms_df['symptom_flagged'] = 0

    for encoded_symptom in encoded_symptoms:

        symptoms_df['similarity'] = list(cosine_similarity(np.array(encoded_symptom).reshape(1, -1),
                                                           np.array(list(symptoms_df['symptom_vector'])))[0])

        symptoms_df.loc[symptoms_df['similarity'] > threshold, 'symptom_flagged'] = 1

        number_of_symptoms_flagged = len(symptoms_df.loc[symptoms_df['similarity'] > threshold, 'symptom_flagged'])
    return list(symptoms_df['symptom_flagged'])


def get_diagnosis(illness_vector):
    '''
    Compares the symptoms vector to our diagnosis df and generate the diagnosis (if one exists)

    :param illness_vector:
    :return: A string containing the diagnosis based off of illness vector similarity
    '''

    threshold = 0.5

    diagnosis_df['similarity'] = list(cosine_similarity(np.array(illness_vector).reshape(1, -1),
                                                        np.array(list(diagnosis_df['illness_vector'])))[0])

    # If there is an illness (or multiple illnesses)
    if len(diagnosis_df.loc[diagnosis_df['similarity'] > threshold]) > 0:
        illness = (
            diagnosis_df
            .sort_values(by='similarity', ascending=False)['illness']
            .iloc[0]
        )

        # logging.info(f"Diagnosing user with {illness}")
        diagnosis_string = f"Based on your symptoms it looks like you could have {illness}"

    else:
        closest_match = (
            diagnosis_df
            .sort_values(by='similarity', ascending=False)[['illness', 'similarity']]
            .head(1)
        )
       
        diagnosis_string = "Unfortunately I am unable to diagnose you based on the symptoms you provided"

    return diagnosis_string
