from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import argparse
import sys


# Parsing args
parser = argparse.ArgumentParser()
parser.add_argument('--host', help='cassandra host')
parser.add_argument('--user',help='username')
parser.add_argument('--passwd',help='password')
 
args = parser.parse_args()
 
# Auth provider for connecting to cassandra
auth_provider = PlainTextAuthProvider(username=args.user, password=args.passwd)
 
# Verifying user args
if (not args.host) or (not args.user) or (not args.passwd):
    print("You must provide host, user, and password for cassandra node as arguments.")
    sys.exit(1)
 
# Connection
cluster = Cluster([args.host],port=9042,auth_provider=auth_provider)
session = cluster.connect()
 
# Creating keyspace
session.execute("""
CREATE KEYSPACE mysimbdp
 WITH REPLICATION = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 1
 };
""")
 
# Using our new keyspace
session.set_keyspace('mysimbdp')
 
# Creating tables
session.execute("""
CREATE TABLE data_acq(
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
CREATE TABLE sensors(
  id int PRIMARY KEY,
  sensor varchar
  );
""")
 
session.execute("""
CREATE TABLE alarms(
  id int PRIMARY KEY,
  alarm varchar
  );
""")
 
print("Successfully created keyspace mysimbdp and tables data_acq, sensors, and alarms.")