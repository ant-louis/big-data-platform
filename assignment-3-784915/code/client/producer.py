#!/usr/bin/env python
import pika, os, logging, sys, time
import argparse



def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue_name', type=str, default='test',
                        help='Name of the queue. Default is test.')
    parser.add_argument('--input_file', type=str, default='../../data/subdatasets/subdataset_0.csv',
                        help='Path to the csv data file. Default is ../../data/subdatasets/subdataset_0.csv')
    args = parser.parse_args()
    return args


def run(args):
    """
    """
    # Connect to the channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue=args.queue_name, durable=True)  # mark both the queue and messages as durable to make sure that messages aren't lost.

    # Send data line by line
    f = open(args.input_file, 'r')
    f.readline()
    for line in f:
        print ("Send a line")
        print ("-----------------------")
        channel.basic_publish(exchange='',
                                routing_key=args.queue_name,
                                body=line,
                                properties=pika.BasicProperties(
                                    delivery_mode = 2, # make message persistent
                            ))
        time.sleep(1)

    # Close connection
    connection.close()


# def delete(args):
#     """
#     """
#     connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit'))
#     channel = connection.channel()
#     channel.queue_delete(queue=args.queue_name)
#     connection.close()


if __name__ == "__main__":
    args = parse_arguments()
    run(args)
