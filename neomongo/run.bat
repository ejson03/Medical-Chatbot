@echo "Docker-Compose launched"
@docker-compose up -d
@echo "Should we perform Replicaset initialization?"
@echo "Wait for a small duration before going ahead"
@pause
@docker exec -ti neomongo_mongo_1 mongo --eval "rs.initiate()"
@echo "Replicaset initialization done"
@echo "Docker-Compose relaunched"
@docker-compose up -d
@echo "Should we terminate?"
@pause
