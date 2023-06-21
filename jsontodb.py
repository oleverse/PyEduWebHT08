import mongoengine

import connect
import json
import logging
from pathlib import Path

import models
from locale import setlocale, LC_ALL
from datetime import datetime


setlocale(LC_ALL, 'en_US.UTF-8')


def get_json_object(file_path: Path):
    try:
        with open(file_path) as json_fh:
            json_obj = json.load(json_fh)
    except json.JSONDecodeError:
        logging.info(f'"{file_path}" is not a valid JSON-file!')
    except OSError as os_error:
        logging.info(f'Error ocurred: {os_error}')
    else:
        return json_obj


def authors_from_json():
    if json_data := get_json_object(Path('data/authors.json')):
        authors = []
        for author_json in json_data:
            author_json["born_date"] = datetime.strptime(author_json["born_date"], "%B %d, %Y").date().isoformat()
            authors.append(models.Authors.from_json(json.dumps(author_json)))

        return authors


def get_quotes(authors):
    if json_data := get_json_object(Path('data/quotes.json')):
        quotes = []
        for quote_json in json_data:
            quote_model = models.Quotes.from_json(json.dumps(quote_json))
            quote_model.author = list(filter(lambda a: a.fullname == quote_json["author"], authors))[0]
            quotes.append(quote_model)

        return quotes


def export_authors():
    json_authors = authors_from_json()
    successfully_saved = 0

    if json_authors:
        for author in json_authors:
            try:
                author.save()
                successfully_saved += 1
            except mongoengine.NotUniqueError:
                logging.info("The author exists.")

    logging.info(f"Authors count saved to DB: {successfully_saved}")


def export_quotes():
    db_authors = [a for a in models.Authors.objects()]
    successfully_saved = 0

    if quotes := get_quotes(db_authors):
        for quote in quotes:
            try:
                quote.save()
                successfully_saved += 1
            except mongoengine.NotUniqueError:
                logging.info("The quote exists.")

    logging.info(f"Quotes count saved to DB: {successfully_saved}")


def export_data():
    export_authors()
    export_quotes()
