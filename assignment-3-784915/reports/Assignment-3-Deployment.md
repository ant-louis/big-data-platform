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
###  1. Launch the Docker containers
In order to run the containers, run the following command in the *code/* repository:
```bash
make install
```
Notice that downloading and installing the different images might take some time. Also, wait a couple of seconds before executing any operations. After running the command, four containers should be running:
* *rabbit*: the RabbitMQ Message Broker;
* *cassandra*: the Cassandra database;
* *flink-jobmanager*: the Job Manager for the Flink analytics;
* *flink-taskmanager*: one Task Manager for the Flink analytics;

Note that UI are available for Flink and RabbitMQ in your web browser at *'localhost:8081'* and *'localhost:15672'* respectively. See more details on the ports and access in the *docker-compose.yml* file. 


### 2. Start the streaming analytics
In order to start the streaming analytics job of our demo customer, run the following commands in the *code/client/customerstreamapp/* repository:
```bash
chmod +x start-analytics.sh
./start-analytics.sh
```
This will first copy the *.jar* file of the customerstreamapp to the Flink Job Manager, and then run it by creating two queues for the customer: the input queue of the stream *'in1* and the output queue *'out1'*. Once the job is launched, Flink will listen at *'in1* for incoming records to process. After the processing, it will send its analytics to *'out1* which can later be consumed by the customer.


### 3. Sending data to the Message Broker
In order to simulate the production of data that is sent to the message broker, run the following command in the *code/clients/* repository:
```bash
python producer.py
```
Some optional parameters can be added to this line of code:
* *--queue_name*: Name of the queue. Default is in1.
* *--input_file*: Path to the csv data file. Default is '../../data/subdatasets/subdataset_12.csv'. It's a subdataset of about 10000 lines from the original *'bts-data-alarm-2017.csv* (which has been sorted by timestamp), where some bad lines (bad format) have intentionally been added to test the deserialization of such formats.



### 4. Consuming data from the Message Broker
In order to consume the analytical messages computed with the customerstreamapp that queued in the output channel of the customer, run the following command in the *code/clients/* repository:
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
