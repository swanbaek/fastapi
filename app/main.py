from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api import posts
from app.api import users
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/users/list", response_class=HTMLResponse)
async def users_page(request: Request):
    if not request.session.get("user_id"):
        return templates.TemplateResponse("users.html", {"request": request, "auth_message": "로그인 해야 이용 가능합니다."})
    return templates.TemplateResponse("users.html", {"request": request, "auth_message": None})

# 마이페이지 라우트가 없으면 추가
@app.get("/mypage", response_class=HTMLResponse)
async def mypage(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("mypage.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

app.include_router(posts.router)
app.include_router(users.router)
