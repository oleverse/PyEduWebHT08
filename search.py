import logging
import re

import models


def get_quotes_by_name(name):
    if not name:
        logging.info("Name is not set!")
    else:
        query_pattern = re.compile(rf'.*{name}.*', re.I)
        authors = [a.id for a in models.Authors.objects(fullname=query_pattern)]
        if authors:
            return [q.quote for q in models.Quotes.objects(author__in=authors)]


def get_quotes_by_tags(tags_string):
    tags_list = re.split(r'\s*,\s*', tags_string)

    if not tags_list:
        logging.info("Tag(s) not set!")
    else:
        return [q.quote for q in models.Quotes.objects(tags__in=tags_list)]


def get_quotes_by_tag(tag_string: str):
    if ',' in tag_string:
        print('For several tags you should use "tags" keyword!')
    else:
        query_pattern = re.compile(rf'.*{tag_string}.*', re.I)
        return get_quotes_by_tags(tag_string)


KEYWORD_ACTIONS = {
    "name": get_quotes_by_name,
    "tag": get_quotes_by_tag,
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
            do_search("tag: life, success")
        else:
            while (query := input(f'Enter search query: ').strip()).lower() != 'exit':
                do_search(query)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        logging.info("Goodbye!")
