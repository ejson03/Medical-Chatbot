until mongo --host mongo --eval "print(\"waited for connection\")"
do
    sleep 1
done

mongo --host mongo --eval "rs.initiate()"
