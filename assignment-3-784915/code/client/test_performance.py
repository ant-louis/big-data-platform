import os, time, sys
import argparse
from multiprocessing import Process, Manager
import timeit

import toggle
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


def run_jobs(n):
    """
    Run n processes that will execute the Flink job.
    """
    flink_jobs = []
    produce_jobs = []
    consume_jobs = []

    # Launch the Flink apps
    for i in range(n):
        p = Process(target=toggle.start_job, args=("in"+str(i), "out"+str(i), str(1)))
        flink_jobs.append(p)
        p.start()
    # Wait for all the processes to end
    for proc in flink_jobs:
        proc.join()

    # Produce data for each customer
    for i in range(n):
        p = Process(target=produce.run, args=("in"+str(i), '../../data/subdatasets/subdataset_47.csv'))
        produce_jobs.append(p)
        p.start()
    # Wait for all the processes to end
    for proc in produce_jobs:
        proc.join()

    # Consume in Flink
    start = timeit.default_timer()
    for i in range(n):
        p = Process(target=consume.run, args=("out"+str(i),))
        consume_jobs.append(p)
        p.start()
    # Wait for all the processes to end
    for proc in consume_jobs:
        proc.join()
    end = timeit.default_timer()
    elapsed_time = end-start

    return elapsed_time


    
if __name__ == "__main__":
    args = parse_arguments()

    # Launch n analytics job simulating n users
    time = run_jobs(args.nb_customers)
    print("Analytics time for {} customers: {}".format(args.nb_customers, time))
