#!/bin/bash
rasa run actions &
P1=$!
rasa run --model /app/models --enable-api \
        --endpoints /app/endpoints.yml \
        --enable-api \
        --cors “*”  &
P2=$!
python3 app.py &
P3=$!
wait $P1 $P2 $P3
