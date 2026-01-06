from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.dependencies import get_current_active_user
from ..models import User as UserModel
from ..schemas import ApiResponse, User, UserUpdate, success_response

router = APIRouter()


@router.get("/me", response_model=ApiResponse[User])
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """현재 로그인한 사용자 정보 조회 (마이페이지용)"""
    return success_response(data=current_user, message="사용자 정보를 불러왔습니다.")


@router.put("/me", response_model=ApiResponse[User])
def update_users_me(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """현재 로그인한 사용자 정보 수정"""
    from ..crud import get_user_by_email, get_user_by_username, update_user
    
    print(f"[DEBUG] 사용자 업데이트 요청: user_id={current_user.id}, update_data={user_update.dict(exclude_unset=True)}")

    # 이메일 중복 체크
    if user_update.email and user_update.email != current_user.email:
        existing_user = get_user_by_email(db, user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "EMAIL_ALREADY_EXISTS", "message": "이미 사용 중인 이메일입니다."},
            )
    
    # 사용자명 중복 체크
    if user_update.username and user_update.username != current_user.username:
        existing_user = get_user_by_username(db, user_update.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "USERNAME_ALREADY_EXISTS", "message": "이미 사용 중인 사용자명입니다."},
            )
    
    updated_user = update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "USER_NOT_FOUND", "message": "사용자를 찾을 수 없습니다."},
        )
    
    return success_response(data=updated_user, message="사용자 정보가 업데이트되었습니다.")


@router.get("/me/stats", response_model=ApiResponse[dict])
def read_users_me_stats(
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """현재 로그인한 사용자의 통계 조회"""
    from ..crud import get_user_stats

    stats = get_user_stats(db, current_user.id)
    return success_response(data=stats, message="사용자 통계를 불러왔습니다.")



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
