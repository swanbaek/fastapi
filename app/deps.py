# 의존성 주입 관련 함수 정의
from app.core.database import SessionLocal
from sqlalchemy.orm import Session	
from fastapi import Request, HTTPException

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


def get_current_user(request: Request) -> int:
    """세션에서 로그인 중인 사용자 ID 가져오기"""

    print(">> get_current_user 세션 내용:", request.session)

    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return user_id

def get_current_user_optional(request: Request):
    """로그인 안 했으면 None 반환"""
    return request.session.get("user_id")

#Node.js의 verifyAccessToken 미들웨어 대응.
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.core.config import settings

bearer = HTTPBearer()

def get_current_user_jwt(token: str = Depends(bearer)):
    try:
        decoded = jwt.decode(
            token.credentials,
            settings.ACCESS_SECRET,
            algorithms=["HS256"]
        )
        return decoded
    except JWTError:
        raise HTTPException(status_code=403, detail="유효하지 않은 토큰입니다.")


#관리자 권한 체크
def admin_only(user = Depends(get_current_user)):
    if user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="관리자 권한 필요")
    return user
