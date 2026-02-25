from app.models.comment import Comment
from sqlalchemy.orm import Session, joinedload

def get_comments_by_post(db: Session, post_id: int):
    return (
        db.query(Comment)
        .options(joinedload(Comment.author))
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

def create_comment(db: Session, post_id: int, user_id: int, content: str):
    comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None
    if comment.user_id != user_id:
        return False
    db.delete(comment)
    db.commit()
    return True

def update_comment(db: Session, comment_id: int, user_id: int, content: str):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        return None
    if comment.user_id != user_id:
        return False
    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment