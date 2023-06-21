import logging, coloredlog

import jsontodb
import search

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[coloredlog.ConsoleHandler()])
    jsontodb.export_data()
    search.search_shell()
