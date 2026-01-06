from typing import List, Optional

from sqlalchemy.orm import Session

from ..core.security import get_password_hash, verify_password
from ..models import Answer, Question, User
from ..schemas import (
    AnswerCreate,
    AnswerUpdate,
    QuestionCreate,
    QuestionUpdate,
    UserCreate,
    UserUpdate,
)


# User CRUD
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """사용자 정보 업데이트"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    print(f"[DEBUG CRUD] update_data before password hash: {update_data}")
    
    # 비밀번호가 포함되어 있으면 해시화
    if "password" in update_data and update_data["password"]:
        hashed = get_password_hash(update_data.pop("password"))
        update_data["hashed_password"] = hashed
        print(f"[DEBUG CRUD] Password will be updated, hashed_password set")
    
    # 필드 업데이트
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_stats(db: Session, user_id: int) -> dict:
    """사용자 통계 조회 (작성한 질문 수, 답변 수)"""
    question_count = db.query(Question).filter(Question.author_id == user_id).count()
    answer_count = db.query(Answer).filter(Answer.author_id == user_id).count()
    
    print(f"[DEBUG STATS] user_id={user_id}, question_count={question_count}, answer_count={answer_count}")
    
    return {
        "question_count": question_count,
        "answer_count": answer_count,
    }


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Question CRUD
def get_questions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> List[Question]:
    query = db.query(Question)

    # 검색어가 있으면 제목 또는 내용에서 검색
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Question.title.ilike(search_filter))
            | (Question.content.ilike(search_filter))
        )

    # 정렬 처리
    if sort_by == "answers":
        from ..models import Answer

        # 답변 개수로 정렬 (많은 순서)
        query = (
            query.outerjoin(Answer)
            .group_by(Question.id)
            .order_by(db.func.count(Answer.id).desc())
        )
    else:
        # 기본: 최신순 (생성 시간 역순)
        query = query.order_by(Question.created_at.desc())

    return query.offset(skip).limit(limit).all()


def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()


def create_question(db: Session, question: QuestionCreate, author_id: int) -> Question:
    db_question = Question(**question.dict(), author_id=author_id)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def update_question(
    db: Session, question_id: int, question_update: QuestionUpdate
) -> Optional[Question]:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        update_data = question_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_question, key, value)
        db.commit()
        db.refresh(db_question)
    return db_question


def increment_question_views(db: Session, question_id: int):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db_question.views += 1
        db.commit()


# Answer CRUD
def get_answers_by_question(db: Session, question_id: int) -> List[Answer]:
    return db.query(Answer).filter(Answer.question_id == question_id).all()


def create_answer(db: Session, answer: AnswerCreate, author_id: int) -> Answer:
    db_answer = Answer(**answer.dict(), author_id=author_id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def update_answer(
    db: Session, answer_id: int, answer_update: AnswerUpdate
) -> Optional[Answer]:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer:
        update_data = answer_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_answer, key, value)
        db.commit()
        db.refresh(db_answer)
    return db_answer


def delete_answer(db: Session, answer_id: int) -> bool:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer:
        db.delete(db_answer)
        db.commit()
        return True
    return False


# Stats CRUD
def get_stats(db: Session) -> dict:
    """전체 통계 조회 (질문 수, 답변 수, 사용자 수)"""
    question_count = db.query(Question).count()
    answer_count = db.query(Answer).count()
    user_count = db.query(User).count()

    return {
        "question_count": question_count,
        "answer_count": answer_count,
        "user_count": user_count,
    }
