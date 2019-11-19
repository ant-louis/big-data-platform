from kafka import KafkaConsumer
import json


while True:

    # initialize consumer to given topic and broker
    consumer = KafkaConsumer(
        'test_topic',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        bootstrap_servers='localhost:9093')
    
    # Loop and print messages
    for m in consumer:
        print(m.value)









import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    sc = SparkContext(appName='customerstreamapp')
    ssc = StreamingContext(sc, 2)
    kvs = KafkaUtils.createDirectStream(ssc, ['test_topic:2:1'], {"bootstrap.servers": 'kafka:9092'})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(“ “)) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()
    ssc.start()
    ssc.awaitTermination()
