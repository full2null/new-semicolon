from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..core.security import create_access_token
from ..crud import (
    authenticate_user,
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from ..schemas import ApiResponse, Token, User, UserCreate, success_response

router = APIRouter()


@router.post("/register", response_model=ApiResponse[User])
def register(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입 - 이메일과 사용자명 중복 검사 후 계정 생성"""
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "EMAIL_EXISTS", "message": "이미 등록된 이메일입니다."},
        )

    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "USERNAME_EXISTS", "message": "이미 사용중인 사용자명입니다."},
        )

    new_user = create_user(db=db, user=user)
    return success_response(data=new_user, message="회원가입이 완료되었습니다.")


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """로그인 - JWT 액세스 토큰 발급"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "INVALID_CREDENTIALS", "message": "사용자명 또는 비밀번호가 올바르지 않습니다."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
