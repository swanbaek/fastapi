from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
from app.deps import get_db, get_current_user_jwt
from app.models.member import Member
from app.services import member_service

router = APIRouter()

# 회원 목록 (GET /users)
@router.get("/users")
def list_members(user=Depends(get_current_user_jwt), db: Session = Depends(get_db)):
	return member_service.service_get_all_members(db)

# 회원가입 (POST /users)
@router.post("/users")
def create_user(
	name: str = Body(...),
	email: str = Body(...),
	password: str = Body(...),
	db: Session = Depends(get_db)
):
	return member_service.service_create_member(db, name, email, password)

# 내 정보 조회 (GET /users/me)
@router.get("/users/me")
def get_my_info(user_id=Depends(get_current_user_jwt), db: Session = Depends(get_db)):
	return member_service.service_get_member(db, user_id)

# 내 정보 수정 (PUT /users/me)
@router.put("/users/me")
def update_my_info(
	user_id=Depends(get_current_user_jwt),
	name: str = Body(None),
	email: str = Body(None),
	password: str = Body(None),
	db: Session = Depends(get_db)
):
	return member_service.service_update_my_info(db, user_id, name, email, password)

# 회원 탈퇴 (DELETE /users/me)
from fastapi import Header

@router.delete("/users/me", status_code=204)
def delete_my_account(
    user_id=Depends(get_current_user_jwt),
    x_password: str = Header(..., alias="X-Password"),
    db: Session = Depends(get_db)
):
    member_service.service_delete_my_account(db, user_id, x_password)
    return None