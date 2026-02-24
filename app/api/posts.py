from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND

from app.core.database import get_db
from app.deps import get_current_user, get_current_user_jwt, get_current_user_optional
from app.schemas.post import PostListOut, PostOut
from app.services import post_service
from app.crud.post_crud import get_post_by_id
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/list")
def post_list_page(request: Request, db: Session = Depends(get_db)):
    posts = post_service.list_posts(db)
    current_user = request.session.get("user_id")
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts, "current_user": current_user})

# 페이징 처리 안할 때
# @router.get("/", response_model=List[PostOut])
# def list_posts(db: Session = Depends(get_db)):
#     return post_service.list_posts(db)

# 페이징 + 검색 처리
@router.get("/", response_model=PostListOut)
def list_posts(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10, #JS에서 3으로 설정해서 호출함. 기본값은 10이지만, 실제로는 프론트에서 전달하는 값이 우선 적용됩니다.
    search: str = ""
):
    return post_service.list_posts_paging(db, page=page, size=size, search=search)

@router.get("/new")
def new_post_form(request: Request):
    return templates.TemplateResponse("post_form.html", {"request": request})

#@router.post("/new")
@router.post("/") #리액트 연동시에는 글쓰기를 /posts로 보냄
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_jwt)
):
    post = post_service.create_new_post(
        db, title, content, file, current_user['id']
    )
    return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)
# 글쓰기 등 "로그인 필수" 라우트는 기존 get_current_user(401 발생)로 두고,
#옵셔널" 라우트(상세, 수정, 삭제)는 get_current_user_optional로 처리하면 모달이 정상적으로 뜹니다.
@router.get("/{post_id}")
def post_detail(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post_detail(db, post_id)
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})

@router.get("/{post_id}/edit")
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    return templates.TemplateResponse("post_form.html", {"request": request, "post": post})

@router.post("/{post_id}/edit")
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_jwt)
):
    post = get_post_by_id(db, post_id)
    post_service.validate_post_owner(post, current_user['id'])
    post_service.update_existing_post(db, post, title, content, file)
    return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)

@router.post("/{post_id}/delete")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user_jwt)):
    post = get_post_by_id(db, post_id)
    post_service.validate_post_owner(post, current_user['id'])
    post_service.delete_post_with_file(db, post)
    return {"result": "success"}
