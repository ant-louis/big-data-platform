#!/usr/bin/env python
import pika, os, logging, sys, time
import argparse
import random


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue_name', type=str, default='out1',
                        help='Name of the queue. Default is out1.')                  
    args = parser.parse_args()
    return args


def callback(ch, method, properties, body):
    """
    """
    print ("Received:", body, sep=" ")
    #ch.basic_ack(delivery_tag = method.delivery_tag)  # acknowledgment for the task


def run(args):
    """
    """
    # Connect to the channel
    print("Connecting to the channel {}...".format(args.queue_name))
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=args.queue_name, durable=False)
    except Exception as e:
        print("Connection to {} failed! Error: {}".format(args.queue_name, e))
    print("Connected !")

    # Don't give more than one message to a worker at a time.
    #channel.basic_qos(prefetch_count=1)

    # Consume messages
    print('Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue=args.queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

    # Close connection
    print("Closing connection to the channel {}...".format(args.queue_name))
    connection.close()


if __name__ == "__main__":
    args = parse_arguments()
    run(args)
