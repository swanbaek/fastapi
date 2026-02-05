
from fastapi import APIRouter, HTTPException, status
from typing import Optional
from datetime import datetime
import pymysql
import os
from dotenv import load_dotenv

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

@router.get("/users")
def get_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users")
            users = cursor.fetchall()
        return users
    finally:
        conn.close()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        conn.close()

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: dict):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (name, email, password, created_at) VALUES (%s, %s, %s, %s)"
            now = datetime.utcnow()
            cursor.execute(sql, (user['name'], user['email'], user['password'], now))
            conn.commit()
            user_id = cursor.lastrowid
        return {"id": user_id, **user, "created_at": now}
    finally:
        conn.close()

@router.put("/users/{user_id}")
def update_user(user_id: int, user: dict):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s"
            cursor.execute(sql, (user['name'], user['email'], user['password'], user_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"id": user_id, **user}
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
    finally:
        conn.close()
