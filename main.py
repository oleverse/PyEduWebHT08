import logging
import threading

import coloredlog
from producer import produce
from consumer import consume


if __name__ == "__main__":
    logging.basicConfig(
        level=None,
        handlers=[coloredlog.ConsoleHandler()]
    )

    consumer_thread = threading.Thread(target=consume)
    consumer_thread.start()
    produce()
    try:
        consumer_thread.join()
    except (KeyboardInterrupt, EOFError):
        print("Consuming stopped.")
