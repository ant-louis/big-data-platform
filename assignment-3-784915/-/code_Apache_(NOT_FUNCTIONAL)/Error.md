# What is the problem ?
The problem happens in the Kafka Integration in Spark Streaming. Basically, Kafka is running in a Docker container, taken from the image *"wurstmeister/kafka:2.12-2.3.0"*, accessible from the inside (inside docker network) at *"kafka:9092"* and from the outside (outside docker network) at *"localhost:9094"* (see docker-compose.yml). Thus, the producer (clients/producer.py) sends records on *"localhost:9094"* (messages are well received by the broker, one can test it by consuming them with clients/consumer.py).

Now, Spark has to consume messages from Kafka container, so it has to access *"kafka:9092"*. The problem happens with this line of code:
````
direct_stream = KafkaUtils.createDirectStream(streaming_spark_context, ['user1'], {"metadata.broker.list": "kafka:9092", "auto.offset.reset":"smallest"})
````
Given me the error: *org.apache.spark.SparkException: java.nio.channels.ClosedChannelException*. So basically the problem is the connection to the Kafka broker.
Here is a screenshot of the error:

![error](error.png)


The topics *'user1'* and *'user2'* are automatically created when building the Docker containers thanks to the environment variable KAFKA_CREATE_TOPICS (see docker-compose.yml). One can easily check that *"kafka:9092"* is accessible and list the topics from it by running the following command in the Kafka Docker:
````
docker exec -ti kafka /bin/bash
kafka-topics.sh --list --bootstrap-server kafka:9092
````

About Spark, there are 3 types of Spark containers (Spark-master, Spark-worker, Spark-submit), all coming from an image built from *docker-spark/spark-base/Dockerfile*. This base image is stretch kernel with openjdk8 where Spark 2.4.4 with Hadoop 2.7 and Scala 2.11.2 was installed. When the user wants to start the streaming analytics, he runs the following command in *clients/*:
````
chmod +x ./my-app.sh
./my-app.sh
````
This will run the spark-submit docker which will starts itself by running its script *start-submit.sh* which basically does the following:
````
#/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 --master spark://spark-master:7077 /opt/spark-apps/customerstreamapp1.py
````
The *--packages* option is necessary to add spark-streaming-kafka-0-8_2.11 and its dependencies (for Python applications which lack SBT/Maven project management). The integration was implemented by following the instructions of the [official documentation](http://spark.apache.org/docs/latest/streaming-kafka-0-8-integration.html).


