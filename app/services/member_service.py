import bcrypt
from datetime import datetime
from fastapi import HTTPException
from app.crud.member import (
    get_member_by_id,
    get_member_by_email,
    get_all_members,
    create_member,
    update_member,
    delete_member
)

def service_get_all_members(db):
    return get_all_members(db)

def service_get_member(db, member_id: int):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(404, "Member not found")
    return member

def service_create_member(db, name, email, password):
    if get_member_by_email(db, email):
        raise HTTPException(400, "이미 등록된 이메일입니다.")
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(400, "비밀번호는 72바이트(약 72자) 이하로 입력하세요.")
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    now = datetime.now()
    member_id = create_member(db, name, email, hashed_pw, now)
    return {"result": "success", "message": "회원가입이 완료되었습니다."}

def service_update_my_info(db, member_id: int, name=None, email=None, password=None):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(404, "회원을 찾을 수 없습니다.")
    if name:
        member.name = name
    if email:
        if get_member_by_email(db, email) and email != member.email:
            raise HTTPException(400, "이미 등록된 이메일입니다.")
        member.email = email
    if password:
        member.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.commit()
    db.refresh(member)
    return {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "created_at": member.created_at,
        "role": member.role
    }

def service_delete_my_account(db, member_id: int, password: str):
    member = get_member_by_id(db, member_id)
    if not member:
        raise HTTPException(404, "회원을 찾을 수 없습니다.")
    if not bcrypt.checkpw(password.encode(), member.password.encode()):
        raise HTTPException(401, "비밀번호가 일치하지 않습니다.")
    db.delete(member)
    db.commit()
    return None
