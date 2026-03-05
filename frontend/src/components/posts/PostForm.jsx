//PostForm.jsx
import { Form, Button } from 'react-bootstrap';
import { usePostFormStore } from '../../stores/postFormStore';
import { usePostStore } from '../../stores/postStore';
import { apiCreatePost, apiCreatePostFileUp } from '../../api/postApi';
import { useEffect, useRef } from 'react';
import { useAuthStore } from '../../stores/authStore';

export default function PostForm() {
    const { formData, setFormData, resetFormData } = usePostFormStore();
    const fetchPostList = usePostStore((s) => s.fetchPostList);
    const authUser = useAuthStore((s) => s.authUser);

    const titleRef = useRef();

    const handleChange = (e) => {
        console.log('>>>', e.target.value);

        const { name, value } = e.target;
        setFormData({ [name]: value });
    };
    const handleFileChange = (e) => {
        //  첨부파일
        console.log(e.target.files); //FileList{0:File, length:1}
        if (e.target.files && e.target.files.length > 0) {
            setFormData({ file: e.target.files[0] }); //File객체로 할당
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (!authUser) {
                alert('로그인해야 이용 가능합니다');
                return;
            }

            // const result = await apiCreatePost(formData); //파일업로드 하지 않는 경우
            //---------------------
            //파일업로드 하는 경우==> FormData객체에 데이터를 담아서 전송해야 한다
            const data = new FormData();
            //data.append('name', formData.name);
            data.append('title', formData.title);
            data.append('content', formData.content);
            if (formData.file) {
                data.append('file', formData.file);
                console.log('formData.file: ', formData.file);
            }
            // for (let i = 0; i < 10; i++) {
            const result = await apiCreatePostFileUp(data);
            // }
            //alert(JSON.stringify(result));
            //전체 글목록 새로고침
            resetFormData();
            titleRef.current?.focus();

            await fetchPostList();
        } catch (error) {
            console.error(error);
            alert('서버 요청 중 에러 발생: ' + error.message);
        }
    };

    return (
        <>
            <Form onSubmit={handleSubmit}>
                <Form.Group controlId="name">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        type="text"
                        name="name"
                        onChange={handleChange}
                        value={authUser?.name ?? ''}
                        placeholder={authUser?.name ?? '로그인해야 이용 가능해요'}
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
                    <Form.Control as="textarea" name="content" onChange={handleChange} value={formData.content} />
                </Form.Group>
                <Form.Group controlId="file">
                    <Form.Label>File</Form.Label>
                    <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button variant="primary" type="submit" className="my-2">
                    글쓰기
                </Button>
            </Form>
        </>
    );
}
