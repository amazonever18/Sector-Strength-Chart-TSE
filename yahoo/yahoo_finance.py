import sys
import datetime

from sqlalchemy import create_engine
import pandas as pd

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

import settings

# TOPIXとTOPIX-17シリーズの証券コード
TOPIX = {"TOPIX": "1306.T"}
TOPIX_17 = {"FOOD": "1617.T",
            "ERGY": "1618.T",
            "CNMT": "1619.T",
            "RWCH": "1620.T",
            "PHRM": "1621.T",
            "TPEQ": "1622.T",
            "STML": "1623.T",
            "MACH": "1624.T",
            "ELPR": "1625.T",
            "ITSV": "1626.T",
            "ELEC": "1627.T",
            "TPLG": "1628.T",
            "WSAL": "1629.T",
            "RETL": "1630.T",
            "BNK": "1631.T",
            "FNCL": "1632.T",
            "REAL": "1633.T"}


# Yahoo Finance からある時間軸における価格データを取得
def generate_values(priod_type, priod, frequency_type, frequency, table):
    # TOPIXの価格データを取得
    my_share = share.Share("1306.T")
    symbol_data = None
    try:
        symbol_data = my_share.get_historical(priod_type, priod, frequency_type, frequency)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    # データフレームに格納し、時刻と終値を抽出した上で整形
    df_base = pd.DataFrame(symbol_data)
    df_base = df_base.loc[:, ['timestamp', 'close']]
    df_base = df_base.rename(columns={'close': 'TOPIX'})
    df_base["timestamp"] = pd.to_datetime(df_base.timestamp, unit="ms") + datetime.timedelta(hours=9)
    df_base = df_base.rename(columns={'timestamp': 'time'})

    # TOPIX-17シリーズの価格データを取得
    for key, value in TOPIX_17.items():
        my_share = share.Share(value)
        symbol_data = None
        try:
            symbol_data = my_share.get_historical(priod_type, priod, frequency_type, frequency)
        except YahooFinanceError as e:
            print(e.message)
            sys.exit(1)

        # データフレームに格納し、時刻と終値を抽出した上で整形
        df_17 = pd.DataFrame(symbol_data)
        df_17 = df_17.loc[:, ['timestamp', 'close']]
        df_17 = df_17.rename(columns={'close': f'{key}'})
        df_17["timestamp"] = pd.to_datetime(df_17.timestamp, unit="ms") + datetime.timedelta(hours=9)
        df_17 = df_17.rename(columns={'timestamp': 'time'})

        # TOPIXのデータフレームとTOPIX-17シリーズのデータフレームをマージ
        df_base = pd.merge(df_base, df_17, on='time')

    # 時刻をインデックスに指定
    df_base.set_index('time', inplace=True)

    # 対TOPIX指数の算出
    df_base = (df_base / df_base.iloc[0])
    df_base = df_base.div(df_base["TOPIX"], axis=0).drop("TOPIX", axis=1) - 1

    # 外れ値の除外と欠損値の補完
    df_base = df_base.mask(df_base > 10)
    df_base = df_base.fillna(method='ffill')

    # データフレームをDBに変換
    engine = create_engine(f'sqlite:///{settings.db_name}?check_same_thread=False')
    df_base.to_sql(table, con=engine, schema=None, if_exists='replace', index=True,
                   index_label=None, chunksize=None, dtype=None, method=None)


# 上記のプロセスを全ての時間軸で行う
def generate_all_values():
    # 有効な時間軸: [1m, 2m, 5m, 15m, 30m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    generate_values(share.PERIOD_TYPE_MONTH, 1, share.FREQUENCY_TYPE_HOUR, 1, 'Value_1M')
    generate_values(share.PERIOD_TYPE_MONTH, 3, share.FREQUENCY_TYPE_HOUR, 1, 'Value_3M')
    generate_values(share.PERIOD_TYPE_YEAR, 1, share.FREQUENCY_TYPE_DAY, 1, 'Value_1Y')
    generate_values(share.PERIOD_TYPE_YEAR, 5, share.FREQUENCY_TYPE_WEEK, 1, 'Value_5Y')
    generate_values(share.PERIOD_TYPE_YEAR, 100, share.FREQUENCY_TYPE_MONTH, 1, 'Value_Max')
