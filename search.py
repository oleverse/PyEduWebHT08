import logging
import re

import models


def get_quotes_by_name(name):
    if not name:
        logging.info("Name is not set!")
    else:
        authors = [a.id for a in models.Authors.objects(fullname=name)]
        if authors:
            return [q.quote for q in models.Quotes.objects(author__in=authors)]


def get_quotes_by_tags(tags_list):
    pass


KEYWORD_ACTIONS = {
    "name": get_quotes_by_name,
    "tag": get_quotes_by_tags,
    "tags": get_quotes_by_tags
}


def do_search(query: str):
    try:
        keyword, params = re.split(r':\s*', query, maxsplit=1)
    except ValueError:
        print("Bad query!")
    else:
        results = KEYWORD_ACTIONS[keyword.strip().lower()](params.strip())

        if results:
            print(f'Results for query "{query}":\n\t', end='')
            print(*results, sep='\n\t')
        else:
            print("Nothing found!")


def search_shell():
    try:
        if logging.getLogger().level == logging.DEBUG:
            do_search("name: Albert Einstein")
        else:
            while (query := input(f'Enter search query: ').strip()).lower() != 'exit':
                do_search(query)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        logging.info("Goodbye!")
