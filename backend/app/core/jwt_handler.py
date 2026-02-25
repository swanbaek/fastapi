from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
# JWT 토큰 생성 및 검증 관련 함수 정의
#Node.js의 jwt.sign(user, secret, { expiresIn }) 과 100% 동일한 구조.
def create_access_token(data: dict):
    exp = datetime.utcnow() + timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": exp}, settings.ACCESS_SECRET, algorithm="HS256")

def create_refresh_token(data: dict):
    exp = datetime.utcnow() + timedelta(hours=settings.REFRESH_EXPIRE_HOURS)
    return jwt.encode({**data, "exp": exp}, settings.REFRESH_SECRET, algorithm="HS256")
