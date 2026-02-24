from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.comment_schema import CommentCreate, CommentOut
from app.services import comment_service
from app.deps import get_current_user_jwt
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])
# 댓글 목록 조회
@router.get("/post/{post_id}", response_model=List[CommentOut])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comments_by_post(db, post_id)

# 댓글 작성
@router.post("/post/{post_id}", response_model=CommentOut)
def create_comment(
    post_id: int,
    data: CommentCreate,
    current_user: dict = Depends(get_current_user_jwt),
    db: Session = Depends(get_db)
):
    return comment_service.create_comment(db, post_id, current_user["id"], data.content)

# 댓글 삭제

@router.delete("/{comment_id}", response_model=dict)
def delete_comment(
    comment_id: int,
    current_user: dict = Depends(get_current_user_jwt),
    db: Session = Depends(get_db)
):
    result = comment_service.delete_comment(db, comment_id, current_user["id"])
    if result is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if result is False:
        raise HTTPException(status_code=403, detail="본인만 삭제할 수 있습니다.")
    return {"result": "success"}

# 댓글 수정
@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    data: CommentCreate,
    current_user: dict = Depends(get_current_user_jwt),
    db: Session = Depends(get_db)
):
    result = comment_service.update_comment(db, comment_id, current_user["id"], data.content)
    if result is None:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if result is False:
        raise HTTPException(status_code=403, detail="본인만 수정할 수 있습니다.")
    return result