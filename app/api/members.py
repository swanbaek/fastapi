from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
from app.deps import get_db, get_current_user_jwt
from app.models.member import Member

#pip install bcrypt passlib 두 라이브러리 버전을 맞추려면 bcrypt==4.0.1, passlib[bcrypt] 설치 필요
#pip install "bcrypt==4.0.1"
# RESTful: /api/users (회원가입 등)
router = APIRouter(prefix="/api", tags=["members"])


# GET /api/members (회원 목록)
@router.get("/members")
def list_members(user=Depends(get_current_user_jwt), db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return [
        {"id": m.id, "name": m.name, "email": m.email, "created_at": m.created_at}
        for m in members
    ]

# 회원가입 (POST /api/users)

@router.post("/users")
def create_user(
    name: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    if db.query(Member).filter(Member.email == email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    print("******create_user()=> name:", name, "email:", email, "password:", password)
    print(f"[DEBUG] password type: {type(password)}, repr: {repr(password)}")
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="비밀번호는 72바이트(약 72자) 이하로 입력하세요.")
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_member = Member(name=name, email=email, password=hashed_pw)
    db.add(new_member)
    try:
        db.commit()
        db.refresh(new_member)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="회원가입 실패: 중복된 정보가 있습니다.")

    return {"result": "success", "message": "회원가입이 완료되었습니다."}
