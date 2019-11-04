# Deployment report

## Setup
The following section lists the requirements in order to start running the project.

This repository contains docker-compose file which uses the Cassandra container and encapsulates some dependencies. Then, ensure to have [Docker](https://docs.docker.com/v17.12/install/) installed on your machine. If so, run the following command to download the [Cassandra image](https://hub.docker.com/_/cassandra):
```bash
docker pull cassandra
```

This project uses Python 3.6 and the following packages are needed for the project to run properly:
- [Cassandra Driver](https://docs.datastax.com/en/developer/python-driver/3.19/installation/)
- [Pandas](https://pypi.org/project/pandas/)
- [Numpy](https://pypi.org/project/numpy/)
- [Argparse](https://pypi.org/project/argparse/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [Tqdm](https://pypi.org/project/tqdm/)

You can automatically download these libraries by running:
```bash
pip install -r requirements.txt
```


## Dataset
The choosen dataset for this project, [Google Play Store Apps](https://www.kaggle.com/lava18/google-play-store-apps), is a public dataset from Kaggle regrouping data about 10k Play Store apps. Each app (row) has values for catergory, rating, size, and more. This dataset was not perfectly cleaned, so a new one was creating from it to better match my application. This clean dataset can be obtained by running:
```bash
python clean_data.py
```

## Initialize mysimbdp-coredms
1. Create the container with Cassandra database pre-installed. Simply run the docker-compose file:
```bash
docker-compose up -d
```

2. Create the keyspace 'mysimdbp-coredms' and the main table 'apps'. Simply run:
```bash
python init.py
```
Some optionnal parameters can be added to this line of code:
* *--address*: List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].
* *--port*: The server-side port to open connections to. Default to 9042.
* *--username*: Username required to connect to Cassandra database. Default is 'cassandra'.
* *--password*: Password required to connect to Cassandra database. Default is 'cassandra'.

## Data ingestion
The following command will ingest the complete **'googleplaystore_clean.csv'** dataset (10840 rows) into the Cassandra database:
```bash
python data_ingest.py
```
Some optionnal parameters can be added to this line of code:
* *--address*: List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].
* *--port*: The server-side port to open connections to. Default to 9042.
* *--username*: Username required to connect to Cassandra database. Default is 'cassandra'.
* *--password*: Password required to connect to Cassandra database. Default is 'cassandra'.
* *--data*: Path to the dataset. Default is '../data/googleplaystore_clean.csv'.


## Testing mysimdbp-coredms performances
The following command will test the performances of n concurrent mysimbdp-dataingest pushing data into mysimbdp-coredms:
```bash
python test_perf.py
```
Some optionnal parameters can be added to this line of code:
* *--address*: List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].
* *--port*: The server-side port to open connections to. Default to 9042.
* *--username*: Username required to connect to Cassandra database. Default is 'cassandra'.
* *--password*: Password required to connect to Cassandra database. Default is 'cassandra'.
* *--data*: Path to the dataset. Default is '../data/googleplaystore_clean.csv'.
