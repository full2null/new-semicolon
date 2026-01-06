from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# PostgreSQL을 위한 엔진 설정
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 연결 확인
    pool_size=10,  # 커넥션 풀 크기
    max_overflow=20  # 추가 연결 허용
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
