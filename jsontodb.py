import connect
import json
import logging
from pathlib import Path

import models

logging.basicConfig(level=logging.INFO & logging.DEBUG)


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


def get_authors():
    if json_data := get_json_object(Path('data/authors.json')):

        authors = []
        for author_json in json_data:
            authors.append(models.Author(author_json))

        return authors


def get_quotes():
    if json_data := get_json_object(Path('data/quotes.json')):

        quotes = []
        for quote_json in json_data:
            quotes.append(models.Quote(quote_json))

        return quotes


def map_quotes_to_authors(authors, quotes):
    for quote in quotes:
        quote.author = list(filter(lambda a: a.fullname == quote.author, authors))[0]


def export_data():
    authors = get_authors()
    quotes = get_quotes()

    if authors and quotes:
        map_quotes_to_authors(authors, quotes)
        [a.save() for a in authors]
        logging.info("List of authors saved to DB.")
        [q.save() for q in quotes]
        logging.info("List of quotes saved to DB.")
    else:
        logging.info(f'Not enough data for export!')
