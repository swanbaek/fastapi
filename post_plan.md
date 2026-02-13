# 게시판(Post) 기능 설계 및 구현 계획

## 1. 목표
- 게시글 CRUD(생성, 조회, 수정, 삭제) API 및 웹 UI 제공
- SQLAlchemy ORM을 사용하여 MySQL DB와 연동
- 게시글 작성자(회원) 연동

---

## 2. DB 테이블 설계 (MySQL)

```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT NULL,
    hit_count int default 0, --조회수
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 3. SQLAlchemy 모델 (app/models/post.py)
- `Post` 클래스: posts 테이블과 매핑
- 주요 필드: id, title, content, user_id, created_at, updated_at
- 관계: User(작성자)와 ForeignKey, relationship 설정
- 📌 Model = “DB 테이블을 어떻게 만들 것인가?”
→ 테이블 설계도 + ORM 기능 포함
---

## 4. Pydantic 스키마 (app/schemas/post.py)
- `PostCreate`: 게시글 생성용(title, content)
- `PostUpdate`: 게시글 수정용(title, content, optional)
- `PostOut`: 게시글 조회용(id, title, content, user_id, created_at, updated_at)
- 📌 Schema = “API 요청/응답은 어떤 모양으로 받을 것인가?”
→ DTO(Data Transfer Object) 역할
---

## 5. DB 세션 관리
- `app/core/database.py`의 `SessionLocal`을 FastAPI 의존성(Depends)로 주입

---

## 6. API 라우터 (app/api/posts.py)
- `/posts` [GET]: 전체 게시글 목록 조회 (페이징/검색 옵션 고려)
- `/posts/{post_id}` [GET]: 게시글 상세 조회
- `/posts` [POST]: 게시글 작성 (로그인 필요, user_id 연동)
- `/posts/{post_id}` [PUT/PATCH]: 게시글 수정 (작성자만 가능)
- `/posts/{post_id}` [DELETE]: 게시글 삭제 (작성자만 가능)

---

## 7. 인증/권한
- 게시글 작성/수정/삭제는 로그인(세션) 필요
- 본인 글만 수정/삭제 가능하도록 user_id 체크

---

## 8. 기타
- Alembic을 통한 마이그레이션 적용
- 게시글 목록/상세 페이지용 Jinja2 템플릿 추가
- 추후 댓글, 파일첨부 등 확장 고려
