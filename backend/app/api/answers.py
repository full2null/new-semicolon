from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..crud import create_answer, delete_answer, get_question, update_answer
from ..models import User
from ..schemas import Answer, AnswerCreate, AnswerUpdate, ApiResponse, success_response

router = APIRouter()


@router.post("/", response_model=ApiResponse[Answer])
def create_answer_endpoint(
    answer: AnswerCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """답변 작성 - 로그인 필수"""
    # Check if question exists
    db_question = get_question(db, question_id=answer.question_id)
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "QUESTION_NOT_FOUND", "message": "질문을 찾을 수 없습니다."},
        )

    new_answer = create_answer(db=db, answer=answer, author_id=current_user.id)
    return success_response(data=new_answer, message="답변이 등록되었습니다.")


@router.put("/{answer_id}", response_model=ApiResponse[Answer])
def update_answer_endpoint(
    answer_id: int,
    answer_update: AnswerUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """답변 수정 - 작성자만 가능"""
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "ANSWER_NOT_FOUND", "message": "답변을 찾을 수 없습니다."},
        )

    if db_answer.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "PERMISSION_DENIED",
                "message": "답변을 수정할 권한이 없습니다. 작성자만 수정할 수 있습니다.",
            },
        )

    updated_answer = update_answer(db=db, answer_id=answer_id, answer_update=answer_update)
    return success_response(data=updated_answer, message="답변이 수정되었습니다.")


@router.delete("/{answer_id}", response_model=ApiResponse[None])
def delete_answer_endpoint(
    answer_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """답변 삭제 - 작성자만 가능"""
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if db_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "ANSWER_NOT_FOUND", "message": "답변을 찾을 수 없습니다."},
        )

    if db_answer.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "PERMISSION_DENIED",
                "message": "답변을 삭제할 권한이 없습니다. 작성자만 삭제할 수 있습니다.",
            },
        )

    success = delete_answer(db=db, answer_id=answer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "DELETE_FAILED", "message": "답변 삭제에 실패했습니다."},
        )

    return success_response(message="답변이 삭제되었습니다.")
