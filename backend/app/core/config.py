# 환경설정 및 환경변수 관리
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

def get_db_url():
	return os.getenv("DB_URL")

class Settings(BaseSettings):
    ACCESS_SECRET: str
    REFRESH_SECRET: str
    ACCESS_EXPIRE_MINUTES: int = 15
    REFRESH_EXPIRE_HOURS: int = 1

    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings()