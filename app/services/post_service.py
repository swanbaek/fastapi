
# 게시글 서비스 계층: 비즈니스 로직 담당
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.crud import post_crud
from app.models.post import Post
from app.services.file_service import save_upload_file

# 게시글 전체 목록 조회
def list_posts(db: Session):
    return post_crud.get_posts(db)

# 게시글 상세 조회 및 조회수 증가
def get_post_detail(db: Session, post_id: int):
    post = post_crud.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글 없음")

    post.hit_count += 1  # 조회수 증가
    db.commit()          # DB 반영
    db.refresh(post)     # 갱신된 post 반환
    return post

# 새 게시글 생성
def create_new_post(db: Session, title: str, content: str, file, current_user_id: int):
    file_url = save_upload_file(file) if file else None  # 파일 업로드 처리
    file_name = file.filename if file and file.filename else None  # 원본 파일명 저장

    post = Post(
        title=title,
        content=content,
        user_id=current_user_id,
        file_url=file_url,
        file_name=file_name,
        created_at=datetime.now(),
        hit_count=0
    )
    return post_crud.create_post(db, post)

# 게시글 수정
def update_existing_post(db: Session, post: Post, title: str, content: str, file):
    post.title = title
    post.content = content

    if file:
        post.file_url = save_upload_file(file)  # 파일이 있으면 새로 저장

    return post_crud.update_post(db, post)

# 게시글 소유자 검증 (권한 체크)
def validate_post_owner(post, current_user_id):
    if not post or post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="권한 없음")
