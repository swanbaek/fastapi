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
    FOREIGN KEY (user_id) REFERENCES members(id) on delete cascade
);
-- 게시글 테이블에 파일 관련 컬럼 추가
-- file_url: 실제 파일 접근 경로(/static/uploads/...)
-- file_name: 원본 파일명
-- ALTER TABLE posts
-- ADD COLUMN file_url VARCHAR(300) DEFAULT NULL,
-- ADD COLUMN file_name VARCHAR(200) DEFAULT NULL;


INSERT INTO posts (title, content, user_id, hit_count, file_url, file_name)
VALUES
('Spring Boot 게시판 만들기', 'Spring Boot로 게시판 기능을 구현하는 예제입니다.', 3, 12, NULL, NULL),
('React 연동 테스트', 'React와 백엔드 API 연동을 위한 샘플 글입니다.', 4, 3, '/uploads/react1.png', 'react1.png'),
('FastAPI 검색 기능 구현', 'FastAPI에서 검색 기능을 구현하는 방법을 설명합니다.', 5, 7, NULL, NULL),
('Java 기초 정리', 'Java 문법과 기초 내용을 정리한 글입니다.', 5, 1, NULL, NULL),
('Next.js 이미지 처리', 'Next.js에서 이미지 최적화를 테스트한 글입니다.', 3, 4, '/uploads/nextimg.jpg', 'nextimg.jpg'),
('MySQL 페이징 테스트용 데이터', 'MySQL LIMIT과 OFFSET을 확인하는 더미 데이터입니다.', 4, 8, NULL, NULL),
('검색 테스트 - Spring', '검색 테스트용 Spring 키워드 포함 데이터입니다.', 3, 2, NULL, NULL),
('검색 테스트 - React', '검색 테스트용 React 키워드 포함 데이터입니다.', 4, 5, NULL, NULL),
('검색 테스트 - FastAPI', '검색 테스트용 FastAPI 키워드 포함 데이터입니다.', 3, 9, NULL, NULL),
('파일 업로드 기능 테스트', '파일 업로드와 다운로드 기능 테스트', 4, 11, '/files/test1.pdf', 'test1.pdf'),
('회원 관리 기능 구현', '회원 가입, 로그인, 로그아웃 기능 구현 테스트', 5, 0, NULL, NULL),
('JPA 연관 관계 매핑', 'JPA @OneToMany, @ManyToOne 매핑 테스트', 4, 6, NULL, NULL),
('JWT 로그인 구현', 'JWT 기반 로그인 처리 구현 내용 정리', 3, 14, NULL, NULL),
('AI 면접 질문 생성', 'AI 기반 면접 질문 생성 기능 테스트', 4, 7, NULL, NULL),
('딥러닝 기초 수업 자료', '딥러닝 기초 개념을 정리한 게시글입니다.', 3, 2, '/uploads/deep.png', 'deep.png'),
('Node.js MySQL 연동', 'Node.js와 MySQL 연동 예제 코드 포함', 5, 12, NULL, NULL),
('검색어 하이라이트 기능', '검색어 하이라이트 기능 구현 과정 테스트', 3, 5, NULL, NULL),
('프론트엔드 배포 자동화', 'GitHub Actions를 활용한 자동 배포 테스트', 4, 3, NULL, NULL),
('이미지 슬라이더 구현', '홈 화면 이미지 슬라이더 구현 테스트', 4, 8, '/uploads/slider.png', 'slider.png'),
('게시판 페이징 테스트', '페이징이 제대로 동작하는지 확인하는 게시글입니다.', 5, 10, NULL, NULL);