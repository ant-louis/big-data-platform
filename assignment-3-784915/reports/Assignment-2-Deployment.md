# Deployment report

## Setup
The following section lists the requirements in order to start running the project.

This project is based on Docker containers, so ensure to have [Docker](https://docs.docker.com/v17.12/install/) installed on your machine. In addition, your machine should dispose from a working version of Python 3.6 as well as the following packages:
- [Cassandra Driver](https://docs.datastax.com/en/developer/python-driver/3.19/installation/)
- [Pandas](https://pypi.org/project/pandas/)
- [Numpy](https://pypi.org/project/numpy/)
- [Argparse](https://pypi.org/project/argparse/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [Tqdm](https://pypi.org/project/tqdm/)

These libraries can be installed automatically by running the following command in the *code/* repository:
```bash
pip install -r requirements.txt
```

## Launching the Docker containers
In order to run the containers, run the following command in the *code/* repository:
```bash
make install
```
Notice that downloading and installing the different images might take some time. Also, waiting a couple of minutes before executing operations on the Cassandra container is advised.


## Initializing the Cassandra database
In order to initialize the database according to the demo users created in the project, run the following command in the *code/mysimbdp-coredms* repository:
```bash
python init_db.py
```
Some optional parameters can be added to this line of code. However, it is recommended not to modify them for now, as this is how the container as been configured. For information, these parameters are:
* *--address*: List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].
* *--port*: The server-side port to open connections to. Default to 9042.
* *--username*: Username required to connect to Cassandra database. Default is 'cassandra'.
* *--password*: Password required to connect to Cassandra database. Default is 'cassandra'.


## Ingesting with batch
In order to ingest files initially stored locally on the machine of a client (client1 for e.g.), run the following command in the *code/clients/client1* directory:
```bash
python fetchdata.py
```
Some optional parameters can be added to this line of code. These parameters are:
* *--username*: Username of the client. Default is 'john_doe' for client1, 'jane_doe' for client2.
* *--password*: Password of the client. Default is '1234' for both clients.
* *--indir*: Path to the client-input-directory. Default is 'client-input-directory/'.


### Testing ingestion performances
In order to test the ingestion performances of the platform over the whole pipeline, run the following command in *code/clients/*:
```bash
python performances.py
```
One optional paramater can be added:
* *--nb_clients*: Number of clients to run the tests (either 1 or 2). Default is 1.