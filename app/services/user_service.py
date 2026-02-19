import bcrypt
from datetime import datetime
from fastapi import HTTPException
from app.crud.user import (
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    create_user,
    update_user,
    delete_user
)


def service_get_all_users():
    return get_all_users()


def service_get_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


def service_create_user(user):
    # 중복 이메일 확인
    if get_user_by_email(user.email):
        raise HTTPException(400, "이미 등록된 이메일입니다.")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    now = datetime.now()

    user_id = create_user(user.name, user.email, hashed_pw, now)

    return {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "created_at": now
    }


def service_update_my_info(user_id: int, user_update):
    current = get_user_by_id(user_id)
    if not current:
        raise HTTPException(404, "사용자를 찾을 수 없습니다.")

    new_name = user_update.name or current["name"]
    new_email = user_update.email or current["email"]

    if user_update.email and user_update.email != current["email"]:
        if get_user_by_email(user_update.email):
            raise HTTPException(400, "이미 등록된 이메일입니다.")

    hashed_pw = None
    if user_update.password:
        hashed_pw = bcrypt.hashpw(user_update.password.encode(), bcrypt.gensalt()).decode()

    update_user(user_id, new_name, new_email, hashed_pw)

    return {
        "id": user_id,
        "name": new_name,
        "email": new_email,
        "created_at": current["created_at"]
    }


def service_delete_my_account(user_id: int, password: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        raise HTTPException(401, "비밀번호가 일치하지 않습니다.")

    delete_user(user_id)
    return {"msg": "회원 탈퇴 완료"}