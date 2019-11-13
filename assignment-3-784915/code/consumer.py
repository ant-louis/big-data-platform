#!/usr/bin/env python
import pika, os, logging, sys, time
import argparse
import random


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue_name', type=str, help='queue name')
    parser.add_argument('--input_file', help='csv data file')
    args = parser.parse_args()
    return args


def callback(ch, method, properties, body):
    """
    """
    print ("Received:", body, sep=" ")


def run(args):
    """
    """
    # Connect to the channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=args.queue, durable=False)


    # Consume messages
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    # Close connection
    connection.close()


if __name__ == "__main__":
    args = parse_arguments()
    run(args)
