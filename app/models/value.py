import logging

from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.base import session_scope

logger = logging.getLogger(__name__)


# 各時間軸のベースとなるテーブルのクラスを定義
class BaseValue(object):
    time = Column(DateTime, primary_key=True, nullable=False)
    FOOD = Column(Float)
    ERGY = Column(Float)
    CNMT = Column(Float)
    RWCH = Column(Float)
    PHRM = Column(Float)
    TPEQ = Column(Float)
    STML = Column(Float)
    MACH = Column(Float)
    ELPR = Column(Float)
    ITSV = Column(Float)
    ELEC = Column(Float)
    TPLG = Column(Float)
    WSAL = Column(Float)
    RETL = Column(Float)
    BNK = Column(Float)
    FNCL = Column(Float)
    REAL = Column(Float)

    # DBにデータを追加
    @classmethod
    def create(cls, time, FOOD, ERGY, CNMT, RWCH, PHRM, TPEQ, STML, MACH,
               ELPR, ITSV, ELEC, TPLG, WSAL, RETL, BNK, FNCL, REAL):
        value = cls(time=time, FOOD=FOOD, ERGY=ERGY, CNMT=CNMT, RWCH=RWCH, PHRM=PHRM, TPEQ=TPEQ, STML=STML,
                    MACH=MACH, ELPR=ELPR, ITSV=ITSV, ELEC=ELEC, TPLG=TPLG, WSAL=WSAL, RETL=RETL, BNK=BNK,
                    FNCL=FNCL, REAL=REAL)
        # ユニーク要件への対処
        try:
            with session_scope() as session:
                session.add(value)
            return value
        except IntegrityError:
            return False

    # DBから特定のデータを取得
    @classmethod
    def get(cls, time):
        with session_scope() as session:
            value = session.query(cls).filter(
                cls.time == time).first()
        if value is None:
            return None
        return value

    # DBをアップデート
    def save(self):
        with session_scope() as session:
            session.add(self)

    # DBから全てのデータを取得
    @classmethod
    def get_all_values(cls, limit=100):
        with session_scope() as session:
            values = session.query(cls).order_by(
                desc(cls.time)).limit(limit).all()

        if values is None:
            return None

        values.reverse()
        return values

    # 取得したデータを辞書型にキャスト（フロントエンドに送る時に便利）
    @property
    def dict(self):
        return {
            "time": self.time,
            "FOOD": self.FOOD,
            "ERGY": self.ERGY,
            "CNMT": self.CNMT,
            "RWCH": self.RWCH,
            "PHRM": self.PHRM,
            "TPEQ": self.TPEQ,
            "STML": self.STML,
            "MACH": self.MACH,
            "ELPR": self.ELPR,
            "ITSV": self.ITSV,
            "ELEC": self.ELEC,
            "TPLG": self.TPLG,
            "WSAL": self.WSAL,
            "RETL": self.RETL,
            "BNK": self.BNK,
            "FNCL": self.FNCL,
            "REAL": self.REAL
        }


# 各時間軸のテーブルを定義
class Value1M(BaseValue, Base):
    __tablename__ = 'Value_1M'


class Value3M(BaseValue, Base):
    __tablename__ = 'Value_3M'


class Value1Y(BaseValue, Base):
    __tablename__ = 'Value_1Y'


class Value5Y(BaseValue, Base):
    __tablename__ = 'Value_5Y'


class ValueMax(BaseValue, Base):
    __tablename__ = 'Value_Max'


# ファクトリメソッド（利便性向上）
def factory_value_class(duration):
    if duration == '1M':
        return Value1M
    if duration == '3M':
        return Value3M
    if duration == '1Y':
        return Value1Y
    if duration == '5Y':
        return Value5Y
    if duration == 'Max':
        return ValueMax
