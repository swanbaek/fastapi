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
#utf8mb4 ==> 이모지 같은 문자와 확장된 유니코드 문자도 저장가능
# most bytes 4 (즉 4바이트 지원)
