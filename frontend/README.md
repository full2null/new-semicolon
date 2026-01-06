# Semicolon Frontend

개발자 커뮤니티 Semicolon의 프론트엔드 프로젝트입니다. SvelteKit으로 구축되었습니다.

## 기능

- 사용자 인증 (로그인/회원가입)
- 질문 작성 및 조회
- 답변 작성 및 관리
- 반응형 UI 디자인
- Pretendard 폰트 적용

## 개발 환경 설정

프로젝트를 생성했다면, 다음 명령어로 의존성을 설치하세요:

```sh
npm install
# 또는
pnpm install
# 또는
yarn install
```

## 개발 서버 실행

개발 서버를 시작하려면:

```sh
npm run dev

# 또는 새 브라우저 탭에서 자동으로 열기
npm run dev -- --open
```

## 빌드

프로덕션 버전을 빌드하려면:

```sh
npm run build
```

빌드된 결과물을 미리보려면 `npm run preview`를 실행하세요.

## 프로젝트 구조

```
src/
├── routes/              # 페이지 라우트
│   ├── +layout.svelte  # 기본 레이아웃
│   └── +page.svelte    # 메인 페이지
├── lib/
│   └── components/     # 재사용 가능한 컴포넌트
│       ├── ui/         # UI 기본 컴포넌트
│       ├── Header.svelte
│       ├── Sidebar.svelte
│       ├── QuestionList.svelte
│       ├── QuestionDetail.svelte
│       ├── LoginPage.svelte
│       └── RegisterPage.svelte
├── app.html            # HTML 템플릿
└── app.css             # 글로벌 스타일
```

## 기술 스택

- **SvelteKit**: 프론트엔드 프레임워크
- **JavaScript**: TypeScript 대신 JSDoc 사용
- **CSS**: 커스텀 CSS (Tailwind 대신)
- **Pretendard**: 한국어 최적화 폰트

> 배포를 위해서는 타겟 환경에 맞는 [어댑터](https://svelte.dev/docs/kit/adapters)를 설치해야 할 수 있습니다.
