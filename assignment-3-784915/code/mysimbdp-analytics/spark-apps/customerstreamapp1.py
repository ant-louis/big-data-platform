import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def my_function():
    """
    """
    lambda x: print(x)
    # #--------------------------------------------------------
    # lines = kvs.map(lambda x: x[1])
    # counts = lines.flatMap(lambda line: line.split(“ “)) \
    #               .map(lambda word: (word, 1)) \
    #               .reduceByKey(lambda a, b: a+b)
    # counts.pprint()
    # #--------------------------------------------------------



if __name__ == "__main__":
    # Initialize sparkcontext
    spark_context = SparkContext(appName='customerstreamapp1')

    # Initialize streaming context
    streaming_spark_context = StreamingContext(spark_context, 1) # 1s is the batch duration

    # Fetch data from Kafka topics
    direct_stream = KafkaUtils.createDirectStream(streaming_spark_context, ['user1'], {"metadata.broker.list": "kafka:9092", "auto.offset.reset":"smallest"})

    # Transformation
    lines = direct_stream.map(lambda x: x[1])
    lines.pprint()

    # Managing the Pipeline
    streaming_spark_context.start()     
    streaming_spark_context.awaitTermination()
