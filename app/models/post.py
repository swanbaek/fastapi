
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


from app.core.database import Base

class Post(Base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(200), nullable=False)
	content = Column(Text, nullable=False)
	user_id = Column(Integer, ForeignKey('members.id'), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.now)
	updated_at = Column(DateTime, nullable=True)
	hit_count = Column(Integer, default=0)
	file_url = Column(String(300), nullable=True)
	file_name = Column(String(200), nullable=True)

	author = relationship("Member", backref="posts", foreign_keys=[user_id])

	#author는 실제 DB 컬럼이 아니라, SQLAlchemy ORM에서 관계(relationship)를 편하게 다루기 위해 사용하는 "파이썬 속성명"
	#Post 모델에서 author = relationship("Member", ...)는 user_id를 통해 연결된 Member 객체를 파이썬에서 author라는 이름으로 접근할 수 있게 해줍니다.
	#즉, post.author는 post.user_id에 해당하는 Member 객체를 의미합니다.
	#반대로, Member.posts는 해당 회원이 작성한 모든 Post 목록을 의미합니다.