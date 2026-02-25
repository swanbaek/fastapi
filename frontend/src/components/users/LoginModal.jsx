//LoginModal.jsx
import { Modal, Button, Row, Col, Form } from 'react-bootstrap';
import { useState, useRef, useEffect } from 'react';
import { apiSignIn } from '../../api/userApi';
import { useAuthStore } from '../../stores/authStore';
export default function LoginModal({ show, setShowLogin }) {
    const [loginUser, setLoginUser] = useState({ email: '', passwd: '' });
    const loginAuthUser = useAuthStore((s) => s.loginAuthUser);

    const emailRef = useRef(null);
    const passwdRef = useRef(null);
    useEffect(() => {
        if (show) emailRef.current?.focus();
    }, [show]);

    const handleChange = (e) => {
        setLoginUser({ ...loginUser, [e.target.name]: e.target.value });
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        const { email, passwd } = loginUser;
        if (!email.trim()) {
            alert('아이디를 입력하세요');
            emailRef.current?.focus();
            return;
        }
        if (!passwd.trim()) {
            alert('비밀번호를 입력하세요');
            passwdRef.current?.focus();
            return;
        }

        requestLogin();
    };
    const requestLogin = async () => {
        try {
            const response = await apiSignIn(loginUser);
            //alert(JSON.stringify(response)); //{result:'success',message:'로그인 성공',data:{...}}
            const { result, message, data } = response;
            if (result === 'success') {
                //인증받은 사용자일 경우 서버가 보내온 accessToken과 refreshToken을 sessionStorage, localStorage에 저장
                const { accessToken, refreshToken } = data;
                sessionStorage.setItem('accessToken', accessToken);
                localStorage.setItem('refreshToken', refreshToken);
                //회원정보(payload), 토큰...=>data를 store 전달. 인증받은 사용자 정보 => 전역 state로 관리하자
                loginAuthUser({ ...data });
            } else {
                alert(message);
            }
            resetForm();
            setShowLogin(false); //모달 창 닫기
        } catch (error) {
            console.error(error);
            alert(error.response?.data?.message ?? error.message);
            resetForm();
        }
    };

    const resetForm = () => {
        setLoginUser({ email: '', passwd: '' });
        emailRef.current?.focus();
    };

    return (
        <>
            <Modal show={show} onHide={() => setShowLogin(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Login</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Row>
                        <Col className="p-4 mx-auto" xs={10} sm={10} md={8}>
                            <Form onSubmit={handleSubmit}>
                                <Form.Group className="mb-3">
                                    <Form.Label>ID (email)</Form.Label>
                                    <Form.Control
                                        type="text"
                                        name="email"
                                        ref={emailRef}
                                        onChange={handleChange}
                                        value={loginUser.email}
                                        placeholder="ID (email)"
                                    />
                                </Form.Group>

                                <Form.Group className="mb-3">
                                    <Form.Label>Password</Form.Label>
                                    <Form.Control
                                        type="password"
                                        name="passwd"
                                        ref={passwdRef}
                                        onChange={handleChange}
                                        value={loginUser.passwd}
                                        placeholder="Password"
                                    />
                                </Form.Group>
                                <div className="d-grid">
                                    <Button type="submit" variant="info">
                                        Login
                                    </Button>
                                </div>
                            </Form>
                        </Col>
                    </Row>
                </Modal.Body>
            </Modal>
        </>
    );
}
