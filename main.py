import logging
import sys
from time import sleep
from threading import Thread

import schedule
from app.controllers.webserver import start
from yahoo import yahoo_finance
from app.controllers.webserver import app as application


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# appのインスタンスを作成
app = application

if __name__ == "__main__":
    # Yahoo Finance からデータを取得し、DBに格納
    # yahoo_finance.generate_all_values()

    # サーバを起動
    # serverThread = Thread(target=start)
    # serverThread.start()
    # serverThread.join()

    # 毎時00分時点でDBのデータを更新
    schedule.every().hour.at(":00").do(yahoo_finance.generate_all_values)
    while True:
        schedule.run_pending()
        sleep(1)
