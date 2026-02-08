# FastAPI 세션 기반 로그인 처리 정리

## 1. 주요 라이브러리 및 환경
- FastAPI, Starlette (SessionMiddleware)
- bcrypt (비밀번호 해시/검증)
- itsdangerous (세션 쿠키 변조 방지, SessionMiddleware 내부에서 사용)
- pymysql (DB 연동)
- python-dotenv (환경변수 관리)

## 2. 세션 미들웨어 설정
```python
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
```
- secret_key는 세션 쿠키의 안전한 서명에 사용됨 (itsdangerous가 내부적으로 사용됨)

## 3. 회원가입 (비밀번호 암호화)
- 회원가입 시 bcrypt로 비밀번호를 해싱하여 DB에 저장
```python
import bcrypt
hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
```

## 4. 로그인 처리 (/login)
- email, password를 받아 DB에서 사용자 조회
- bcrypt로 비밀번호 검증
- 성공 시 request.session에 user_id, user_name 등 저장 (세션 쿠키 자동 발급)
```python
@router.post("/login")
def login(request: Request, response: Response):
    # ... (email, password 추출)
    # DB에서 user 조회
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    request.session['user_id'] = user['id']
    request.session['user_name'] = user['name']
    return {"id": user['id'], "name": user['name'], "email": user['email']}
```

## 5. 로그아웃 처리 (/logout)
- 세션 정보 삭제
```python
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"msg": "로그아웃 완료"}
```

## 6. 프론트엔드 처리
- 로그인 폼에서 /login으로 POST 요청
- 성공 시 세션 쿠키가 자동 저장되어 인증 유지
- 별도 토큰 저장 불필요

## 7. itsdangerous란?
- 세션 쿠키의 변조 방지(서명)를 위해 SessionMiddleware 내부에서 사용하는 라이브러리
- 클라이언트가 쿠키 값을 임의로 바꿔도 서버에서 위조 여부를 검증할 수 있게 해줌
- Flask, FastAPI 등에서 세션/토큰 보안에 널리 사용

---

## 참고
- 세션 기반 인증은 서버가 세션 상태를 관리하며, 보안상 HttpOnly 쿠키 사용이 권장됨
- JWT 방식으로 발전시키고 싶다면, 세션 대신 JWT 발급/검증 로직을 추가하면 됨
# FastAPI 세션 기반 로그인 처리 정리

## 1. 주요 라이브러리 및 환경
- FastAPI, Starlette (SessionMiddleware)
- bcrypt (비밀번호 해시/검증)
- itsdangerous (세션 쿠키 변조 방지, SessionMiddleware 내부에서 사용)
- pymysql (DB 연동)
- python-dotenv (환경변수 관리)

## 2. 세션 미들웨어 설정
```python
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
```
- secret_key는 세션 쿠키의 안전한 서명에 사용됨 (itsdangerous가 내부적으로 사용됨)

## 3. 회원가입 (비밀번호 암호화)
- 회원가입 시 bcrypt로 비밀번호를 해싱하여 DB에 저장
```python
import bcrypt
hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
```

## 4. 로그인 처리 (/login)
- email, password를 받아 DB에서 사용자 조회
- bcrypt로 비밀번호 검증
- 성공 시 request.session에 user_id, user_name 등 저장 (세션 쿠키 자동 발급)
```python
@router.post("/login")
def login(request: Request, response: Response):
    # ... (email, password 추출)
    # DB에서 user 조회
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    request.session['user_id'] = user['id']
    request.session['user_name'] = user['name']
    return {"id": user['id'], "name": user['name'], "email": user['email']}
```

## 5. 로그아웃 처리 (/logout)
- 세션 정보 삭제
```python
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"msg": "로그아웃 완료"}
```

## 6. 프론트엔드 처리
- 로그인 폼에서 /login으로 POST 요청
- 성공 시 세션 쿠키가 자동 저장되어 인증 유지
- 별도 토큰 저장 불필요

## 7. itsdangerous란?
- 세션 쿠키의 변조 방지(서명)를 위해 SessionMiddleware 내부에서 사용하는 라이브러리
- 클라이언트가 쿠키 값을 임의로 바꿔도 서버에서 위조 여부를 검증할 수 있게 해줌
- Flask, FastAPI 등에서 세션/토큰 보안에 널리 사용

---

## 참고
- 세션 기반 인증은 서버가 세션 상태를 관리하며, 보안상 HttpOnly 쿠키 사용이 권장됨
- JWT 방식으로 발전시키고 싶다면, 세션 대신 JWT 발급/검증 로직을 추가하면 됨