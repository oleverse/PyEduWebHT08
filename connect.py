from mongoengine import connect
import configparser
from pathlib import Path
from redis import Redis


config = configparser.ConfigParser()
config.read(Path('db.ini'))

mongo_conn_string = config.get('MongoDB', 'url')

connect(host=mongo_conn_string)

redis_host = config.get('Redis', 'host')
redis_port = int(config.get('Redis', 'port'))
redis_cache = Redis(host=redis_host, port=redis_port)

