from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import answers, auth, questions, users
from .core.config import settings
from .core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## Semicolon Developer Forum API
    
    개발자 커뮤니티 Semicolon의 RESTful API입니다.
    
    ### 주요 기능
    * **인증 (Auth)**: 회원가입, 로그인, JWT 토큰 기반 인증
    * **사용자 (Users)**: 사용자 정보 조회 (공개 정보 / 마이페이지)
    * **질문 (Questions)**: 질문 작성, 조회, 수정 (작성자만)
    * **답변 (Answers)**: 답변 작성, 수정, 삭제 (작성자만)
    
    ### API 응답 형식
    
    **성공 응답**:
    ```json
    {
      "success": true,
      "data": {...},
      "message": "작업 성공 메시지"
    }
    ```
    
    **에러 응답**:
    ```json
    {
      "error": "ERROR_CODE",
      "message": "사용자 친화적 에러 메시지"
    }
    ```
    
    ### 권한 관리
    * 공개 API: 질문/답변 조회
    * 로그인 필요: 질문/답변 작성
    * 작성자만: 본인이 작성한 질문/답변 수정/삭제
    """,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(
    questions.router, prefix=f"{settings.API_V1_STR}/questions", tags=["questions"]
)
app.include_router(
    answers.router, prefix=f"{settings.API_V1_STR}/answers", tags=["answers"]
)
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Semicolon Developer Forum API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
