from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse
import pandas as pd
import uuid
import timeit


def connect_db(args):
    """
    Connect to the database.
    """
    auth_provider = PlainTextAuthProvider(username=args.username, password=args.password)
    cluster = Cluster(contact_points=[args.address], port=args.port, auth_provider=auth_provider)
    session = cluster.connect()
    return cluster, session


def insert(df, session):
    """
    Insert the first 'nb_rows' rows of csv dataset to the database.
    """
    for i, row in df.iterrows():
        session.execute("""
        INSERT INTO mysimpbdp_coredms.apps (id, name, category, rating, reviews, size, installs, free, price_dollar, 
                                            content_rating, genres, last_updated, current_version, android_version)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
        (uuid.uuid1(), row['App'], row['Category'], row['Rating'], row['Reviews'], row['Size'], row['Installs'], row['Free'],
        row['Price_dollars'], row['Content Rating'], row['Genres'], row['Last Updated'], row['Current Ver'], row['Android Ver'])
        )


def run(args, i, return_dict):
    # Connect to database
    cluster, session = connect_db(args)

    # Read data from csv to database
    df = pd.read_csv(args.data, sep=',', index_col=0, dtype={'Rating': 'float64',
                                                            'Reviews': 'int64',
                                                            'Free': 'bool',
                                                            'Price_dollars':'float64',
                                                            'Last Updated':'str'})
    
    # Insert all dataframe into database and measure elapsed time
    start = timeit.default_timer()
    insert(df, session)
    end = timeit.default_timer()
    elapsed_time = end-start

    # Close cluster
    cluster.shutdown()

    # Store result of process i in shared variable return_dict
    return_dict[i] = elapsed_time

    return elapsed_time


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser("Init the Cassandra database.")

    parser.add_argument("--address", type=str, default='0.0.0.0',
                        help="List of contact points to try connecting for cluster discovery.")
    parser.add_argument("--port", type=int, default=9042,
                        help="Server-side port to open connections to. Defaults to 9042.")
    parser.add_argument("--username", type=str, default='cassandra',
                        help="Username required to connect to Cassandra database.")
    parser.add_argument("--password", type=str, default='cassandra',
                        help="Password required to connect to Cassandra database.")
    parser.add_argument("--data", type=str, default='../data/googleplaystore_clean.csv',
                        help="Path to the dataset. Default is ../data/googleplaystore_clean.csv")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    print(run(args, 0, [0]))
