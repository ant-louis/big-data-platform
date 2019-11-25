import os
import argparse


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--iqueue', type=str, default='in1',
                        help='Name of the input queue. Default is in1.')
    parser.add_argument('--oqueue', type=str, default='out1',
                    help='Name of the output queue. Default is out1.')
    parser.add_argument('--parallelism', type=str, default='1',
                help='Level off parallelism for Flink. Default is 1.')
    args = parser.parse_args()
    return args


def run(args):
    """
    """
    # Run the analytics job
    os.system("docker exec -ti flink-jobmanager flink run /analyticsjob.jar --amqpurl rabbit  --iqueue "+args.iqueue+" --oqueue "+args.oqueue+" --parallelism "+args.parallelism)

if __name__ == "__main__":
    args = parse_arguments()
    run(args)
