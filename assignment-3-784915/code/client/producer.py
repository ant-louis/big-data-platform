import os, logging, sys, time
import argparse
from kafka import KafkaProducer
import json


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic_name', type=str, default='test_topic',
                        help='Name of the topic. Default is test_topic.')
    parser.add_argument('--input_file', type=str, default='../../data/subdatasets/subdataset_0.csv',
                        help='Path to the csv data file. Default is ../../data/subdatasets/subdataset_0.csv')
    args = parser.parse_args()
    return args


def run(args):
    """
    Run the producer demo.
    """
    # Create producer that connects to Kafka server running in Docker.
    producer = KafkaProducer(
        bootstrap_servers='localhost:9093', 
        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # Send data line by line
    f = open(args.input_file, 'r')
    f.readline()
    for line in f:
        print ("Send a line")
        print ("-----------------------")
        producer.send(args.topic_name, value=line)
        time.sleep(1)


if __name__ == "__main__":
    args = parse_arguments()
    run(args)