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


### 2. Deploy the streaming analytics app
In this demo, the customer Java app has been compiled into a *.jar* file available in *code/client/customerstreamapp/target/CustomerStreamApp-0.1-SNAPSHOT.jar*. To deploy this app on the Flink Job Manager, run the following command in the *code/client/customerstreamapp/* repository:
```bash
docker cp target/CustomerStreamApp-0.1-SNAPSHOT.jar flink-jobmanager:/analyticsjob.jar
```
This will copy the *.jar* file to the Docker container in order to run it when the customer wants to.

In the case where the customer would want to modify his customerstreamapp Java project, he must first recompile his project by running the following command in the *code/client/customerstreamapp/* repository:
```bash
mvn install
```
Then, he must copy the new *.jar* file to the Flink Job Manager Docker as previously explained.


### 3. Start the streaming analytics job
In order to start the streaming analytics for the customer's data, run the following command in the *code/client/* repository:
```bash
python toggle.py
```
Some optional parameters can be added to this line of code:
* *---iqueue*: Name of the input queue. Default is in1.
* *--oqueue*: Name of the output queue. Default is out1.
* *--parallelism*: Level off parallelism for Flink. Default is 1.


### 4. Produce data
In order to simulate the production of data that is sent to the message broker, run the following command in the *code/clients/* repository:
```bash
python produce.py
```
Some optional parameters can be added to this line of code:
* *--queue_name*: Name of the queue. Default is in1.
* *--input_file*: Path to the csv data file. Default is '../../data/subdatasets/subdataset_12.csv'. It's a subdataset of about 10000 lines from the original *'bts-data-alarm-2017.csv* (which has been sorted by timestamp), where some bad lines (bad format) have intentionally been added to test the deserialization of such formats.



### 5. Consume analytics results
In order to consume the analytical messages computed with the customerstreamapp that queued in the output channel of the customer, run the following command in the *code/clients/* repository:
```bash
python consume.py
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
