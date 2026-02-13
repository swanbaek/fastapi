# 의존성 주입 관련 함수 정의
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
	'''	DB 세션을 안전하게 생성·관리하기 위한 의존성(Dependency) 함수
		요청이 들어올 때마다 DB 세션을 하나 열고, 요청이 끝나면 알아서 닫아주는 역할을 한다
	'''
	db = SessionLocal()
	#DB에 접근하기 위한 연결(Session)을 하나 생성 이 세션 객체를 사용해서 쿼리 실행/객체 조회/추가,수정,삭제 등을 수행
	try:
		yield db #의존성 주입을 통해 라우터 함수에 전달 yield로 FastAPI 라우터에 DB 세션 제공
		#FastAPI는 yield를 보자마자 "라이터 함수에게 이 db 객체를 전달하자!" 그리고 라우터 함수 실행을 시작함
	finally:
		db.close() # 요청이 끝나면 DB 세션 닫기

# --- IGNORE ---
# SQLAlchemy

# 클라이언트 요청 →  get_db() 실행
#                   ├─ db = SessionLocal()        (세션 열기)
#                   ├─ yield db  ───────────────► (라우터로 db 전달)
# 라우터 실행 끝 ◄─────── (다시 돌아옴)
#                   └─ finally: db.close()        (세션 닫기)
