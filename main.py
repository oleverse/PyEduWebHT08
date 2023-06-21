import logging

import jsontodb
import search

if __name__ == "__main__":
    logging.basicConfig(level=None)
    jsontodb.export_data()
    search.search_shell()
