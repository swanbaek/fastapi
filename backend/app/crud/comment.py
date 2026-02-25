from sqlalchemy.orm import Session
from app.models.comment import Comment

# 댓글 목록 조회
def get_comments_by_post(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()

# 댓글 작성
def create_comment(db: Session, post_id: int, user_id: int, content: str):
    comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

# 댓글 삭제
def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
