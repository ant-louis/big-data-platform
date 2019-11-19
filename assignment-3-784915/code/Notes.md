To run app:
````
/spark/bin/spark-submit --master spark://spark-master:7077 --class \
    org.apache.spark.examples.SparkPi \
    /spark/examples/jars/spark-examples_2.11-2.4.0.jar 1000
````

# Start spark job
```
spark-submit --class org.sevenmob.spark.streaming.DirectKafkaProcessing \
     --master local[*] target/scala-2.10/TwitterProcessingPipeLine-assembly-0.1.jar \
     $KAFKA_ENV_KAFKA_ADVERTISED_HOST_NAME:$KAFKA_PORT_9092_TCP_PORT \
     $KAFKA_TOPIC_NAME \
     $CASSANDRA_PORT_9042_TCP_ADDR \
     $GOOGLE_GEOCODING_API_KEY
```



````
./bin/spark-submit \
  --master spark://207.184.161.138:7077 \
  examples/src/main/python/pi.py \
  1000
```