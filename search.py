import json
import logging
import re

import models
from connect import redis_cache


def get_quotes_by_name(name):
    if not name:
        logging.info("Name is not set!")
    else:
        # two ways of regex search:
        # case-insensitive with python re
        #   query_pattern = re.compile(rf'.*{name}.*', re.I)
        #   authors = [a.id for a in models.Authors.objects(fullname=query_pattern)]
        # OR
        #   case-insensitive with $regex Mongo modifier
        authors = [a.id for a in models.Authors.objects(fullname__iregex=name)]
        if authors:
            return [q.quote for q in models.Quotes.objects(author__in=authors)]


def get_quotes_by_tags(tags_string):
    tags_list = [re.compile(rf'.*{ts}.*', re.I) for ts in re.split(r'\s*,\s*', tags_string)]

    if not tags_list:
        logging.info("Tag(s) not set!")
    else:
        return [q.quote for q in models.Quotes.objects(tags__in=tags_list)]


def get_quotes_by_tag(tag_string: str):
    if ',' in tag_string:
        print('For several tags you should use "tags" keyword!')
    else:
        return get_quotes_by_tags(tag_string)


KEYWORD_ACTIONS = {
    "name": get_quotes_by_name,
    "tag": get_quotes_by_tag,
    "tags": get_quotes_by_tags
}


def do_search(query: str):
    try:
        keyword, params = re.split(r'\s*:\s*', query, maxsplit=1)
        keyword = keyword.strip().lower()
        if keyword not in KEYWORD_ACTIONS:
            raise ValueError
        params = params.strip()
    except ValueError:
        print("Bad query!")
    else:
        is_from_redis = False

        if not (results := redis_cache.get(f'{keyword}: {params}')):
            results = KEYWORD_ACTIONS[keyword](params)
        else:
            logging.info("Found in Redis cache!")
            is_from_redis = True
            results = json.loads(results)

        if results:
            if not is_from_redis:
                # save for 5 minutes
                redis_cache.set(f'{keyword}: {params}', json.dumps(results), ex=300)
                logging.info("Saved to Redis cache.")

            print(f'Results for query "{query}":\n\t', end='')
            print(*results, sep='\n\t')
        else:
            print("Nothing found!")


def search_shell():
    try:
        if logging.getLogger().level == logging.DEBUG:
            do_search("tags: life, deep")
        else:
            while (query := input(f'Enter search query: ').strip()).lower() != 'exit':
                do_search(query)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        logging.info("Goodbye!")
