from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..crud import (
    create_question,
    get_answers_by_question,
    get_question,
    get_questions,
    increment_question_views,
    update_question,
)
from ..models import User
from ..schemas import (
    Answer,
    ApiResponse,
    Question,
    QuestionCreate,
    QuestionUpdate,
    success_response,
)

router = APIRouter()


@router.get("/", response_model=ApiResponse[List[Question]])
def read_questions(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    q: Optional[str] = Query(default=None, description="검색어 (제목 또는 내용)"),
    sort_by: Optional[str] = Query(default=None, description="정렬 방식 (answers: 답변순)"),
    db: Session = Depends(get_db),
):
    """질문 목록 조회 - 페이지네이션, 검색, 정렬 지원"""
    questions = get_questions(db, skip=skip, limit=limit, search=q, sort_by=sort_by)
    return success_response(data=questions, message="질문 목록을 불러왔습니다.")


@router.post("/", response_model=ApiResponse[Question])
def create_question_endpoint(
    question: QuestionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """질문 작성 - 로그인 필수"""
    new_question = create_question(db=db, question=question, author_id=current_user.id)
    return success_response(data=new_question, message="질문이 등록되었습니다.")


@router.get("/{question_id}", response_model=ApiResponse[Question])
def read_question(question_id: int, db: Session = Depends(get_db)):
    """질문 상세 조회 - 조회수 자동 증가"""
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "QUESTION_NOT_FOUND", "message": "질문을 찾을 수 없습니다."},
        )

    # Increment views
    increment_question_views(db, question_id)

    return success_response(data=db_question, message="질문을 불러왔습니다.")


@router.put("/{question_id}", response_model=ApiResponse[Question])
def update_question_endpoint(
    question_id: int,
    question_update: QuestionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """질문 수정 - 작성자만 가능"""
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "QUESTION_NOT_FOUND", "message": "질문을 찾을 수 없습니다."},
        )

    if db_question.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "PERMISSION_DENIED",
                "message": "질문을 수정할 권한이 없습니다. 작성자만 수정할 수 있습니다.",
            },
        )

    updated_question = update_question(
        db=db, question_id=question_id, question_update=question_update
    )
    return success_response(data=updated_question, message="질문이 수정되었습니다.")


@router.get("/{question_id}/answers", response_model=ApiResponse[List[Answer]])
def read_question_answers(question_id: int, db: Session = Depends(get_db)):
    """특정 질문의 모든 답변 조회"""
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "QUESTION_NOT_FOUND", "message": "질문을 찾을 수 없습니다."},
        )

    answers = get_answers_by_question(db, question_id=question_id)
    return success_response(data=answers, message="답변 목록을 불러왔습니다.")
