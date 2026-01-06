# Semicolon Forum Backend

FastAPI 기반의 개발자 포럼 백엔드 API입니다.

## 기능

- 사용자 인증 (JWT)
- 질문/답변 CRUD
- 사용자 관리
- SQLite/PostgreSQL 데이터베이스 지원

## 설치 및 실행

### 1. Python 환경 설정

```bash
# Python 3.13 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -e .
```

### 3. 환경 변수 설정

```bash
# .env.example을 .env로 복사
copy .env.example .env

# .env 파일을 편집하여 실제 값으로 변경
```

### 4. 서버 실행

```bash
# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

## API 엔드포인트

### 인증

- `POST /api/v1/auth/register` - 사용자 회원가입
- `POST /api/v1/auth/token` - 로그인 (JWT 토큰 발급)

### 사용자

- `GET /api/v1/users/me` - 현재 사용자 정보
- `GET /api/v1/users/{user_id}` - 특정 사용자 정보

### 질문

- `GET /api/v1/questions/` - 질문 목록
- `POST /api/v1/questions/` - 질문 작성
- `GET /api/v1/questions/{question_id}` - 질문 상세
- `PUT /api/v1/questions/{question_id}` - 질문 수정
- `GET /api/v1/questions/{question_id}/answers` - 질문의 답변 목록

### 답변

- `POST /api/v1/answers/` - 답변 작성
- `PUT /api/v1/answers/{answer_id}` - 답변 수정
- `DELETE /api/v1/answers/{answer_id}` - 답변 삭제

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/                 # API 엔드포인트
│   │   ├── auth.py         # 인증 관련 API
│   │   ├── questions.py    # 질문 관련 API
│   │   ├── answers.py      # 답변 관련 API
│   │   └── users.py        # 사용자 관련 API
│   ├── core/               # 핵심 설정
│   │   ├── config.py       # 앱 설정
│   │   ├── database.py     # 데이터베이스 설정
│   │   ├── security.py     # 보안 (JWT, 패스워드 해시)
│   │   └── dependencies.py # FastAPI 의존성
│   ├── crud/               # 데이터베이스 CRUD 연산
│   ├── models/             # SQLAlchemy 모델
│   ├── schemas/            # Pydantic 스키마
│   ├── tests/              # 테스트
│   └── main.py             # FastAPI 앱 진입점
├── pyproject.toml          # 프로젝트 설정 및 의존성
└── .env.example            # 환경변수 예시
```

## 테스트

```bash
# 테스트 실행
pytest

# 커버리지와 함께 테스트 실행
pytest --cov=app
```

## 개발

개발 환경에서는 SQLite를 사용하며, 운영 환경에서는 PostgreSQL을 권장합니다.

### 데이터베이스 마이그레이션 (향후 추가 예정)

```bash
# Alembic 초기화
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Add initial tables"

# 마이그레이션 적용
alembic upgrade head
```
