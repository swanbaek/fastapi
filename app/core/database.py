# DB 연결 관리 (MySQL)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL, pool_pre_ping=True, echo=True)  
# echo=True는 SQLAlchemy가 실행하는 SQL 쿼리를 콘솔에 출력하도록 하는 설정. 
# 디버깅 시 유용하지만, 운영 환경에서는 성능 저하를 일으킬 수 있으므로 주의해서 사용해야 합니다.
#pool_pre_ping=True 옵션은 DB 커넥션이 끊어졌는지 미리 확인(ping)하고, 끊어졌다면 자동으로 새 커넥션을 만들어주는 기능
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#트랜잭션 단위로 작동하도록 하기 위해 autocommit=False, autoflush=False로 설정.

# FastAPI 의존성 주입용 DB 세션 generator
from sqlalchemy.orm import Session
from typing import Generator

# SQLAlchemy Base for models
Base = declarative_base()
#Base = declarative_base()는 SQLAlchemy에서 모든 모델(테이블 클래스)의 부모가 되는 "기본 클래스"를 생성
#이 Base 클래스를 상속하여 각 모델을 정의하면, SQLAlchemy는 해당 모델을 데이터베이스 테이블과 매핑할 수 있다. 
#또한, Base.metadata.create_all(bind=engine)와 같은 명령을 사용하여 데이터베이스에 필요한 
# 테이블을 자동으로 생성할 수 있게 됨. ==> app/main.py에서 Base.metadata.create_all(bind=engine)로 테이블 생성
def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()