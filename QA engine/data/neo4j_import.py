import json
from neo4j import GraphDatabase

# query = """
# WITH $json_data AS diseases
# UNWIND diseases AS d

# MERGE (question:Question { name: d.header }) 
# MERGE (answer:Answer { name: d.body }) 
# FOREACH (c IN d.categories | MERGE (category:Category { name: c })
#   MERGE (question)-[:IS_OF]->(category))
# FOREACH (c IN d.categories | MERGE (category:Category { name: c })
#   MERGE (answer)-[:BELONGS_TO]->(category))

# """
query = """
WITH $json_data AS diseases
UNWIND diseases AS d

MERGE (disease:Disease { name: d.name }) 
MERGE (description:Description { name: d.description }) 
MERGE (treatment:Treatment { name: d.treatment }) 

FOREACH (s IN d.symptoms | MERGE (symptom:Symptom { name: s })
  MERGE (symptom)-[:IS_OF]->(disease))
MERGE (treatment)-[:TREATS]->(disease)
MERGE (description)-[:DESCRIBES]->(disease)
"""
url = "bolt://192.168.99.100:7687"
data = "./disease.json"

driver = GraphDatabase.driver(url, encrypted=False)


def add_diseases(tx, json_data):
    for record in tx.run(query, json_data=json_data):
        print(record)

with open(data) as diseases_file:
    diseases_json = json.load(diseases_file)

with driver.session() as session:
    session.write_transaction(add_diseases, diseases_json)
