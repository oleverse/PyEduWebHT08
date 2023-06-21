import logging

import jsontodb
import search

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    jsontodb.export_data()
    search.search_shell()
