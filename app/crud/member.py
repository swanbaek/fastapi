from sqlalchemy.orm import Session
from app.models.member import Member

def get_all_members(db: Session):
    return db.query(Member).all()

def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

def get_member_by_email(db: Session, email: str):
    return db.query(Member).filter(Member.email == email).first()

def create_member(db: Session, name, email, hashed_pw, created_at, role=None):
    member = Member(
        name=name,
        email=email,
        password=hashed_pw,
        created_at=created_at,
        role=role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member.id

def update_member(db: Session, member_id: int, name: str, email: str, password: str | None, role: str | None = None):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        return None
    member.name = name
    member.email = email
    if password:
        member.password = password
    if role is not None:
        member.role = role
    db.commit()
    db.refresh(member)
    return member

def delete_member(db: Session, member_id: int):
    member = db.query(Member).filter(Member.id == member_id).first()
    if member:
        db.delete(member)
        db.commit()
