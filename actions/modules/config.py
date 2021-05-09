import os

MONGODB_STRING = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
NEO4J_STRING = os.environ.get("NEO4J_URL", "localhost")
NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")
WEATHER_KEY= os.environ.get("WEATHER_KEY", "twQ8s3NiYo2MCBZfj1pZAQ")
WEATHER_ID= os.environ.get("WEATHER_ID", "JnnC8L7yA6ebC44rCiuj")
