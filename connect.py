import logging
from mongoengine import connect
import configparser
from pathlib import Path
import pika
from contextlib import contextmanager

@contextmanager
def get_rabbit_connection() -> pika.BlockingConnection:
    rabbit_conn = None

    rabbit_user = config.get('RabbitMQ', 'user')
    rabbit_pass = config.get('RabbitMQ', 'password')
    creds = pika.PlainCredentials(rabbit_user, rabbit_pass)
    rabbit_host = config.get('RabbitMQ', 'host')
    rabbit_port = int(config.get('RabbitMQ', 'port'))

    try:
        rabbit_conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbit_host,
                port=rabbit_port,
                credentials=creds
            )
        )
        logging.info(f'Pika connection established. {rabbit_conn}')
        yield rabbit_conn
    except pika.exceptions as error:
        logging.info(error)
    finally:
        logging.info('Pika connection closed.')
        rabbit_conn.close()


config = configparser.ConfigParser()
config.read(Path('db.ini'))

mongo_conn_string = config.get('MongoDB', 'url')

connect(host=mongo_conn_string)
