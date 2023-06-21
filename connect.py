from mongoengine import connect
import configparser
from pathlib import Path


config = configparser.ConfigParser()
config.read(Path('db.ini'))

mongo_conn_string = config.get('MongoDB', 'url')

# connect to cluster on Atlas with connection string
connect(host=mongo_conn_string)
