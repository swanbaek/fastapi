from fastapi import APIRouter, Depends, HTTPException, status, Request
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

# 의존성 함수
def get_current_user(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인 필요")
    return user_id

#Depends()를 사용하면, FastAPI가 해당 파라미터에 필요한 값을 자동으로 주입해줌.
#/users/me 요청이 들어오면 /users/{user_id} 경로가 먼저 매칭됨."me"를 user_id로 해석하려다 타입 에러 발생
#더 구체적인 경로를 먼저 선언하자
@router.get("/users/me", response_model=UserOut)
def get_me(user_id: int = Depends(get_current_user)):
    """현재 로그인한 사용자 정보 반환"""
    
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인 필요")
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


# PATCH와 PUT을 통합 (실제 로직은 동일하므로)
@router.put("/users/me", response_model=UserOut)
@router.patch("/users/me", response_model=UserOut)
def update_my_info(
    user: UserUpdate,
    user_id: int = Depends(get_current_user)
):
    """
    내 정보 수정
    - 세션에서 자동으로 user_id 추출
    - 비밀번호는 선택적
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 현재 정보 조회
            cursor.execute(
                "SELECT id, name, email, created_at FROM users WHERE id=%s",
                (user_id,)
            )
            current_user = cursor.fetchone()
            if not current_user:
                raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
            
            # 업데이트할 필드가 하나도 없으면 에러
            if not any([user.name, user.email, user.password]):
                raise HTTPException(
                    status_code=400,
                    detail="최소 하나의 필드는 업데이트해야 합니다."
                )
            
            # 업데이트할 값 준비
            new_name = user.name if user.name is not None else current_user['name']
            new_email = user.email if user.email is not None else current_user['email']
            
            # 이메일 변경 시 중복 체크
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
            update_fields = ["name=%s", "email=%s"]
            update_values = [new_name, new_email]
            
            # 비밀번호가 제공된 경우에만 업데이트
            if user.password is not None:
                hashed_pw = bcrypt.hashpw(
                    user.password.encode('utf-8'),
                    bcrypt.gensalt()
                )
                update_fields.append("password=%s")
                update_values.append(hashed_pw.decode('utf-8'))
            
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

@router.put("/users/{user_id}", response_model=UserOut)
def update_user_by_id(user_id: int, user: UserUpdate):
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

from fastapi import Body

@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    password: str = Body(..., embed=True),
    user_id: int = Depends(get_current_user)
):
    """
    내 계정 삭제 (비밀번호 확인)
    - 세션에서 user_id 추출
    - 비밀번호 일치 시에만 삭제
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 1. 현재 비밀번호 해시 조회
            cursor.execute("SELECT password FROM users WHERE id=%s", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            # 2. 비밀번호 검증
            if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
            # 3. 삭제
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
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