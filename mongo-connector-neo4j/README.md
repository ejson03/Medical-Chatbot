# NeoMongo

A [docker-compose](http://docs.docker.com/compose/) based test setup for the neo4j\_doc\_manager that automatically transfers MongoDB data into neo4j using the Mongo-Connector.

Please see both projects for more information:

- [neo4j\_doc\_manager](https://github.com/neo4j-contrib/neo4j_doc_manager)
- [mongo-connector](https://github.com/mongodb-labs/mongo-connector)

## Usage

[Docker](https://www.docker.com) and [Docker-Compose](http://docs.docker.com/compose/) need to be installed. 

Checkout this repository then cd into the directory and start the docker containers using: 

```
docker-compose up -d
```

In the first run the connector will not work as the MongoDB Replicaset needs to be initiated first. 

Connect to the MongoDB using the shell:

```
docker exec -ti neomongo_mongo_1 mongo
```

Then initiate the replicaset using:

```
rs.initiate()
```

Now start the connector again using:

```
docker-compose up -d
```

The setup is ready to go.


## Experimenting with the Connector

You can connect to the neo4j by pointing your browser to:

```
http://<docker-host>:7474
```

You can connect to MongoDB using the shell:

```
docker exec -ti neomongo_mongo_1 mongo
```

or by using any other MongoDB client using the mongoUri:

```
mongodb://<docker-host>:27017
```

The neo4j\_doc\_manager [documentation](https://github.com/neo4j-contrib/neo4j_doc_manager/blob/master/docs/neo4j_doc_manager_doc.adoc) has a number of examples that should get you started.

**Have fun!**


