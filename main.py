import logging
import sys
from threading import Thread

from app.controllers.webserver import start
from yahoo import yahoo_finance


logging.basicConfig(level=logging.INFO, stream=sys.stdout)


if __name__ == "__main__":
    # Yahoo Finance からデータを取得し、DBに格納
    yahoo_finance.generate_all_values()

    # サーバを起動
    # serverThread = Thread(target=start)
    # serverThread.start()
    # serverThread.join()
