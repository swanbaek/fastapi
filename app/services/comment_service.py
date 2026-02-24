from app.crud import comment_crud
from sqlalchemy.orm import Session

def get_comments_by_post(db: Session, post_id: int):
    return comment_crud.get_comments_by_post(db, post_id)

def create_comment(db: Session, post_id: int, user_id: int, content: str):
    return comment_crud.create_comment(db, post_id, user_id, content)

def delete_comment(db: Session, comment_id: int, user_id: int):
    return comment_crud.delete_comment(db, comment_id, user_id)

def update_comment(db: Session, comment_id: int, user_id: int, content: str):
    return comment_crud.update_comment(db, comment_id, user_id, content)