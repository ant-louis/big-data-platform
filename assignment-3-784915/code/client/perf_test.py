import os, time, sys
import argparse
from multiprocessing import Process, Manager
import timeit

import produce
import consume


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--nb_customers', type=int, default=2,
                        help='Number of customers to consider for the test. Default is 2.')
    args = parser.parse_args()
    return args


def make_test(n):
    """
    """
    jobs = []

    # Start timer
    start = timeit.default_timer()

    # Produce data for each customer
    for i in range(n):
        # Create the process
        produce = Process(target=produce.run, args=("in"+str(i), '../../data/subdatasets/subdataset_47.csv'))
        consume = Process(target=consume.run, args=("out"+str(i),))

        # Add them to the list
        jobs.append(produce)
        jobs.append(consume)

        # Start them
        produce.start()
        consume.start()

    # Wait for all the processes to end
    for proc in jobs:
        proc.join()

    # End timer
    end = timeit.default_timer()
    elapsed_time = end-start

    return elapsed_time


    
if __name__ == "__main__":
    args = parse_arguments()
    time = make_test(args.nb_customers)
    print("Analytics time for {} customers: {}".format(args.nb_customers, time))
