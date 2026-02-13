from fastapi import APIRouter, HTTPException, Request, Response
from app.core.db import get_connection
import bcrypt

router = APIRouter()

@router.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        raise HTTPException(status_code=400, detail="이메일과 비밀번호를 입력하세요.")
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
            if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # bcrypt.checkpw(): 사용자가 입력한 password와 DB에 저장된 해시된 비밀번호 비교 
                raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
            request.session['user_id'] = user['id']
            # 세션에 로그인한 사용자 번호와 이름, 이메일 저장
            request.session['user_name'] = user['name']
            request.session['user_email'] = user['email']
            return {"id": user['id'], "name": user['name'], "email": user['email']}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()

@router.post("/logout")
def logout(request: Request):
    request.session.clear() # 세션 데이터 모두 삭제
    return {"msg": "로그아웃 완료"}
