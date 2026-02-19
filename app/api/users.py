from fastapi import APIRouter, Depends, Body, Form, Request, Response
from typing import List

from fastapi.responses import JSONResponse, HTMLResponse
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserDelete
from app.deps import get_current_user
from app.services.user_service import (
    service_get_all_users,
    service_get_user,
    service_create_user,
    service_update_my_info,
    service_delete_my_account
)

router = APIRouter()

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/users", response_class=HTMLResponse)
def get_users(request: Request, current_user: int = Depends(get_current_user)):
    # 로그인 안 했으면 auth_message 전달
    if not current_user:
        return templates.TemplateResponse("users.html", {"request": request, "auth_message": "로그인이 필요합니다."})
    return templates.TemplateResponse("users.html", {"request": request})


@router.get("/users/me", response_model=UserOut)
def get_me(user_id: int = Depends(get_current_user)):
    return service_get_user(user_id)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return service_get_user(user_id)

# JSON Body로 받는 경우- 비동기방식
@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    print("create_user()=> user:", user)
    return service_create_user(user)

# Form 데이터로 동기식으로 받는 경우
@router.post("/users2", response_model=UserOut)
def create_user2(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    user = UserCreate(name=name, email=email, password=password)
    return service_create_user(user)

@router.put("/users/me", response_model=UserOut)
@router.patch("/users/me", response_model=UserOut)
def update_me(user: UserUpdate, user_id: int = Depends(get_current_user)):
    return service_update_my_info(user_id, user)

from fastapi import Header
#CORS 설정 필요 main.py에서 
# 기본값이 없는 인자는 항상 기본값이 있는 인자보다 앞에 와야 한다 request가 먼저 와야 함
@router.delete("/users/me", status_code=204)
def delete_me(
    request: Request,
    x_password: str = Header(..., alias="X-Password"),  # "X-Password" 헤더 받기, convert_underscores=False로 대소문자 구분
    user_id: int = Depends(get_current_user),
):
    print("x-password 받은 헤더값:", x_password)
    service_delete_my_account(user_id, x_password)

    request.session.clear()
    response = Response(status_code=204)
    response.delete_cookie("session")
    return response
