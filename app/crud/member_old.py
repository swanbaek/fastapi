from app.core.db import get_connection

def get_all_members():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, email, created_at FROM members")
            return cursor.fetchall()
    finally:
        conn.close()


def get_member_by_id(member_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, created_at, password FROM members WHERE id=%s",
                (member_id,)
            )
            return cursor.fetchone()
    finally:
        conn.close()


def get_member_by_email(email: str):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM members WHERE email=%s", (email,))
            return cursor.fetchone()
    finally:
        conn.close()


def create_member(name, email, hashed_pw, created_at):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO members (name, email, password, created_at)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (name, email, hashed_pw, created_at))
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()


def update_member(member_id: int, name: str, email: str, password: str | None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            fields = ["name=%s", "email=%s"]
            values = [name, email]

            if password:
                fields.append("password=%s")
                values.append(password)

            values.append(member_id)

            sql = f"UPDATE members SET {', '.join(fields)} WHERE id=%s"
            cursor.execute(sql, values)
            conn.commit()
    finally:
        conn.close()


def delete_member(member_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
            conn.commit()
    finally:
        conn.close()
