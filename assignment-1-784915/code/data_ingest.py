from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse
import pandas as pd
import uuid


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
    for index, row in df.iterrows():
        # if index >= 1000:
        #     break
        # else:
        session.execute("""
        INSERT INTO mysimpbdp_coredms.apps (id, name, category, rating, reviews, size, installs, free, price_dollar, 
                                            content_rating, genres, last_updated, current_version, android_version)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
        (uuid.uuid1(), row['App'], row['Category'], row['Rating'], row['Reviews'], row['Size'], row['Installs'], row['Free'],
        row['Price_dollars'], row['Content Rating'], row['Genres'], row['Last Updated'], row['Current Ver'], row['Android Ver'])
        )


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

    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Connect to database
    cluster, session = connect_db(args)

    # Insert data from csv to database
    df = pd.read_csv(args.data, sep=',', index_col=0, dtype={'Rating': 'float64',
                                                            'Reviews': 'int64',
                                                            'Free': 'bool',
                                                            'Price_dollars':'float64',
                                                            'Last Updated':'str'})
    insert(df, session)

    # Close cluster
    cluster.shutdown()
