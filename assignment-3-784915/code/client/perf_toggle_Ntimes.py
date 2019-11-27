import os, time, sys
import argparse
from multiprocessing import Process, Manager

import toggle


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

    # Launch the Flink apps
    for i in range(n):
        p = Process(target=toggle.start_job, args=("in"+str(i), "out"+str(i), str(1)))
        flink_jobs.append(p)
        p.start()

    # Wait for all the processes to end
    for proc in flink_jobs:
        proc.join()

    
if __name__ == "__main__":
    args = parse_arguments()
    run_jobs(args.nb_customers)
