import pika, os, logging, sys, time
import argparse
import timeit



def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--queue_name', type=str, default='in1',
                        help='Name of the queue. Default is in1.')
    parser.add_argument('--input_file', type=str, default='../../data/subdatasets/subdataset_12.csv',
                        help='Path to the csv data file. Default is ../../data/subdatasets/subdataset_12.csv')
    args = parser.parse_args()
    return args


def run(queue_name, input_file):
    """
    """
    # Connect to the channel
    print("Connecting to the channel {}...".format(queue_name))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)  # mark both the queue and messages as durable to make sure that messages aren't lost.
    print("Connected !")


    # Send data line by line
    print("Sending data from {}...".format(input_file))
    f = open(input_file, 'r')
    f.readline()  # Consume header

    # Start timing
    start = timeit.default_timer()
    counter = 0
    for line in f:
        print ("Send a line")
        print ("-----------------------")
        channel.basic_publish(exchange='',
                                routing_key=queue_name,
                                body=line,
                                properties=pika.BasicProperties(
                                    delivery_mode = 2, # make message persistent
                            ))
        time.sleep(1)
        counter += 1

    # End timing, get elapsed time and compute emission throughput
    end = timeit.default_timer()
    elapsed_time = end-start
    throughput = counter/elapsed_time

    # Close connection
    print("Closing connection to the channel {}...".format(queue_name))
    connection.close()

    # Return throuhput rate
    return throughput


if __name__ == "__main__":
    args = parse_arguments()
    run(args.queue_name, args.input_file)
