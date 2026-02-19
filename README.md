# EduApp FastAPI 프로젝트

## 소개
이 프로젝트는 FastAPI 기반의 웹 애플리케이션으로, 회원가입, 로그인, 회원 목록 조회 기능을 제공합니다. SQLAlchemy와 같은 ORM을 사용하고, 로그인시 JWT 로그인 처리를 통해 사용자 인증과 인가 처리를 하는 것이 목적입니다

## 주요 기능
- **회원가입**: 사용자는 이름, 이메일, 비밀번호를 입력해 회원가입할 수 있습니다. 이메일 중복 체크 및 비밀번호 해싱(bcrypt) 적용.
- **로그인/로그아웃**: 이메일과 비밀번호로 로그인, 세션 기반 인증. 로그아웃 시 세션 삭제.
- **회원 목록**: 전체 회원 목록을 조회할 수 있습니다. (로그인 필요)
- **회원 정보 수정/삭제**: 회원 정보(이름, 이메일, 비밀번호) 수정 및 회원 삭제 기능 제공.

## 기술 스택
- Python 3.9+
- FastAPI
- PyMySQL (SQL 직접 사용)
- bcrypt (비밀번호 해싱)
- Jinja2 (템플릿)
- python-dotenv (환경변수 관리)
- Starlette SessionMiddleware (세션)

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
    login.py      # 로그인/로그아웃 API
  core/
    db.py         # DB 연결 함수 (get_connection)
  schemas/
    user.py       # Pydantic 스키마
  static/        # 정적 파일(css 등)
  templates/     # Jinja2 템플릿(html)
main.py          # FastAPI 앱 진입점
requirements.txt # 의존성 목록
```

#### User 관련 API 엔드포인트
| 메서드 | 경로                | 설명                        |
|--------|---------------------|-----------------------------|
| GET    | /users/list         | 회원목록 페이지(HTML, 로그인 필요) |
| GET    | /users              | 회원목록(JSON, 로그인 필요, JS fetch용) |
| GET    | /users/me           | 내 정보 조회 (로그인 필요)   |
| GET    | /users/{user_id}    | 특정 회원 정보 조회         |
| POST   | /users              | 회원가입 (JSON)             |
| POST   | /users2             | 회원가입 (Form)             |
| PUT    | /users/me           | 내 정보 수정 (로그인 필요)   |
| PATCH  | /users/me           | 내 정보 일부 수정 (로그인 필요) |
| DELETE | /users/me           | 회원 탈퇴 (로그인 필요)      |

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

#### Posts 관련 API 엔드포인트
| 메서드 | 경로                      | 설명                                 |
|--------|---------------------------|--------------------------------------|
| GET    | /posts/list               | 게시글 목록 페이지(HTML)             |
| GET    | /posts                    | 게시글 목록(JSON)                    |
| GET    | /posts/new                | 게시글 작성 폼(HTML, 로그인 필요)    |
| POST   | /posts/new                | 게시글 작성(폼 제출, 로그인 필요)    |
| GET    | /posts/{post_id}          | 게시글 상세(HTML, 로그인 필요시 모달) |
| GET    | /posts/{post_id}/edit     | 게시글 수정 폼(HTML, 본인만)         |
| POST   | /posts/{post_id}/edit     | 게시글 수정(폼 제출, 본인만)         |
| POST   | /posts/{post_id}/delete   | 게시글 삭제(본인만)                  |

### 화면 예시

#### 게시글 목록
![게시글 목록](./1.png)

#### 게시글 상세
![게시글 상세](./2.png)

## DB 연동 방식
- `.env` 파일 또는 환경변수에서 DB 접속 정보(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB) 로드
- `app/core/db.py`의 `get_connection()` 함수로 PyMySQL 커넥션 생성
- SQL문 직접 작성 및 실행 (예: `SELECT`, `INSERT`, `UPDATE`, `DELETE`)
- 트랜잭션/에러 발생 시 `conn.rollback()` 처리

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
- 세션 기반 인증(Starlette SessionMiddleware)
- 템플릿(Jinja2) 기반의 기본 UI 제공
- 테스트/마이그레이션용 `pytest`, `alembic` 등은 필요시 사용

---

문의/기여: [GitHub Issues](https://github.com/swanbaek/fastapi)
