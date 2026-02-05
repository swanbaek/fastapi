# 의존성 주입 관련 함수 정의
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
