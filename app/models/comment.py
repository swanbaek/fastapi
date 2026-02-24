
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from app.core.database import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    author = relationship("Member", foreign_keys=[user_id])
    post = relationship("Post", back_populates="comments")
    #SQLAlchemy에서 두 테이블(모델) 간의 양방향 관계를 명확하게 연결해주는 옵션
    #Post 모델에서 comments = relationship("Comment", back_populates="post", passive_deletes=True)로 설정되어 있어야 함
    # post.comments는 해당 게시글에 달린 모든 댓글 목록을 의미하게 됨.
    # 이렇게 하면 Post와 Comment가 서로 연결되어, 한쪽에서 값을 바꾸면 다른쪽에서도 자동 반영된다
    #즉, 두 모델의 관계를 "쌍방향으로 동기화"해주는 역할을 합니다.
