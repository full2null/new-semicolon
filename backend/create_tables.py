"""PostgreSQL 데이터베이스 테이블 생성 스크립트"""
from app.core.database import engine, Base
from app.models import User, Question, Answer  # 모델 임포트해서 Base.metadata에 등록

def create_tables():
    """모든 테이블 생성"""
    print("테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✓ 테이블 생성 완료!")

if __name__ == "__main__":
    create_tables()
