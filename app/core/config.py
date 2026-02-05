# 환경설정 및 환경변수 관리
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
	return os.getenv("DB_URL")
