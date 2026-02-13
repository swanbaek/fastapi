# DB 연결 관리 (MySQL)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#SessionLocal()은 SQLAlchemy의 세션 팩토리로, 데이터베이스와의 세션(연결)을 생성하는 역할을 한다.