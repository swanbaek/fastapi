from app.core.db import get_connection

def get_all_users():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM users")
            return cursor.fetchall()
    finally:
        conn.close()


def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, created_at, password FROM users WHERE id=%s",
                (user_id,)
            )
            return cursor.fetchone()
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_user(name, email, hashed_pw, created_at):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO users (name, email, password, created_at)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, hashed_pw, created_at))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_user(user_id: int, name: str, email: str, password: str | None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            fields = ["name=%s", "email=%s"]
            values = [name, email]

            if password:
                fields.append("password=%s")
                values.append(password)

            values.append(user_id)

            sql = f"UPDATE users SET {', '.join(fields)} WHERE id=%s"
            cursor.execute(sql, values)
            conn.commit()
    finally:
        conn.close()


def delete_user(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
            conn.commit()
    finally:
        conn.close()
