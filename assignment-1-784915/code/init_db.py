from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse


def main(args):
    # Connect to database
    auth_provider = PlainTextAuthProvider(username=args.username, password=args.password)
    cluster = Cluster(contact_points=[args.address], port=args.port, auth_provider=auth_provider)
    session = cluster.connect()

    # Create keyspace
    session.execute("""
    CREATE  KEYSPACE IF NOT EXISTS mysimpbdp_coredms
    WITH REPLICATION = {
        'class' : 'SimpleStrategy', 
        'replication_factor' : 1 
    };
    """)

    # Create the table
    session.execute("""
    CREATE TABLE IF NOT EXISTS mysimpbdp_coredms.apps (
        id uuid PRIMARY KEY, 
        name text,
        category text,
        rating float,
        reviews int,
        size text,
        installs text,
        type text,
        price float,
        content_rating text,
        genres text,
        last_updated text,
        current_version text,
        android_version text
    );
    """)

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
                        help="The server-side port to open connections to. Defaults to 9042.")
    parser.add_argument("--username", type=str, default='cassandra',
                        help="The username required to connect to Cassandra database.")
    parser.add_argument("--password", type=str, default='cassandra',
                        help="The password required to connect to Cassandra database.")

    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
