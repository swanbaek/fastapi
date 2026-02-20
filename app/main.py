from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from app.api import posts
from app.api.members import router as members_router
from app.api.auth import router as auth_router
from app.api.login import router as login_router
from app.api.members import router as members_router
from starlette.middleware.sessions import SessionMiddleware

# SQLAlchemy 모델 import 및 테이블 생성
from app.models.post import Post
from app.core.database import engine
from app.models.post import Base
from app.services import user_service


Base.metadata.create_all(bind=engine)


app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영시에는 도메인 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*","x-password"],  # "x-password" 헤더 허용 추가
)

app.add_middleware(SessionMiddleware, 
                secret_key="supersecret",
                max_age=1800  # 1800초 = 30분
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

#include_in_schema=False는 해당 엔드포인트를 API 문서(Swagger / Redoc)에 표시하지 않도록 숨기는 설정. 
# 일반적으로 favicon과 같이 API 문서에 포함될 필요가 없는 엔드포인트에 사용됩니다.
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

@app.get("/users/list", response_class=HTMLResponse)
async def users_page(request: Request):
    # 항상 users.html 렌더링, 인증/권한은 JS에서 처리
    return templates.TemplateResponse("users.html", {"request": request})

# 마이페이지 라우트가 없으면 추가
@app.get("/mypage", response_class=HTMLResponse)
async def mypage(request: Request):
    # SSR에서는 인증/사용자 정보 전달 없이 항상 mypage.html 렌더링
    return templates.TemplateResponse("mypage.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

app.include_router(posts.router)
app.include_router(members_router, prefix="/api")
app.include_router(auth_router)
app.include_router(login_router)
