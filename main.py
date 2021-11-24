import logging
import sys
from time import sleep
from threading import Thread

import schedule
from app.controllers.webserver import start
from yahoo import yahoo_finance

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == "__main__":
    # サーバを起動
    # serverThread = Thread(target=start)
    # serverThread.start()
    # serverThread.join()

    # 毎時00分時点でDBのデータを更新
    schedule.every().hour.at(":00").do(yahoo_finance.generate_all_values)
    while True:
        schedule.run_pending()
        sleep(1)
