from multiprocessing import Pool, TimeoutError, Process
import os

def run_process(process):
    """
    Run a process.
    """                                                             
    os.system('python {}'.format(process))


if __name__ == "__main__":
    processes = []
    processes.append('batchingestmanager.py')
    #processes.append('streamingestmanager.py')
    pool = Pool(processes=2)
    pool.map(run_process, processes)