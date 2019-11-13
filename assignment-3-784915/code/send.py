#!/usr/bin/env python
import pika, os, logging, sys, time
import argparse

def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue_name', type=str, help='queue name')
    parser.add_argument('--input_file', help='csv data file')
    args = parser.parse_args()
    return args


def run(args):
    """
    """
    # Connect to the channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=args.queue, durable=True)

    # Send data line by line
    f = open(args.input_file, 'r')
    f.readline()
    for line in f:
        print ("Send a line")
        print ("-----------------------")
        channel.basic_publish(exchange='', routing_key=args.queue_name, body=line)
        time.sleep(1)

    # Close connection
    connection.close()


if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()
    run(args)
