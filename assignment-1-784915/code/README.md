# Guidelines

## Setup
The following section lists the requirements in order to start running the project.

This repository contains docker-compose file which uses the Cassandra container and encapsulates some dependencies. Then, ensure to have installed on your machine:
- [Docker](https://docs.docker.com/v17.12/install/)
- [Cassandra image](https://hub.docker.com/_/cassandra)

This project uses Python 3.6 and the following packages are needed for the project to run properly:
- [Pandas](https://pypi.org/project/pandas/)
- [Argparse](https://pypi.org/project/argparse/)
- [Cassandra Driver for Python](https://docs.datastax.com/en/developer/python-driver/3.19/installation/)


## Dataset
The choosen dataset for this project, [Google Play Store Apps](https://www.kaggle.com/lava18/google-play-store-apps), is a public dataset from Kaggle regrouping data about 10k Play Store apps. Each app (row) has values for catergory, rating, size, and more. 

This dataset was not perfectly cleaned, so a new one was creating from it to better match our application. This clean dataset can be obtained by running:
```bash
python clean_data.py
```


## Quick Start Guide
1. Run the docker-compose file to create the container with Cassandra pre-installed:
```bash
docker-compose up -d
```

2. Initialize the database mysimdbp-coredms:
```bash
python init.py
```

3. Ingest data from **'googleplaystore_clean.csv'** to the database:
```bash
python data_ingest.py
```
