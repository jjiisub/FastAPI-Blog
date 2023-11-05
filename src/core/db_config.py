from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.config import Settings

engine = create_engine(Settings().SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    '''
    DB 세션 관리 함수
    '''
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()