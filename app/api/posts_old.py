
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from app.core.database import get_db
from app.models import post as post_model
from app.schemas import post as post_schema
from sqlalchemy.orm import Session,joinedload
from typing import List
from app.services.file_service import save_upload_file
from app.deps import get_current_user
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/list")
def post_list_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(post_model.Post).order_by(post_model.Post.id.desc()).all()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})

@router.get("/", response_model=List[post_schema.PostOut])
def list_posts(request: Request, db: Session = Depends(get_db)):
	posts = db.query(post_model.Post).order_by(post_model.Post.id.desc()).all()
	return posts

@router.get("/new")
def new_post_form(request: Request, current_user=Depends(get_current_user)):
	# 로그인 없이도 글쓰기 폼 접근 가능
	return templates.TemplateResponse("post_form.html", {"request": request, "current_user": current_user})

@router.post("/new")
def create_post(request: Request,
            title: str = Form(...),
            content: str = Form(...),
            file: UploadFile = File(None),
            db: Session = Depends(get_db),
            current_user=Depends(get_current_user)):
	if not current_user:
		raise HTTPException(status_code=401, detail="로그인 필요")
	file_url = None
	if file:
		file_url = save_upload_file(file)
	print('#'*100)
	print('current_user:', current_user)
	post = post_model.Post(
		title=title,
		content=content,
		user_id=current_user,  # author_id -> user_id
		file_url=file_url,
		created_at=datetime.now(),
		hit_count=0
	)
	db.add(post)
	db.commit()
	db.refresh(post)
	return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)

@router.get("/{post_id}")
def post_detail(request: Request, post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
	if not post:
		raise HTTPException(status_code=404, detail="게시글 없음")
	post.hit_count += 1
	db.commit()
	db.refresh(post)
	return templates.TemplateResponse("post_detail.html", {"request": request, "post": post, "current_user": current_user})

@router.get("/{post_id}/edit")
def edit_post_form(request: Request, post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
	if not post or post.author_id != current_user.id:
		raise HTTPException(status_code=403, detail="권한 없음")
	return templates.TemplateResponse("post_form.html", {"request": request, "post": post, "current_user": current_user})

@router.post("/{post_id}/edit")
def update_post(request: Request,
				post_id: int,
				title: str = Form(...),
				content: str = Form(...),
				file: UploadFile = File(None),
				db: Session = Depends(get_db),
				current_user=Depends(get_current_user)):
	#post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
	post = (
        db.query(post_model.Post)
        .options(joinedload(post_model.Post.user))  # Post 모델에 relationship이 정의되어 있다면
        .filter(post_model.Post.id == post_id)
        .first()
    )
	if not post or post.author_id != current_user.id:
		raise HTTPException(status_code=403, detail="권한 없음")
	post.title = title
	post.content = content
	if file:
		post.file_url = save_upload_file(file)
	db.commit()
	db.refresh(post)
	return RedirectResponse(url=f"/posts/{post.id}", status_code=HTTP_302_FOUND)

@router.post("/{post_id}/delete")
def delete_post(request: Request, post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
	post = db.query(post_model.Post).filter(post_model.Post.id == post_id).first()
	if not post or post.author_id != current_user.id:
		raise HTTPException(status_code=403, detail="권한 없음")
	db.delete(post)
	db.commit()
	return RedirectResponse(url="/posts", status_code=HTTP_302_FOUND)

# 댓글 추가/삭제 라우팅은 필요시 구현