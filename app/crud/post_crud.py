
# SQLAlchemy 세션과 Post 모델 import
from sqlalchemy.orm import Session, joinedload
from app.models.post import Post

# 게시글 전체 목록 조회 (최신순)
def get_posts(db: Session):
    return db.query(Post).options(joinedload(Post.author)).order_by(Post.id.desc()).all()

# 게시글 목록 조회 (페이징 + 검색)
def get_posts_paging(db: Session, page: int = 1, size: int = 10, search: str = ""):
    query = db.query(Post).options(joinedload(Post.author))
    # join해야 작성자명이 출력됨
    if search:
        query = query.filter(Post.title.contains(search))
    total = query.count()
    offset = (page - 1) * size
    posts = query.order_by(Post.id.desc()).offset(offset).limit(size).all()
    return total, posts

# 게시글 단일 조회 (id로)
def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).options(joinedload(Post.author)).filter(Post.id == post_id).first()

# 게시글 생성
def create_post(db: Session, post: Post):
    db.add(post)  # 새 게시글 추가
    db.commit()   # DB에 반영
    db.refresh(post)  # 갱신된 post 객체 반환
    return post

# 게시글 수정
def update_post(db: Session, post: Post):
    db.commit()   # 변경사항 저장
    db.refresh(post)  # 갱신된 post 객체 반환
    return post

# 게시글 삭제
def delete_post(db: Session, post: Post):
    db.delete(post)  # 게시글 삭제
    db.commit()      # DB에 반영
