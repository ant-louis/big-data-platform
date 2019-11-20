To submit a job:
````
#/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 --master spark://spark-master:7077 /opt/spark-apps/customerstreamapp1.py
````

````
bin/spark-submit — packages org.apache.spark:spark-streaming-kafka-0–8_2.11:2.0.0 spark-direct-kafka.py localhost:9092 new_topic
````



Pour Spark, je fais [Direct Approach](http://spark.apache.org/docs/latest/streaming-kafka-0-8-integration.html) -> noter les avantages dans le rapport notamment au niveau du parallélisme (c'est une question dans le rapport).

For Python applications which lack SBT/Maven project management, spark-streaming-kafka-0-8_2.12 and its dependencies can be directly added to spark-submit using --packages. That is,
````
 ./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.12:2.4.4 ...
 ````



 ````
kafka-topics.sh --list --bootstrap-server kafka:9092
````