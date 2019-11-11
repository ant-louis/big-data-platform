from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse


def connect_db(args):
    """
    Connect to the database.
    """
    auth_provider = PlainTextAuthProvider(username=args.username, password=args.password)
    cluster = Cluster(contact_points=[args.address], port=args.port, auth_provider=auth_provider)
    session = cluster.connect()
    return cluster, session


def init_keyspace(session):
    """
    Init keyspace and create table.
    """
    # Creating keyspace
    session.execute("""
    CREATE  KEYSPACE IF NOT EXISTS mysimpbdp_coredms
    WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
    };
    """)
    
    # Creating tables
    session.execute("""
    CREATE TABLE IF NOT EXISTS mysimpbdp_coredms.data(
    id UUID PRIMARY KEY,
    station_id bigint,
    datapoint_id int,
    alarm_id int,
    event_time timestamp,
    value float,
    valueThreshold float,
    isActive Boolean
    );
    """)
    
    session.execute("""
    CREATE TABLE IF NOT EXISTS mysimpbdp_coredms.sensors(
    id int PRIMARY KEY,
    sensor varchar
    );
    """)
    
    session.execute("""
    CREATE TABLE IF NOT EXISTS mysimpbdp_coredms.alarms(
    id int PRIMARY KEY,
    alarm varchar
    );
    """)


def parse_arguments():
    """
    :return: the different arguments of the command line.
    """
    parser = argparse.ArgumentParser("Init the Cassandra database.")
    parser.add_argument("--address", type=str, default='0.0.0.0',
                        help="List of contact points to try connecting for cluster discovery. Default is [0.0.0.0].")
    parser.add_argument("--port", type=int, default=9042,
                        help="The server-side port to open connections to. Default to 9042.")
    parser.add_argument("--username", type=str, default='cassandra',
                        help="Username required to connect to Cassandra database. Default is 'cassandra'.")
    parser.add_argument("--password", type=str, default='cassandra',
                        help="Password required to connect to Cassandra database. Default is 'cassandra'.")
    args, _ = parser.parse_known_args()
    return args


if __name__ == "__main__":
    # Parse arguments
    args = parse_arguments()

    # Connect to database
    cluster, session = connect_db(args)

    # Init keyspace
    init_keyspace(session)

    # Close cluster
    cluster.shutdown()
