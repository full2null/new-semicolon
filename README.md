# Semicolon - 개발자 커뮤니티

개발자들의 질문과 답변을 나누는 커뮤니티 플랫폼입니다.

## 🚀 빠른 시작

### 프로덕션 모드 (서버 배포용)

**Linux/Mac:**

```bash
chmod +x start.sh
./start.sh
```

**Windows:**

```cmd
start.bat
```

서버를 중지하려면:

```bash
./stop.sh  # Linux/Mac only
```

### 개발 모드

**Linux/Mac:**

```bash
chmod +x dev.sh
./dev.sh
```

**Windows:**

```cmd
dev.bat
```

## 📋 요구사항

- Python 3.13 이상
- Node.js 18 이상
- PostgreSQL (선택사항, 기본값은 SQLite)

## 🔧 수동 설치 및 실행

### 백엔드 설정

```bash
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate.bat

# 의존성 설치
pip install -e .

# 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 또는 프로덕션 빌드
npm run build
npm run preview
```

## 🌐 접속 URL

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 📁 프로젝트 구조

```
semicolon/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── api/         # API 엔드포인트
│   │   ├── core/        # 설정 및 데이터베이스
│   │   ├── crud/        # CRUD 작업
│   │   ├── models/      # 데이터베이스 모델
│   │   ├── schemas/     # Pydantic 스키마
│   │   └── main.py      # FastAPI 앱
│   └── pyproject.toml
├── frontend/             # Svelte 프론트엔드
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # UI 컴포넌트
│   │   │   └── utils.js     # 유틸리티 함수
│   │   └── routes/          # 페이지 라우트
│   └── package.json
├── start.sh             # 프로덕션 시작 스크립트 (Linux/Mac)
├── start.bat            # 프로덕션 시작 스크립트 (Windows)
├── stop.sh              # 서버 중지 스크립트 (Linux/Mac)
├── dev.sh               # 개발 모드 스크립트 (Linux/Mac)
└── dev.bat              # 개발 모드 스크립트 (Windows)
```

## 🛠️ 개발 도구

### 백엔드

```bash
cd backend

# 테스트 실행
pytest

# 코드 포맷팅
black .
isort .

# 린팅
flake8
mypy .
```

### 프론트엔드

```bash
cd frontend

# 타입 체크
npm run check

# 포맷팅
npm run format

# 린팅
npm run lint
```

## 📝 환경 변수

백엔드 설정은 `backend/app/core/config.py`에서 관리됩니다.
필요시 `.env` 파일을 생성하여 환경 변수를 설정할 수 있습니다:

```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost/semicolon

# 보안
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## 🐳 Docker (추후 지원 예정)

```bash
docker-compose up -d
```

## 📄 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🤝 기여

기여는 언제나 환영합니다! Pull Request를 보내주세요.
