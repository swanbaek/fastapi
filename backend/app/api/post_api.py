from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.deps import get_current_user_jwt
from app.schemas.post import PostListOut, PostOut
from app.services import post_service
from app.crud.post_crud import get_post_by_id
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


# ──────────────────────────────────────────────
# 목록 조회 (페이징 + 검색)  ← 기존 연동 잘 됨, 그대로 유지
# GET /posts/?page=1&size=10&search=
# ──────────────────────────────────────────────
@router.get("/", response_model=PostListOut)
def list_posts(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10,
    search: str = ""
):
    return post_service.list_posts_paging(db, page=page, size=size, search=search)


# ──────────────────────────────────────────────
# 글 작성  ← 리다이렉트 → JSON 응답으로 변경
# POST /posts/
# ──────────────────────────────────────────────
@router.post("/", response_model=PostOut)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_jwt)
):
    post = post_service.create_new_post(
        db, title, content, file, current_user["id"]
    )
    return post  # 생성된 글 객체를 JSON으로 반환 (프론트에서 post.id로 상세 이동)


# ──────────────────────────────────────────────
# 글 상세 조회
# GET /posts/{post_id}
# ──────────────────────────────────────────────
@router.get("/{post_id}", response_model=PostOut)
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_detail(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


# ──────────────────────────────────────────────
# 글 수정
# PUT /posts/{post_id}
# ──────────────────────────────────────────────
@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_jwt)
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    post_service.validate_post_owner(post, current_user["id"])
    updated_post = post_service.update_existing_post(db, post, title, content, file)
    return updated_post  # 수정된 글 객체를 JSON으로 반환


# ──────────────────────────────────────────────
# 글 삭제
# DELETE /posts/{post_id}
# ──────────────────────────────────────────────
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_jwt)
):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    post_service.validate_post_owner(post, current_user["id"])
    post_service.delete_post_with_file(db, post)
    return {"result": "success", "deleted_id": post_id}