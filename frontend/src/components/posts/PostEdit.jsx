// PostEdit.jsx
import { Row, Col, Form, Button } from 'react-bootstrap';
import { usePostFormStore } from '../../stores/postFormStore';
import { usePostStore } from '../../stores/postStore';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useRef } from 'react';
export default function PostEdit() {
    const { formData, setFormData, resetFormData } = usePostFormStore();

    const post = usePostStore((s) => s.post);
    const fetchPostById = usePostStore((s) => s.fetchPostById);
    const updatePost = usePostStore((s) => s.updatePost);

    const navigate = useNavigate();
    const { id } = useParams();

    const titleRef = useRef();

    useEffect(() => {
        const fetchAndSet = async () => {
            if (id) {
                await fetchPostById(id); //  글번호로 해당글 가져와서 post값에 setting
            }
        };
        fetchAndSet(); //함수 호출
        return () => {
            //정리함수
            resetFormData();
        };
    }, [id]);

    useEffect(() => {
        if (post) {
            //백엔드에서 받아온 포스트 글을 formData state값에 설정
            setFormData({
                ...post,
                name: post.author?.name ?? '', //post.author.name이 null 또는 undefined인 경우 빈 문자열로 대체
                file: post.file_url ?? '', //기존 첨부파일 경로. file_url을 file필드로 대체
                file_url: post.file_url ?? '',   // 미리보기용
            })
        }
    }, [post]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        //유효성 체크 (권장)
        if (!confirm('게시글을 수정할까요?')) return;

        try {
            const { name, title, content, newFile } = formData;

            //파일업로드 시에는 =>FormData객체에 담아서 보낸다. 파일업로드 안할 경우=> json데이터로
            const data = new FormData();
            data.append('name', name);
            data.append('title', title);
            data.append('content', content);
            if (newFile) {
                data.append('file', newFile);
            }

            const result = await updatePost(id, data);
            if (result) {
                alert('수정 성공');
            } else {
                alert('수정 실패- 서버 에러 또는 해당 글이 없습니다');
            }
            navigate('/posts');
        } catch (error) {
            console.error(error);
            alert('수정 실패1 : ' + error.message);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFileChange = (e) => {
        //e.target.files ==> FileList {0:File,1:File,2:File, length:3}
        if (e.target.files && e.target.files.length > 0) {
            setFormData({ ...formData, newFile: e.target.files[0] });
            //newFile에 새로 첨부한 File객체를 넣어준다
        }
    };

    return (
        <>
            <Row>
                <Col md={10} className="mx-auto p-3">
                    <h1 className="text-center my-5">Post 글 수정 [No. {id}]</h1>

                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="name">
                            <Form.Label>Name</Form.Label>
                            <Form.Control
                                type="text"
                                name="name"
                                onChange={handleChange}
                                value={formData.name}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="title">
                            <Form.Label>Title</Form.Label>
                            <Form.Control
                                type="text"
                                name="title"
                                ref={titleRef}
                                onChange={handleChange}
                                value={formData.title}
                                required
                            />
                        </Form.Group>
                        <Form.Group controlId="content">
                            <Form.Label>Content</Form.Label>
                            <Form.Control
                                as="textarea"
                                name="content"
                                onChange={handleChange}
                                value={formData.content}
                            />
                        </Form.Group>
                        <Form.Group controlId="file">
                            <Form.Label>File</Form.Label>
                            <Form.Control type="file" onChange={handleFileChange} />
                            
                            {/* 첨부된 이미지 파일 미리보기---------------------- */}
                            {formData.file_url && (
                                <div className="my-2 text-muted">
                                    <img
                                        src={`http://myswan.shop${formData.file_url}`}
                                        alt={formData.file}
                                        style={{ width: '150px' }}
                                        className="img-thumbnail"
                                    />
                                    <div>현재 첨부파일: {formData.file}</div>
                                </div>
                            )}
                        </Form.Group>
                        <Button variant="primary" type="submit" className="my-2">
                            글수정
                        </Button>
                        {/* <Button type="button" variant="success" className="mx-1">
                            다시쓰기
                        </Button> */}
                        <Button type="button" onClick={() => navigate('/posts')} variant="secondary" className="mx-1">
                            글 목록
                        </Button>
                    </Form>
                </Col>
            </Row>
        </>
    );
}
