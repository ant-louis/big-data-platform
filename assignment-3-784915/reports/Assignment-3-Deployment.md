# Deployment report

## Setup
The following section lists the requirements in order to start running the project.

This project is based on Docker containers, so ensure to have [Docker](https://docs.docker.com/v17.12/install/) installed on your machine. In addition, your machine should dispose from a working version of Python 3.6 as well as the following packages:
- [cassandra-driver](https://pypi.org/project/cassandra-driver/)
- [pandas](https://pypi.org/project/pandas/)
- [numpy](https://pypi.org/project/numpy/)
- [argparse](https://pypi.org/project/argparse/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [tqdm](https://pypi.org/project/tqdm/)
- [pika](https://pypi.org/project/pika/)

These libraries can be installed automatically by running the following command in the *code/* repository:
```bash
pip install -r requirements.txt
```

## Deployment

###  1. Launching the Docker containers
In order to run the containers, run the following command in the *code/* repository:
```bash
make install
```
Notice that downloading and installing the different images might take some time. Also, waiting a couple of seconds before executing any operations.


### 2. Sending data to the Message Broker
In order to simulate the production of data that is sent to the message broker, run the following command in the *code/clients/* repository:
```bash
python producer.py
```
Some optional parameters can be added to this line of code:
* *--queue_name*: Name of the queue. Default is in1.
* *--input_file*: Path to the csv data file. Default is '../../data/bts-data-alarm-2017.csv'



### 3. Consuming data from the Message Broker
In order to simulate the production of data that is sent to the message broker, run the following command in the *code/clients/* repository:
```bash
python consumer.py
```
Some optional parameters can be added to this line of code:
* *--queue_name*: Name of the queue. Default is out1.



### (Optional) Initializing the Cassandra database
In order to initialize the database according to the demo users created in the project, run the following command in the *code/mysimbdp-coredms* repository:
```bash
python init_db.py
```
Some optional parameters can be added to this line of code. However, it is recommended not to modify them for now, as this is how the container as been configured. For information, these parameters are:
* *--address*: List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].
* *--port*: The server-side port to open connections to. Default to 9042.
* *--username*: Username required to connect to Cassandra database. Default is 'cassandra'.
* *--password*: Password required to connect to Cassandra database. Default is 'cassandra'.





## 
````
mvn install
docker cp target/mysimbdp-0.1-SNAPSHOT.jar flink-jobmanager:/job_user1.jar
docker exec -ti flink-jobmanager flink run /job_user1.jar --amqpurl rabbit  --iqueue in1 --oqueue out1 --parallelism 1
````

