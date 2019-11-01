#coding: utf-8
from flask import Flask, request, jsonify
from os import listdir, path, system
import json
import logging
import timeit


app = Flask(__name__)


@app.route('/login/<username>/<password>')
def login(username, password):
    """
    Check password of user and returns corresponding directory if matches.
    """
    f = open('users.json')
    users_data = json.load(f)
    f.close()

    client_dir = ""
    for (k, v) in users_data.items():
        if str(username) == v['username']:
            if str(password) == v['password']:
                client_dir = v['client_dir']
            else:
                return '-1'

    if not client_dir:
        return '-1'
    
    return client_dir


@app.route('/constraints/<client_id>')
def get_constraints(client_id):
    """
    Given client_id, send back corresponding constraints.
    """
    constraints = {}
    with open(client_id+'/customer_profile.json') as f:
        constraints = json.load(f)
        f.close()
    return jsonify(constraints)


@app.route('/ingest/<client_id>')
def ingest(client_id):
    """
    Once fetching is done, ingest data to mysimbdp-coredms.
    """
    # Config the log file
    logging.basicConfig(level=logging.INFO, filename='server.log', filemode='a', format='%(asctime)s :: %(levelname)s :: %(name)s : %(message)s')

    # Get files of client saved on the server
    files_path = client_id+'/files/'
    files = [f for f in listdir(files_path) if path.isfile(path.join(files_path, f))]

    # Get batchingestapp of client
    ingestapp_path = client_id +'/clientbatchingestapp.py'

    # Ingest each file
    for f in files:
        # Start timer
        start = timeit.default_timer()

        # Get size of file
        size = path.getsize(files_path+f)

        # Ingestion
        result = system("python "+ingestapp_path+" "+files_path+f+" "+client_id)

        # End timer
        end = timeit.default_timer()
        elapsed_time = end-start

        # Ingestion failed
        if result != 0:
            logging.warning('Problem while ingesting {}.'.format(f))
            return '-1'
        else:
            # Ingestion suceed
            logging.info('{} was correctly ingested into mysimbdp-coredms. File size: {} KB -- Total ingestion time: {} -- '.format(f, size, elapsed_time))

    return '0'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')