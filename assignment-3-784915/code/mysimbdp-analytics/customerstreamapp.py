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
