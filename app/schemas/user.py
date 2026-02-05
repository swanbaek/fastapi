from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):    
    name: str
    email: EmailStr
    # EmailStr 사용해서 이메일 자동 검증
    #  UserBase에 공통 필드만 정의

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    # 유저 정보 수정시엔 선택적 업데이트를 하도록 Optional로 줌

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
        #Pydantic 모델이 파이썬 객체(특히 ORM 객체)의 속성(attribute)에서 값을 읽을 수 있게 허용하는 옵션
        # dict가 아니라 클래스 객체를 넣어도 자동으로 모델로 변환해주는 기능
        # Pydantic은 기본적으로 “딕셔너리만 이해”하기 때문에,
        # 클래스 객체는 처리 못 함.
