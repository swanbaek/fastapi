# 📝 FastAPI + React 게시판 프로젝트

FastAPI 백엔드와 React 프론트엔드로 구성된 게시판 웹 애플리케이션입니다.  
JWT 인증 기반의 로그인/회원가입, 게시글 CRUD, 파일 업로드 기능을 제공합니다.

---

## 📁 프로젝트 구조

```
fastapi/
├── backend/               # FastAPI 백엔드
│   ├── app/
│   │   ├── core/          # DB 설정 등 핵심 설정
│   │   ├── crud/          # DB CRUD 함수
│   │   ├── deps.py        # 의존성 주입 (JWT 인증 등)
│   │   ├── models/        # SQLAlchemy 모델
│   │   ├── routers/       # API 라우터
│   │   │   ├── auth.py    # 로그인 / 로그아웃
│   │   │   └── post_api.py
│   │   ├── schemas/       # Pydantic 스키마
│   │   ├── services/      # 비즈니스 로직
│   │   └── main.py
│   └── requirements.txt
│
└── frontend/              # React 프론트엔드
    ├── src/
    │   ├── api/
    │   │   ├── userApi.js       # 로그인 / 로그아웃 API 호출
    │   │   └── postApi.js       # 게시글 API 호출
    │   ├── stores/
    │   │   ├── authStore.js     # 로그인 사용자 상태
    │   │   ├── postStore.js     # 게시글 서버 통신 상태
    │   │   └── postFormStore.js # 게시글 폼 UI 상태
    │   └── utils/
    │       └── authUtils.js     # 토큰 만료 체크 / refresh 유틸
    └── package.json
```

---

## 🔐 인증 (Auth)

### 기술 방식

Access Token (단기) + Refresh Token (장기) 이중 토큰 구조를 사용합니다.

| 토큰 | 저장 위치 | 용도 |
|------|-----------|------|
| Access Token | `sessionStorage` | API 요청 인증 헤더에 사용 |
| Refresh Token | `localStorage` | Access Token 만료 시 재발급 |

### 인증 API 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| POST | `/auth/login` | 로그인 → Access/Refresh Token 발급 |
| POST | `/auth/logout` | 로그아웃 → 서버 측 Refresh Token 무효화 |

### 로그인 흐름

```
1. 사용자가 이메일/비밀번호 입력
2. POST /auth/login 요청
3. 서버에서 Access Token + Refresh Token 발급
4. Access Token → sessionStorage 저장
5. Refresh Token → localStorage 저장
6. authStore의 authUser에 사용자 정보 저장
```

### 토큰 갱신 흐름 (axiosAuthInstance 인터셉터)

```
요청 전 (요청 인터셉터)
  └─ sessionStorage에서 Access Token 꺼내기
      ├─ 유효한 경우  → Authorization 헤더에 첨부 후 요청
      └─ 만료된 경우  → Refresh Token으로 새 Access Token 발급
                         ├─ 성공 → 새 토큰으로 요청 재시도
                         └─ 실패 → 토큰 전체 삭제 후 홈으로 이동

응답 후 (응답 인터셉터)
  ├─ 401 → Refresh Token으로 재발급 시도
  │         ├─ 성공 → 원래 요청 재시도 (1회 한정, _retry 플래그로 무한루프 방지)
  │         └─ 실패 → 토큰 삭제 후 홈으로 이동
  ├─ 403 → 권한 없음 알림 → 토큰 삭제 후 홈으로 이동
  └─ 400 → 에러 메시지 알림
```

### 로그아웃 흐름

```
1. POST /auth/logout 요청 (email 전달)
2. 서버 측 Refresh Token 무효화
3. sessionStorage에서 Access Token 삭제
4. localStorage에서 Refresh Token 삭제
5. authStore 초기화 (authUser: null)
```

### authStore 구조

```js
authUser: null        // 로그인한 사용자 정보 { id, name, email, role }
loginAuthUser(user)   // 로그인 성공 시 사용자 정보 저장
logout()              // 로그아웃 시 상태 초기화
```

### Axios 인스턴스 구분

| 인스턴스 | 용도 |
|----------|------|
| `axiosInstance` | 인증 불필요 요청 (목록 조회, 상세 조회, 로그인) |
| `axiosAuthInstance` | 인증 필요 요청 — JWT 토큰 자동 첨부 + 만료 시 자동 갱신 (작성, 수정, 삭제) |

---

## 📋 게시글 (Posts)

### 게시글 API 엔드포인트

| Method | URL | 설명 | 인증 |
|--------|-----|------|------|
| GET | `/posts/` | 게시글 목록 (페이징 + 검색) | ❌ |
| POST | `/posts/` | 게시글 작성 | ✅ |
| GET | `/posts/{post_id}` | 게시글 상세 조회 | ❌ |
| PUT | `/posts/{post_id}` | 게시글 수정 | ✅ |
| DELETE | `/posts/{post_id}` | 게시글 삭제 | ✅ |

### 응답 데이터 구조 (게시글 단건)

```json
{
    "id": 51,
    "title": "제목",
    "content": "내용",
    "user_id": 3,
    "author": {
        "id": 3,
        "name": "홍길동",
        "email": "hong@a.b.c",
        "role": "user",
        "created_at": "2026-02-20T15:18:18"
    },
    "created_at": "2026-02-24T18:09:58",
    "updated_at": null,
    "hit_count": 11,
    "file_url": "/static/uploads/20260224180958_9.jpg",
    "file_name": "9.jpg",
    "comments": []
}
```

### 목록 응답 구조 (페이징)

```json
{
    "posts": [...],
    "total": 100,
    "total_pages": 34,
    "page": 1,
    "size": 3
}
```

### 상태 관리 (Zustand)

| 스토어 | 역할 |
|--------|------|
| `postStore.js` | 게시글 목록 조회, 단건 조회, 수정, 삭제 서버 통신 |
| `postFormStore.js` | 작성/수정 폼 입력 UI 상태 관리 |

### 작성자 권한 처리

수정/삭제 버튼은 `authUser.email === post.author.email` 일치 여부로 조건부 렌더링합니다.

```jsx
{authUser?.email === post.author?.email && (
    <div>
        <button>수정</button>
        <button>삭제</button>
    </div>
)}
```

---

## 🖥️ 백엔드 설치 및 실행 (FastAPI)

### 기술 스택

- **Python 3.11+** / **FastAPI** / **SQLAlchemy** / **Pydantic**

### 설치 및 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 7777
```

### 환경 변수 (.env)

```env
DATABASE_URL=sqlite:///./board.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 💻 프론트엔드 설치 및 실행 (React)

### 기술 스택

- **React 18+** / **React Router DOM** / **Zustand** / **Axios** / **React Bootstrap**

### 설치 및 실행

```bash
cd frontend
npm install
npm run dev
```

### 환경 변수 (.env)

```env
VITE_API_BASE_URL=http://localhost:7777
```

---

## 🚀 전체 실행 순서

```bash
# 1. 백엔드 실행
cd backend && uvicorn app.main:app --reload --port 7777

또는 (Windows의 경우)
cd backend; uvicorn app.main:app --reload --port 7777

# 2. 프론트엔드 실행
cd frontend && npm run dev

또는 (Windows의 경우)
cd frontend; npm run dev
```

브라우저에서 `http://localhost:5173` 접속

---

## 📌 주요 구현 포인트

- Access Token은 `sessionStorage`, Refresh Token은 `localStorage`에 분리 저장하여 보안과 편의성을 함께 확보
- `axiosAuthInstance` 인터셉터에서 토큰 만료를 자동 감지하고 재발급 처리 (`_retry` 플래그로 무한 루프 방지)
- 401과 403을 구분 처리 — 401은 토큰 재발급 시도, 403은 즉시 로그아웃
- 게시글 작성자 식별은 이름이 아닌 `email` 기준으로 비교하여 동명이인 오류 방지
- FastAPI 에러 응답 형태 `{ detail: "..." }` 에 맞게 `error.response?.data?.detail`로 파싱
- 게시글 수정 폼 진입 시 `post.author.name`을 `formData.name`으로 매핑하여 초기값 설정
- 파일 업로드 시 `multipart/form-data`, 미업로드 시 `application/json`으로 Content-Type 분기 처리
