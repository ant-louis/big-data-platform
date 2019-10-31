import urllib.request
from os import listdir, path, system
import argparse
import json


def ingest(client_id):
    """
    Once fetching is done, ingest data to mysimbdp-coredms.
    """
    # Get files of client saved on the server
    files_path = client_id+'/files/'
    files = [f for f in listdir(files_path) if path.isfile(path.join(files_path, f))]


    # Get batchingestapp of client
    ingestapp_path = client_id +'/clientbatchingestapp.py'

    # Ingest each file
    for f in files:
        msg = "python "+ingestapp_path+" "+files_path+f+" "+client_id
        print(msg)
        # result = system("python "+ingestapp_path+" "+files_path+f+" "+client_id)
        # if result != 0:
        #     print('Problem while ingesting {}.'.format(f))
        #     return '-1'
    return '0'


if __name__ == '__main__':
    code = ingest('dir1')

    

    # python dir1/clientbatchingestapp.py dir1/files/sample10.csv dir1