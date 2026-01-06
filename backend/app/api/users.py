from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models import User as UserModel
from ..schemas import ApiResponse, User, success_response

router = APIRouter()


@router.get("/me", response_model=ApiResponse[User])
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """현재 로그인한 사용자 정보 조회 (마이페이지용)"""
    return success_response(data=current_user, message="사용자 정보를 불러왔습니다.")


@router.get("/{user_id}", response_model=ApiResponse[User])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """특정 사용자 공개 정보 조회"""
    from ..crud import get_user

    user = get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "USER_NOT_FOUND", "message": "사용자를 찾을 수 없습니다."},
        )
    return success_response(data=user, message="사용자 정보를 불러왔습니다.")
