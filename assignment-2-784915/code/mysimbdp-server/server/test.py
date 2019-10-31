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
    files = [f for f in listdir(files_path)]

    # Get batchingestapp of client
    ingestapp_path = client_id + '/clientbatchingestapp.py'

    #
    system("python "+ingestapp_path+" "+files_path+files[0]+" "+client_id)

    # # Ingest each file
    # for f in files:
    #     result = system("python "+ingestapp_path+" --data=" + files_path+f)
    #     if result != 0:
    #         print('Problem while ingesting {}.'.format(f))
    #         return 1
    return 200


if __name__ == '__main__':
    code = ingest('dir1')