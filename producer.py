import argparse
import json
import random

import mongoengine
import pika
from faker import Faker

import connect
import models


def create_contact(fake):
    contact = models.Contacts()
    contact.fullname = f'{fake.first_name()} {fake.last_name()}'
    contact.email = fake.email()
    try:
        contact.save()
    except mongoengine.NotUniqueError:
        print("The contact already exists.")

    return contact.id


def enqueue_message(fake, params):
    channel, contact, exchange, queue = params
    message = {
        "contact_id": str(contact),
        "subject": fake.paragraph(),
        "body": ' '.join(fake.paragraphs())
    }

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json.dumps(message).encode(),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )

    )

    try:
        email = models.Contacts.objects(id=message["contact_id"]).only('email').first()
    except mongoengine.errors.ValidationError as error:
        print(error)
    else:
        if email:
            print(f' [P] The message for "{email.email}" has been enqueued!')
        else:
            print(f'Object with id {message["contact_id"]} was not found.')


def produce(contacts_from=3, contacts_to=10):
    fake = Faker()

    contacts = [create_contact(fake) for _ in range(random.randint(contacts_from, contacts_to))]
    exchange = 'email_test'
    queue = 'email_queue'

    with connect.get_rabbit_connection() as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type='direct')
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(exchange=exchange, queue=queue)

        for contact in contacts:
            params = channel, contact, exchange, queue
            enqueue_message(fake, params)


def init_argparse():
    parser = argparse.ArgumentParser(prog="Producer for mocking email sending via RabbitMQ")
    parser.add_argument('-c', '--contacts-count', type=int,
                        help=f'number of contacts to generate (from 3 to 50)', required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = init_argparse()
    if 3 > args.contacts_count > 50:
        print("Bad count, use --help for the description.")
    else:
        produce(args.contacts_count, args.contacts_count)
