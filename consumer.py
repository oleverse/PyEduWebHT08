import json
import logging
import time

import connect
import models


def send_email(message):
    try:
        contact = models.Contacts.objects(id=message["contact_id"])[0]
    except IndexError:
        logging.info("Nothing found in DB")
    else:
        print(f'To: {contact.email}')
        print(f'Subject: {message["subject"]}')
        print(f'Body: {message["body"]}')
        time.sleep(1)
        print("Message has been sent!")


def on_message(channel, method, properties, body):
    message = json.loads(body.decode())
    logging.info(f" [C] Received {message}")

    send_email(message)

    print(f" [C] Done: {method.delivery_tag}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    with connect.get_rabbit_connection() as connection:
        channel = connection.channel()
        channel.queue_declare(queue='email_queue', durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='email_queue', on_message_callback=on_message)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

