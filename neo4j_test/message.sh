curl --request POST \
  --url http://localhost:5005/webhooks/rest/webhook \
  --header 'content-type: application/json' \
  --data '{
      
"sender_id": "dddd",
  "message": "Bored"
}'