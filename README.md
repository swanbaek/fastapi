# EduApp FastAPI 프로젝트

## 소개
- 이 프로젝트는 FastAPI 기반의 웹 애플리케이션으로, 회원가입, JWT 로그인, 회원 목록/게시글 CRUD 기능을 제공합니다. JWT(Json Web Token) 기반 인증/인가 처리를 통해 보안성과 확장성을 높였습니다.
- **React.js와 연동하는 Restfull Service에 초점을 둡니다**

## 주요 기능
- **회원가입**: 이름, 이메일, 비밀번호 입력 후 회원가입. 이메일 중복 체크 및 비밀번호 해싱(bcrypt) 적용.
- **JWT 로그인/로그아웃**: 이메일+비밀번호로 로그인 시 JWT 토큰(access/refresh) 발급, 클라이언트(브라우저) LocalStorage에 저장. 로그아웃 시 토큰 삭제.
- **회원 목록**: JWT 토큰이 있고 role이 admin인 경우 전체 회원 목록 조회 가능.
- **회원 정보 수정/삭제**: JWT 토큰이 있는 경우 내 정보 수정/탈퇴 가능.
- **Post글 CRUD기능** : 글수정,삭제는 JWT 토큰이 있는 경우만 가능
- **Comment글 CRUD기능** : 댓글 수정,삭제는 JWT 토큰이 있는 경우만 가능

## 기술 스택
- Python 3.9+
- FastAPI
- PyMySQL (SQL 직접 사용)
- bcrypt (비밀번호 해싱)
- Jinja2 (템플릿)
- python-dotenv (환경변수 관리)
- python-jose (JWT 토큰 발급/검증)

## 폴더 구조
```

app/
 ├── api/          # 라우터(엔드포인트) 모음
 ├── core/         # 설정, 환경변수, 보안, CORS, init 관련, DB연결함수
 ├── crud/         # DB CRUD 함수 모음
 ├── models/       # SQLAlchemy 모델 [DB 구조(테이블) 정의]
 ├── schemas/      # Pydantic 스키마 [FastAPI용 Request/Response 데이터 검증/반환용]
 ├── services/     # 비즈니스 로직 (서비스 계층)
 ├── static/       # CSS, JS, 이미지 (정적 파일)
 ├── templates/    # Jinja2 HTML 템플릿
 ├── deps.py       # 의존성(dependencies)
 └── main.py       # FastAPI 진입점
```
### User관련 폴더 구조
```
app/
  api/
    users.py      # 회원 관련 API (CRUD)
    login.py      # JWT 로그인/로그아웃 API
  core/
    db.py         # DB 연결 함수 (get_connection)
  schemas/
    user.py       # Pydantic 스키마
  static/        # 정적 파일(css 등)
  templates/     # Jinja2 템플릿(html)
main.py          # FastAPI 앱 진입점
requirements.txt # 의존성 목록
```

#### User 관련 API 엔드포인트 (JWT 기반)
| 메서드 | 경로                | 설명                        |
|--------|---------------------|-----------------------------|
| GET    | /api/users/list         | 회원목록 페이지(HTML, JWT 필요시 JS로 제어) |
| GET    | /api/users              | 회원목록(JSON, JWT 필요, JS fetch Authorization 헤더) |
| GET    | /api/users/me           | 내 정보 조회 (JWT 필요)   |
| GET    | /api/users/{user_id}    | 특정 회원 정보 조회         |
| POST   | /api/users              | 회원가입 (JSON)             |
| POST   | /signup                 | 회원가입 (Form)             |
| POST   | /auth/login             | 로그인(JWT 토큰 발급, JSON) |
| POST   | /auth/logout            | 로그아웃(토큰 삭제, 클라이언트 처리) |
| POST   | /auth/refresh           | 토큰 재발급(리프레시)       |
| PUT    | /api/users/me           | 내 정보 수정 (JWT 필요)   |
| PATCH  | /api/users/me           | 내 정보 일부 수정 (JWT 필요) |
| DELETE | /api/users/me           | 회원 탈퇴 (JWT 필요)      |

### Posts 관련 폴더 구조
```
app/
 ├── api/
 │    └── posts.py            ← 라우터만 (요청/응답만 담당)
 ├── services/
 │    └── post_service.py     ← 비즈니스 로직
 ├── crud/
 │    └── post_crud.py        ← DB 접근만 담당
 ├── models/
 │    └── post.py
 ├── schemas/
 │    └── post.py
```

### Posts 관련 API 엔드포인트 (JWT 기반)
| 메서드 | 경로                      | 설명                                 |
|--------|---------------------------|--------------------------------------|
| GET    | /posts/list               | 게시글 목록 페이지(HTML, JWT 필요시 JS로 제어) |
| GET    | /posts                    | 게시글 목록(JSON)                    |
| GET    | /posts/new                | 게시글 작성 폼(HTML, JWT 필요시 JS로 제어) |
| POST   | /posts                    | 게시글 작성(폼 제출, JWT 필요, Authorization 헤더) |
| GET    | /posts/{post_id}          | 게시글 상세(HTML, JWT 필요시 JS로 제어) |
| GET    | /posts/{post_id}/edit     | 게시글 수정 폼(HTML, 본인만, JS로 제어) |
| POST   | /posts/{post_id}/edit     | 게시글 수정(폼 제출, JWT 필요, 본인만) |
| POST   | /posts/{post_id}/delete   | 게시글 삭제(JWT 필요, 본인만)        |

#### Posts 페이징 처리 및 검색 관련  API 엔드포인트


```
GET /posts/?page={page}&size={size}&search={keyword}
```

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| page | int | 1 | 현재 페이지 번호 |
| size | int | 10 | 페이지당 게시글 수 |
| search | str | "" | 제목 검색 키워드 (없으면 전체 조회) |

**응답 형식 (`PostListOut`)**

```json
{
  "total": 22,
  "posts": [
    {
      "id": 1,
      "title": "게시글 제목",
      "author": { "name": "홍길동" },
      "created_at": "2025-01-01T00:00:00",
      "hit_count": 10,
      "file_url": null
    }
  ]
}
```

---
## 💬 댓글 기능

### 구조 개요

댓글은 Router → Service → CRUD 3계층으로 구현되어 있으며,  
작성/수정/삭제는 JWT 인증이 필요하고 본인 댓글만 수정/삭제할 수 있습니다.

---

### 데이터 모델

**Comment 모델** (`app/models/comment.py`)

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | PK |
| content | Text | 댓글 내용 |
| user_id | Integer | FK → members.id |
| post_id | Integer | FK → posts.id (CASCADE) |
| created_at | DateTime | 작성일 |

---

### Comment관련 API 엔드포인트

| 메서드 | URL | 인증 | 설명 |
|--------|-----|------|------|
| GET | `/comments/post/{post_id}` | 불필요 | 특정 게시글 댓글 목록 |
| POST | `/comments/post/{post_id}` | JWT 필요 | 댓글 작성 |
| PUT | `/comments/{comment_id}` | JWT 필요 | 댓글 수정 (본인만) |
| DELETE | `/comments/{comment_id}` | JWT 필요 | 댓글 삭제 (본인만) |

---

### 요청/응답 형식

**댓글 목록 조회**
```
GET /comments/post/1
```
```json
[
  {
    "id": 1,
    "content": "댓글 내용",
    "author": { "id": 1, "name": "홍길동", "email": "..." },
    "created_at": "2025-01-01T00:00:00"
  }
]
```

**댓글 작성**
```
POST /comments/post/1
Authorization: Bearer {token}
Content-Type: application/json

{ "content": "댓글 내용" }
```

**댓글 수정**
```
PUT /comments/1
Authorization: Bearer {token}
Content-Type: application/json

{ "content": "수정된 댓글 내용" }
```

**댓글 삭제**
```
DELETE /comments/1
Authorization: Bearer {token}
```

---

### 백엔드 구현

**CRUD** (`app/crud/comment_crud.py`)
```python
# 목록 조회 - author joinedload로 N+1 방지
def get_comments_by_post(db, post_id):
    return (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

# 작성
def create_comment(db, post_id, user_id, content):
    ...

# 수정 - 본인 확인 후 수정, None(없음)/False(권한없음)/comment(성공) 반환
def update_comment(db, comment_id, user_id, content):
    ...

# 삭제 - 본인 확인 후 삭제, None(없음)/False(권한없음)/True(성공) 반환
def delete_comment(db, comment_id, user_id):
    ...
```

**Schema** (`app/schemas/comment_schema.py`)
```python
class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    author: Optional[UserOut] = None
    created_at: datetime

    class Config:
        from_attributes = True
```

---

### 프론트엔드 구현

게시글 상세 페이지(`post_detail.html`)에서 처리합니다.

- JWT 페이로드의 `id`와 댓글의 `author.id`를 비교해 **본인 댓글에만 수정/삭제 버튼 표시**
- 수정은 **인라인 편집** 방식 (댓글 자리에서 textarea로 전환)
- 작성/수정/삭제 후 `location.reload()`로 목록 갱신
- 댓글 수는 게시글 상세 헤더에 badge로 표시
- 게시글 목록(`posts.html`)에서도 제목 옆에 댓글 수 badge 표시

---

### 권한 처리

| 액션 | 프론트 | 백엔드 |
|------|--------|--------|
| 작성 | 로그인 시에만 폼 노출 | JWT 토큰 검증 |
| 수정 | 본인 댓글에만 버튼 노출 | user_id 일치 여부 확인 |
| 삭제 | 본인 댓글에만 버튼 노출 | user_id 일치 여부 확인 |

---
### 백엔드 구현

**Router** (`app/api/posts.py`)
```python
@router.get("/", response_model=PostListOut)
def list_posts(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10,
    search: str = ""
):
    return post_service.list_posts_paging(db, page=page, size=size, search=search)
```

**Service** (`app/services/post_service.py`)
```python
def list_posts_paging(db: Session, page: int = 1, size: int = 10, search: str = ""):
    total, posts = post_crud.get_posts(db, page=page, size=size, search=search)
    return {"total": total, "posts": posts}
```

**CRUD** (`app/crud/post_crud.py`)
```python
def get_posts(db: Session, page: int = 1, size: int = 10, search: str = ""):
    query = db.query(Post)
    if search:
        query = query.filter(Post.title.contains(search))
    total = query.count()
    offset = (page - 1) * size
    posts = query.order_by(Post.id.desc()).offset(offset).limit(size).all()
    return total, posts
```

**Schema** (`app/schemas/post_schema.py`)
```python
class PostListOut(BaseModel):
    total: int
    posts: List[PostOut]
```

---

### 프론트엔드 구현

**페이징 블럭 방식**으로 구현되어 있으며, 한 블럭에 최대 5개의 페이지 번호를 표시합니다.

```
이전 | [1] [2] [3] | 다음
```

- 블럭 끝에서 `다음` 클릭 시 다음 블럭의 첫 페이지로 이동
- 블럭 시작에서 `이전` 클릭 시 이전 블럭의 마지막 페이지로 이동
- 현재 페이지는 파란색으로 강조 표시

```javascript
const pageSize = 3;   // 페이지당 게시글 수
const blockSize = 3;   // 블럭당 페이지 번호 수
```

**검색 결과 표시**

테이블 상단에 검색 상태에 따라 다르게 표시됩니다.

- 전체 조회 시: `전체 22건`
- 검색 시: `"키워드" 검색결과 3건`

---

### 동작 흐름

```
[검색어 입력 or 페이지 클릭]
        ↓
fetch /posts/?page=N&size=10&search=키워드
        ↓
{ total: N, posts: [...] } 응답
        ↓
테이블 렌더링 + 건수 표시 + 페이지네이션 렌더링
```

### 화면 예시

#### 게시글 댓글 목록
![댓글 목록](./5.png)

#### 게시글 목록에 댓글수 출력
![게시글 목록](./6.png)

## DB 연동 방식
이 프로젝트는 **SQLAlchemy** ORM을 사용하여 데이터베이스와 연동합니다.

1. `.env` 파일 또는 환경변수에서 DB 접속 정보(`DB_URL`)를 로드합니다.
2. `app/core/database.py`에서 SQLAlchemy의 `create_engine`으로 DB 연결을 생성합니다.
3. ORM 모델은 `app/models/` 폴더에서 정의하며, 테이블 구조를 파이썬 클래스로 관리합니다.
4. 데이터베이스 작업은 SQLAlchemy의 `Session`을 통해 트랜잭션 단위로 처리합니다.
5. CRUD 작업은 SQLAlchemy 쿼리문으로 수행하며, 직접 SQL문을 작성하지 않아도 됩니다.
6. 트랜잭션/에러 발생 시 `session.rollback()`으로 처리합니다.

자세한 SQLAlchemy 연동 및 사용법은 [sqlalchemy_guide.md](./sqlalchemy_guide.md) 파일을 참고하세요.

## 실행 방법
1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```
2. 환경변수 설정 (예: .env 파일)
   ```env
   DB_URL=mysql+pymysql://계정:비밀번호@localhost:3306/데이터베이스명
   MYSQL_HOST=localhost
   MYSQL_USER=youruser
   MYSQL_PASSWORD=yourpassword
   MYSQL_DB=yourdb
   ```
3. 서버 실행
   ```bash
   uvicorn app.main:app --reload
   ```
4. 브라우저에서 `http://localhost:8000` 접속

## 기타 참고
- SQLAlchemy 등 ORM 미사용, 모든 DB작업은 SQL문으로 처리
- 비밀번호는 bcrypt로 해싱 저장
- JWT 기반 인증 (python-jose, access/refresh 토큰)
- 템플릿(Jinja2) 기반의 기본 UI 제공
- 테스트/마이그레이션용 `pytest`, `alembic` 등은 필요시 사용

---

문의/기여: [GitHub Issues](https://github.com/swanbaek/fastapi)
