from multiprocessing import Process, Manager
import data_ingest
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
plt.style.use('ggplot')


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser("Init the Cassandra database.")

    parser.add_argument("--address", type=str, default='0.0.0.0',
                        help="List of contact points to try connecting for cluster discovery.")
    parser.add_argument("--port", type=int, default=9042,
                        help="Server-side port to open connections to. Defaults to 9042.")
    parser.add_argument("--username", type=str, default='cassandra',
                        help="Username required to connect to Cassandra database.")
    parser.add_argument("--password", type=str, default='cassandra',
                        help="Password required to connect to Cassandra database.")
    parser.add_argument("--data", type=str, default='../data/googleplaystore_clean.csv',
                        help="Path to the dataset. Default is ../data/googleplaystore_clean.csv")
    parser.add_argument("--runonly", type=int, default=2,
                        help="Number of processes that will ingest the entire dataset to Cassandra database.")
    parser.add_argument("--runfrom", type=int,
                        help="Starting number of processes that will ingest the entire dataset to Cassandra database.")

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
        p = Process(target=data_ingest.run, args=(args, i, return_dict))
        jobs.append(p)
        p.start()

    # Wait for all the processes to end
    for proc in jobs:
        proc.join()

    # Return time elapsed
    return return_dict.values()


def convert_time2speed(times):
    """
    """
    len_df = 10840
    speeds = [len_df/x for x in times]
    return speeds


def barplot(means, std, steps):
    """
    """
    bars = tuple([str(i)+' processes' for i in steps])
    x_pos = np.arange(len(bars))
    
    # Create bars
    _, ax = plt.subplots()
    ax.bar(x_pos, means, yerr=std, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(bars)
    ax.set_title('Speed (insertions/s)', fontsize=13)
    
    # Show graphic
    plt.tight_layout()
    plt.savefig('plots/barplot.png')



if __name__ == '__main__':
    # Parse arguments
    args = parse_arguments()

    # Run 1,5,...,N processes consecutively and store stats
    if args.runfrom is not None:
        steps = np.arange(args.runfrom, 0, -5)
        mean = np.zeros(len(steps))
        std = np.zeros(len(steps))
        for i, nb in enumerate(tqdm(steps)):
            # Run i processes and get elapsed times
            times = run_processes(nb)

            # Convert to insertions/s
            speeds = convert_time2speed(times)

            # Get stats
            mean[i] = np.mean(speeds)
            std[i] = np.std(speeds)

    # Run only N processes
    else:
        # Run N processes and get elapsed times
        times = run_processes(args.runonly)

        # Convert to insertions/s
        speeds = convert_time2speed(times)

        # Get stats
        steps = [args.runonly]
        mean = np.zeros(len(steps))
        std = np.zeros(len(steps))
        mean[0] = np.mean(speeds)
        std[0] = np.std(speeds)
    
    # Draw barplot
    barplot(mean, std, steps)
