
from pydantic import BaseModel
from typing import Optional
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
		orm_mode = True
