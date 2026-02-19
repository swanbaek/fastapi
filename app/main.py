from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


from app.api import posts
from app.api import users
from app.api.login import router as login_router
from starlette.middleware.sessions import SessionMiddleware

# SQLAlchemy 모델 import 및 테이블 생성
from app.models.user import User
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
    if not request.session.get("user_id"):
        return templates.TemplateResponse("users.html", {"request": request, "auth_message": "로그인 해야 이용 가능합니다."})
    return templates.TemplateResponse("users.html", {"request": request, "auth_message": None})

# 마이페이지 라우트가 없으면 추가
@app.get("/mypage", response_class=HTMLResponse)
async def mypage(request: Request):
    if not request.session.get("user_id"):
        print("No user_id in session, redirecting to home.")
        # return RedirectResponse("/", status_code=302)
        # 로그인 안 했으면 안내 메시지와 함께 렌더링
        return templates.TemplateResponse(
            "mypage.html",
            {"request": request, "auth_message": "로그인 해야 이용 가능합니다."}
        )
    
    # DB에서 user 정보 조회
    # user = ... # user_id로 DB에서 조회
    user_id = request.session.get("user_id")
    user = user_service.service_get_user(user_id)  # DB에서 user_id로 사용자 정보 조회하는 함수 필요

    print("user_id found in session:", user)
    return templates.TemplateResponse("mypage.html", {"request": request, "user": user})

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login_router)
