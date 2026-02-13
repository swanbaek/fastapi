import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'scott'),
        password=os.getenv('MYSQL_PASSWORD', 'tiger'),
        db=os.getenv('MYSQL_DB', 'eduDB'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("DB 연결 성공!", conn)
        conn.close()
    except Exception as e:
        print("DB 연결 실패:", e)
