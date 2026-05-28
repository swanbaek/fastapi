from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware

from app.core.database import engine
from app.models.post import Base
from app.models import post, comment, member

from app.api import comments, posts, post_api
from app.api.members import router as members_router
from app.api.auth import router as auth_router

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "x-password"],
)

# Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="supersecret",
    max_age=1800,
)

# Static / Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# ------- HTML Page Routes -------
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # return templates.TemplateResponse("index.html", {"request": request}) #옛날 버전
    return templates.TemplateResponse(request=request, name="index.html") #최신 문법

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html")

@app.get("/mypage", response_class=HTMLResponse)
async def mypage(request: Request):
    return templates.TemplateResponse(request=request, name="mypage.html")

@app.get("/users/list", response_class=HTMLResponse)
async def user_list_page(request: Request):
    return templates.TemplateResponse(request=request, name="users.html")


# ------- API Routes -------
# app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(auth_router)
app.include_router(members_router, prefix="/api")
app.include_router(post_api.router)