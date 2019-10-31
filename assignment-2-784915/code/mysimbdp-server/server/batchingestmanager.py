#coding: utf-8
from flask import Flask, request, jsonify
from os import listdir, path, system
import json


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
    # Get files of client saved on the server
    files_path = client_id+'/files/'
    files = [f for f in listdir(files_path)]

    # Get batchingestapp of client
    ingestapp_path = client_id +'/clientbatchingestapp.py'

    # Ingest each file
    for f in files:
        result = system("python "+ingestapp_path+" "+files_path+f+" "+client_id)
        if result != 0:
            print('Problem while ingesting {}.'.format(f))
            return '-1'
    return '0'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')