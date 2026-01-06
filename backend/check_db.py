"""데이터베이스 상태 확인 스크립트"""
import sys
sys.path.append(".")

from app.core.database import SessionLocal
from app.models import User, Question, Answer

def check_db():
    db = SessionLocal()
    try:
        # 모든 사용자 조회
        users = db.query(User).all()
        print(f"\n=== 사용자 목록 (총 {len(users)}명) ===")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
            
            # 각 사용자의 질문/답변 수 확인
            q_count = db.query(Question).filter(Question.author_id == user.id).count()
            a_count = db.query(Answer).filter(Answer.author_id == user.id).count()
            print(f"  -> 질문: {q_count}개, 답변: {a_count}개")
        
        # 전체 통계
        total_questions = db.query(Question).count()
        total_answers = db.query(Answer).count()
        print(f"\n=== 전체 통계 ===")
        print(f"총 질문: {total_questions}개")
        print(f"총 답변: {total_answers}개")
        
        # 질문 목록
        questions = db.query(Question).all()
        print(f"\n=== 질문 목록 ===")
        for q in questions:
            print(f"ID: {q.id}, Title: {q.title[:50]}..., Author ID: {q.author_id}")
        
        # 답변 목록
        answers = db.query(Answer).all()
        print(f"\n=== 답변 목록 ===")
        for a in answers:
            print(f"ID: {a.id}, Question ID: {a.question_id}, Author ID: {a.author_id}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
