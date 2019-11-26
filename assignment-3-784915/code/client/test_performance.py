import os, time
import argparse
from multiprocessing import Process, Manager

import toggle
import produce


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--nb_customers', type=int, default=10,
                        help='Number of customers to consider for the test. Default is 10.')
    args = parser.parse_args()
    return args


def run_jobs(n):
    """
    Run n processes that will execute the Flink job.
    """
    for i in range(n):
        os.system("python toggle.py --iqueue=in"+str(i)+" --oqueue=out"+str(i)+" --parallelism=1 &")
    # jobs = []
    # for i in range(n):
    #     p = Process(target=toggle.start_job, args=("in"+str(i), "out"+str(i), str(1)))
    #     jobs.append(p)
    #     p.start()
    
    # # Wait for all the processes to end
    # for proc in jobs:
    #     proc.join()

    
if __name__ == "__main__":
    args = parse_arguments()

    # Launch n analytics job simulating n users
    run_jobs(args.nb_customers)
    time.sleep(2)

    # # Get production throughput for one customer
    # input_file = '../../data/subdatasets/subdataset_47.csv'
    # emission_rate = produce.run("in1", input_file)
    # print(emission_rate)



    # Get consumption throughput for the same customer

    
    
    # Compare them