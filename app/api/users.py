from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas.user import UserCreate, UserUpdate, UserOut
import bcrypt
from app.core.db import get_connection

router = APIRouter()


@router.get("/users", response_model=List[UserOut])
def get_users():
    """모든 사용자 목록 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users")
            users = cursor.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """특정 사용자 조회"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id=%s",
                (user_id,)
            )
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """새 사용자 생성"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 이메일 중복 체크
            cursor.execute("SELECT id FROM users WHERE email=%s", (user.email,))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="이미 등록된 이메일입니다."
                )
            
            # 비밀번호 해싱
            hashed_pw = bcrypt.hashpw(
                user.password.encode('utf-8'),
                bcrypt.gensalt()
            )
            
            # 사용자 생성
            now = datetime.now()
            sql = """
                INSERT INTO users (name, email, password, created_at)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                sql,
                (user.name, user.email, hashed_pw.decode('utf-8'), now)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
        return {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "created_at": now
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()


@router.patch("/users/{user_id}", response_model=UserOut)
def partial_update_user(user_id: int, user: UserUpdate):
    """
    사용자 정보 부분 수정 (PATCH)
    - PUT과 동일한 로직이지만 의미상 부분 업데이트를 명확히 함
    """
    return update_user(user_id, user)


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    """사용자 정보 수정 - 비밀번호는 선택적"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 사용자 존재 여부 및 현재 정보 조회
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id=%s",
                (user_id,)
            )
            current_user = cursor.fetchone()
            if not current_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # 업데이트할 필드가 하나도 없으면 에러
            if not any([user.name, user.email, user.password]):
                raise HTTPException(
                    status_code=400,
                    detail="최소 하나의 필드는 업데이트해야 합니다."
                )
            
            # 업데이트할 값 준비 (제공된 값만 사용, 없으면 기존 값 유지)
            new_name = user.name if user.name is not None else current_user['name']
            new_email = user.email if user.email is not None else current_user['email']
            
            # 이메일이 변경되는 경우, 다른 사용자가 사용 중인지 체크
            if new_email != current_user['email']:
                cursor.execute(
                    "SELECT id FROM users WHERE email=%s AND id!=%s",
                    (new_email, user_id)
                )
                if cursor.fetchone():
                    raise HTTPException(
                        status_code=400,
                        detail="이미 등록된 이메일입니다."
                    )
            
            # SQL 쿼리 동적 생성
            update_fields = []
            update_values = []
            
            update_fields.append("name=%s")
            update_values.append(new_name)
            
            update_fields.append("email=%s")
            update_values.append(new_email)
            
            # 비밀번호가 제공된 경우에만 업데이트
            if user.password is not None:
                hashed_pw = bcrypt.hashpw(
                    user.password.encode('utf-8'),
                    bcrypt.gensalt()
                )
                update_fields.append("password=%s")
                update_values.append(hashed_pw.decode('utf-8'))
            
            # WHERE 조건을 위한 user_id 추가
            update_values.append(user_id)
            
            # 업데이트 실행
            sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id=%s"
            cursor.execute(sql, tuple(update_values))
            conn.commit()
            
        return {
            "id": user_id,
            "name": new_name,
            "email": new_email,
            "created_at": current_user['created_at']
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()


@router.put("/users/old/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    """사용자 정보 필드를 모두 수정"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 다른 사용자가 사용 중인 이메일인지 체크
            cursor.execute(
                "SELECT id FROM users WHERE email=%s AND id!=%s",
                (user.email, user_id)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="이미 등록된 이메일입니다."
                )
            
            # 기존 created_at 조회
            cursor.execute(
                "SELECT created_at FROM users WHERE id=%s",
                (user_id,)
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            
            created_at = result['created_at']
            
            # 비밀번호 해싱
            hashed_pw = bcrypt.hashpw(
                user.password.encode('utf-8'),
                bcrypt.gensalt()
            )
            
            # 사용자 정보 업데이트
            sql = """
                UPDATE users
                SET name=%s, email=%s, password=%s
                WHERE id=%s
            """
            cursor.execute(
                sql,
                (user.name, user.email, hashed_pw.decode('utf-8'), user_id)
            )
            conn.commit()
            
        return {
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "created_at": created_at  # 원래 생성일 유지
        }
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """사용자 삭제"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE id=%s"
            cursor.execute(sql, (user_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    finally:
        conn.close()