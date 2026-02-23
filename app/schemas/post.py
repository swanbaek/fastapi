
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
	title: str
	content: str

class PostCreate(PostBase):
	file_url: Optional[str] = None
	file_name: Optional[str] = None

class PostUpdate(PostBase):
	file_url: Optional[str] = None
	file_name: Optional[str] = None

class PostOut(PostBase):
	id: int
	user_id: int
	created_at: datetime
	updated_at: Optional[datetime] = None
	hit_count: int
	file_url: Optional[str] = None
	file_name: Optional[str] = None

	class Config:
		#orm_mode = True
		from_attributes = True

# 게시글 목록 조회 시, 총 게시글 수와 함께 반환할 모델
class PostListOut(BaseModel):
    total: int
    posts: List[PostOut]

