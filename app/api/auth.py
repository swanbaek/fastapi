from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.core.jwt_handler import create_access_token, create_refresh_token
from app.core.database import get_db
from app.models.member import Member
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 회원가입 API
from fastapi import Body
from sqlalchemy.exc import IntegrityError

@router.post("/signup")
def signup(
    name: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    # 이메일 중복 체크
    if db.query(Member).filter(Member.email == email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")

    hashed_pw = pwd_context.hash(password)
    new_member = Member(name=name, email=email, password=hashed_pw)
    db.add(new_member)
    try:
        db.commit()
        db.refresh(new_member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="회원가입 실패: 중복된 정보가 있습니다.")

    return {"result": "success", "message": "회원가입이 완료되었습니다."}

@router.post("/login")
def login(email: str, passwd: str, db: Session = Depends(get_db)):
    user = db.query(Member).filter(Member.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

    if not pwd_context.verify(passwd, user.passwd):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

    payload = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    user.refresh_token = refresh_token
    db.commit()

    return {
        "result": "success",
        "message": "로그인 성공",
        "data": {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            **payload
        }
    }


from jose import jwt, JWTError
#6. RefreshToken 재발급 API
@router.post("/refresh")
def refresh_token(refreshToken: str, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(refreshToken, settings.REFRESH_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=403, detail="유효하지 않은 refreshToken")

    user = db.query(Member).filter(Member.refresh_token == refreshToken).first()
    if not user:
        raise HTTPException(status_code=403, detail="인증받지 않은 회원입니다.")

    new_access = create_access_token({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    })

    return {"accessToken": new_access}


# 7. 로그아웃 API (RefreshToken 제거)
@router.post("/logout")
def logout(email: str, db: Session = Depends(get_db)):
    user = db.query(Member).filter(Member.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="잘못된 요청입니다")

    user.refresh_token = None
    db.commit()

    return {"result": "success", "message": "로그아웃 완료"}
