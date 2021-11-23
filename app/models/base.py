from contextlib import contextmanager
import logging
import threading

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

import settings

# セッションの作成
engine = create_engine(f'sqlite:///{settings.db_name}?check_same_thread=False')
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))
logger = logging.getLogger(__name__)
lock = threading.Lock()


# セッションの管理（コミット、クローズ）
# コンテキストマネージャーをラッパーとした例外処理
@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        lock.acquire()
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'action=session_scope error={e}')
        session.rollback()
        raise
    finally:
        session.expire_on_commit = True
        lock.release()


# テーブルをDBに作成
def init_db():
    import app.models.value
    Base.metadata.create_all(bind=engine)
