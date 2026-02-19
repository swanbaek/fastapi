from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND

from app.core.database import get_db
from app.deps import get_current_user
from app.api.users import get_current_user
from app.schemas.post import PostOut
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

@router.get("/", response_model=List[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return post_service.list_posts(db)

@router.get("/new")
def new_post_form(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse("post_form.html", {"request": request, "current_user": current_user})

@router.post("/new")
def create_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = post_service.create_new_post(
        db, title, content, file, current_user
    )
    return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)

@router.get("/{post_id}")
def post_detail(request: Request, post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = post_service.get_post_detail(db, post_id)
    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post, "current_user": current_user})

@router.get("/{post_id}/edit")
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = get_post_by_id(db, post_id)
    post_service.validate_post_owner(post, current_user)
    return templates.TemplateResponse("post_form.html", {"request": request, "post": post, "current_user": current_user})

@router.post("/{post_id}/edit")
def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    post = get_post_by_id(db, post_id)
    post_service.validate_post_owner(post, current_user)
    post_service.update_existing_post(db, post, title, content, file)
    return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)

@router.post("/{post_id}/delete")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = get_post_by_id(db, post_id)
    post_service.validate_post_owner(post, current_user)
    post_service.delete_post(db, post)
    return RedirectResponse(url="/posts", status_code=HTTP_302_FOUND)
