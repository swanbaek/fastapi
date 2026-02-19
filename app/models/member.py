from sqlalchemy import Column, Integer, String, DateTime, func, Text

from sqlalchemy.orm import relationship
from app.core.database import Base


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Refresh Token 저장
    refresh_token = Column(Text, nullable=True)  # 또는 String(500) 등의 길이 제한 가능

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

