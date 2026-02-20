
# 게시글 삭제 (첨부파일까지 삭제)
import os
from sqlalchemy.orm import Session

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')

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
def create_new_post(db: Session, title: str, content: str, file, current_user):
    print(">> create_new_post() current_user:", current_user)  # 디버깅용 출력
    file_url = save_upload_file(file) if file else None  # 파일 업로드 처리
    file_name = file.filename if file and file.filename else None  # 원본 파일명 저장

    post = Post(
        title=title,
        content=content,
        user_id=current_user,
        file_url=file_url,
        file_name=file_name,
        created_at=datetime.now(),
        hit_count=0
    )
    return post_crud.create_post(db, post)

# 게시글 수정
from datetime import datetime
def update_existing_post(db: Session, post: Post, title: str, content: str, file):
    post.title = title
    post.content = content
    post.updated_at = datetime.now()  # 수정시각 갱신

    # 파일이 새로 업로드된 경우 기존 파일 삭제 후 새 파일 저장
    if file and file.filename:
        # 기존 파일 삭제
        if post.file_url:
            file_name = post.file_url.split('/static/uploads/')[-1]
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
        # 새 파일 저장
        post.file_url = save_upload_file(file)
        post.file_name = file.filename
    # 파일을 새로 업로드하지 않으면 기존 file_url/file_name 유지

    return post_crud.update_post(db, post)

# 게시글 소유자 검증 (권한 체크)
def validate_post_owner(post, current_user_id):
    if not post or post.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="권한 없음")

def delete_post_with_file(db: Session, post: Post):
    """
    게시글 삭제 시 첨부파일이 있으면 uploads 폴더에서 파일도 함께 삭제
    """
    # 첨부파일 경로가 있으면 파일 삭제 시도
    if post.file_url:
        # file_url 예: /static/uploads/20260219123456_filename.jpg
        file_name = post.file_url.split('/static/uploads/')[-1]
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                # 파일 삭제 실패 시 무시하고 게시글만 삭제
                pass
    # DB에서 게시글 삭제
    post_crud.delete_post(db, post)

