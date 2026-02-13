
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Post(Base):
	__tablename__ = 'posts'

	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(200), nullable=False)
	content = Column(Text, nullable=False)
	user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.now)
	updated_at = Column(DateTime, nullable=True)
	hit_count = Column(Integer, default=0)
	file_url = Column(String(300), nullable=True)
	file_name = Column(String(200), nullable=True)
