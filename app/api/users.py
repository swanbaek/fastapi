
# 개선: Pydantic, bcrypt, 예외처리, 중복체크
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
import pymysql
import os
from dotenv import load_dotenv
from app.schemas.user import UserCreate, UserUpdate, UserOut
import bcrypt

load_dotenv()

router = APIRouter()

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'scott'),
        password=os.getenv('MYSQL_PASSWORD', 'tiger'),
        db=os.getenv('MYSQL_DB', 'eduDB'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
#utf8mb4 ==> 이모지 같은 문자와 확장된 유니코드 문자도 저장가능
# most bytes 4 (즉 4바이트 지원)

@router.get("/users", response_model=List[UserOut])
def get_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users")
            users = cursor.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 이메일 중복 체크
            cursor.execute("SELECT id FROM users WHERE email=%s", (user.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
            # 비밀번호 해싱
            hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            now = datetime.utcnow()
            sql = "INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user.name, user.email, hashed_pw.decode('utf-8'), now))
            conn.commit()
            user_id = cursor.lastrowid
        return {"id": user_id, "name": user.name, "email": user.email, "created_at": now}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 이메일 중복 체크 (본인 제외)
            cursor.execute("SELECT id FROM users WHERE email=%s AND id!=%s", (user.email, user_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
            hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            sql = "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s"
            cursor.execute(sql, (user.name, user.email, hashed_pw.decode('utf-8'), user_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"id": user_id, "name": user.name, "email": user.email, "created_at": datetime.utcnow()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE id=%s"
            cursor.execute(sql, (user_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail="DB Error: " + str(e))
    finally:
        conn.close()
