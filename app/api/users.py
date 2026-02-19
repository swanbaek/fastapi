from fastapi import APIRouter, Depends, Body, Request, Response
from typing import List

from fastapi.responses import JSONResponse
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

@router.get("/users", response_model=List[UserOut])
def get_users():
    return service_get_all_users()


@router.get("/users/me", response_model=UserOut)
def get_me(user_id: int = Depends(get_current_user)):
    return service_get_user(user_id)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return service_get_user(user_id)


@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate):
    return service_create_user(user)


@router.put("/users/me", response_model=UserOut)
@router.patch("/users/me", response_model=UserOut)
def update_me(user: UserUpdate, user_id: int = Depends(get_current_user)):
    return service_update_my_info(user_id, user)

from fastapi import Header
#CORS 설정 필요 main.py에서 
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

# @router.delete("/users/me", status_code=204)
# def delete_me(body: UserDelete,
#         user_id: int = Depends(get_current_user),        
#         request: Request = Depends()):
#     print("body: ", body)
#     password = body.password
#     print("password received for account deletion:", password)
#     # 1. 탈퇴 처리 - DB에서 사용자 정보 삭제
#     service_delete_my_account(user_id, password)
#     # 2. 세션에서 사용자 정보 제거 (로그아웃)
#     request.session.clear()  # 세션 데이터 모두 삭제


#     # 3. 쿠키도 함께 제거 (선택)
#     response = JSONResponse(content=None, status_code=204)
#     response.delete_cookie("session")  # 브라우저 쿠키 제거
#     return response
