from multiprocessing import Process, Manager
import fetchdata_demo
import argparse
from argparse import Namespace
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import timeit
plt.style.use('ggplot')


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser("Init the Cassandra database.")

    parser.add_argument("--nb_clients", type=int, choices=[1,2], default=1,
                        help="Number of clients to run the tests.")
    args, _ = parser.parse_known_args()
    return args


def run_processes(n):
    """
    Run n processes that will simultaneously ingest data into database.
    """
    # Shared variable to get return values
    manager = Manager()
    return_dict = manager.dict()
    jobs = []

    # Run the n processes
    for i in range(n):
        print(i)
        if i == 0:
            args = Namespace(username='john_doe', password='1234', indir='client'+str(i+1)+'/client-input-directory')
        else:
            args = Namespace(username='jane_doe', password='1234', indir='client'+str(i+1)+'/client-input-directory')
        p = Process(target=fetchdata_demo.run, args=(args,))
        jobs.append(p)
        p.start()

    # Wait for all the processes to end
    for proc in jobs:
        proc.join()

    # Return time elapsed
    return return_dict.values()


def barplot(times, steps):
    """
    """
    bars = tuple([str(i)+' proc. ' for i in steps])
    x_pos = np.arange(len(bars))
    
    # Create bars
    _, ax = plt.subplots()
    ax.bar(x_pos, times, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(bars)
    ax.set_title('Time (s)', fontsize=13)
    
    # Show graphic
    plt.tight_layout()
    plt.savefig('../reports/figures/barplot.png')



if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()

    # Start timer
    start = timeit.default_timer()

    # Run N processes and get elapsed times
    run_processes(args.nb_clients)

    # End timer
    end = timeit.default_timer()
    elapsed_time = end-start
    print(elapsed_time)

    # # Draw barplot
    # steps = [args.nb_clients]
    # barplot(times, steps)
