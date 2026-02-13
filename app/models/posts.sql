use eduDB;
drop table if exists posts;
CREATE TABLE if not exists posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT NULL,
    hit_count int default 0, 
    file_url VARCHAR(300) DEFAULT NULL,
    file_name VARCHAR(200) DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
-- 게시글 테이블에 파일 관련 컬럼 추가
-- file_url: 실제 파일 접근 경로(/static/uploads/...)
-- file_name: 원본 파일명
-- ALTER TABLE posts
-- ADD COLUMN file_url VARCHAR(300) DEFAULT NULL,
-- ADD COLUMN file_name VARCHAR(200) DEFAULT NULL;


