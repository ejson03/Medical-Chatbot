from py2neo import Graph,Node,Relationship
from modules.config import * 
import difflib
import random

disease_file = './assets/disease.txt'
disease_names = [i.strip() for i in open(disease_file, 'r', encoding='UTF-8').readlines()]

try:
    graph = Graph(
            host=NEO4J_STRING,
            http_port=7474,
            user=NEO4J_USERNAME,
            password= NEO4J_PASSWORD)
except Exception as e:
    print(e)
    import sys
    sys.exit(-1)

def retrieve_disease_name(name):
    names = []
    name = '.*' + '.*'.join(list(name)) + '.*'
    import re
    pattern = re.compile(name)
    for i in disease_names:
        candidate = pattern.search(i)
        if candidate:
            names.append(candidate.group())
    return names

def get_disease(disease):
    possible_diseases = list(difflib.get_close_matches(disease, disease_names))
    print("o"*50)
    print(possible_diseases)
    if len(possible_diseases) == 0:
        possible_diseases = retrieve_disease_name(disease)
        print("y"*50)
        print(possible_diseases)
    return possible_diseases


def treatment(disease):
    disease = get_disease(disease)
    disease = random.choice(disease)
    a = graph.run("match (a:Disease{name: $disease}) return a", disease=disease).data()[0]['a']
    print(a)
   
def symptom(disease):
    disease = get_disease(disease)
    disease = random.choice(disease)
    a = [x['s.name'] for x in graph.run("MATCH (p:Disease{name: $disease})-[r:has_symptom]->\
                                            (s:Symptom) RETURN s.name", disease=disease).data()]
    a = '\n'.join(a)
    print(a)
    
 
def cause(disease):
    disease = get_disease(disease)
    disease = random.choice(disease)
    a = graph.run("match (a:Disease{name: $disease}) return a.cause", disease=disease).data()[0]['a.cause']
    print(a)
 

def department(disease):
    disease = get_disease(disease)
    disease = random.choice(disease)
    a = graph.run("match (a:Disease{name: $disease})-[:belongs_to]->(s:Department) return s.name",
                        disease=disease).data()[0]['s.name']
    print(a)
   

department("poisoning")

