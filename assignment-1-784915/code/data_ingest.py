from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse
from datetime import datetime
import csv

def connect_db(args):
    """
    Connect to the database.
    """
    auth_provider = PlainTextAuthProvider(username=args.username, password=args.password)
    cluster = Cluster(contact_points=[args.address], port=args.port, auth_provider=auth_provider)
    session = cluster.connect()
    return cluster, session


def insert(session, data_path, nb_rows):
    """
    Insert the first 'nb_rows' rows of csv dataset to the database.
    """
    with open(data_path) as csv_file:
        # Read csv and skip the header
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)

        # Insert rows to db
        line_count = 0
        for row in csv_reader:
            session.execute("""
            INSERT INTO apps(username,name,city,age) VALUES ('aali24','Ali Amin','Karachi',34);
            """)
            
        



def main(args):
    # Connect to database
    cluster, session = connect_db(args)

    # Insert data from csv to database
    insert(session, args.data, 10)



    # Close cluster
    cluster.shutdown()


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
    parser.add_argument("--data", type=str, default='../data/googleplaystore.csv',
                        help="Path to the dataset. Default is ../data/googleplaystore.csv")

    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
