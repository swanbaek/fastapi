import { Form, Row, Col, Button } from 'react-bootstrap';
import { useState, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function SignUp() {
    const [formData, setFormData] = useState({ name: '', email: '', passwd: '', role: 'USER' });
    const nameRef = useRef(null);
    const emailRef = useRef(null);
    const pwRef = useRef(null);
    const roleRef = useRef(null);

    const navigate = useNavigate();

    const handleChange = (e) => {
        console.log('e.target.name: ', e.target.name); //"name", email, password ==>string
        //e.target.name을 속성으로 사용하려면 [e.target.name]
        //obj.name === obj['name'] [o]
        //  obj."name"[x]
        console.log('e.target.value: ', e.target.value);
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    //입력값 유효성 체크를 하는 함수
    const check = () => {
        const { name, email, passwd, role } = formData;
        // 유효성 체크. 입력 포커스 주기
        if (!name.trim()) {
            alert('이름을 입력하세요');
            nameRef.current?.focus();
            return false;
        }
        if (!email.trim()) {
            //정규식 이용해서 이메일 형식 맞는지 체크
            alert('이메일 입력하세요');
            emailRef.current?.focus();
            return false;
        }
        if (!passwd.trim()) {
            //정규식 이용해서 이메일 형식 맞는지 체크
            alert('비밀번호 입력하세요');
            pwRef.current?.focus();
            return false;
        }
        if (!role.trim()) {
            //정규식 이용해서 이메일 형식 맞는지 체크
            alert('역할을 선택하세요');
            roleRef.current?.focus();
            return false;
        }
        return true;
    };

    const handleSubmit = async (e) => {
        //submit하려는 기본동작을 막자. 왜? 비동기요청을 위해서
        e.preventDefault();
        const b = check();
        if (!b) return;
        //alert('ajax요청');
        try {
            //post방식으로 요청. 회원데이터를 body포함시켜야함, headers에 'Content-Type'을 'application/json'으로 설정
            const url = `/api/users`; // 프록시를 통한 백엔드 서버
            //vite.config.js에서 proxy 설정으로 cors 문제 해결
            //vite proxy 설정으로 cors 문제 해결
            const response = await axios.post(url, formData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            //alert(JSON.stringify(response));
            if (response.status === 200) {
                alert('회원가입을 완료했습니다. 로그인 페이지로 이동합니다');
                navigate('/');
            }
        } catch (error) {
            alert('서버 오류: ' + error.message);
        }
    };
    const handleReset = () => {
        setFormData({ name: '', email: '', passwd: '', role: 'USER' });
    };

    const { name, email, passwd, role } = formData;

    return (
        <div className="container py-4">
            <h1 className="text-center my-4">Signup</h1>
            <Form method="post" onSubmit={handleSubmit}>
                <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm={2}>
                        이름
                    </Form.Label>
                    <Col sm={8}>
                        <Form.Control
                            type="text"
                            name="name"
                            value={name}
                            ref={nameRef}
                            placeholder="Name"
                            onChange={handleChange}
                        />
                    </Col>
                </Form.Group>
                {/* 이메일 */}
                <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm={2}>
                        이메일
                    </Form.Label>
                    <Col sm={8}>
                        <Form.Control
                            type="email"
                            name="email"
                            value={email}
                            ref={emailRef}
                            placeholder="Email"
                            onChange={handleChange}
                        />
                    </Col>
                    <Col sm={2}>
                        <Button type="button" variant="success">
                            중복체크
                        </Button>
                    </Col>
                    <div className="mt-2 small text-primary d-none">이메일 중복여부 체크 결과 메시지</div>
                </Form.Group>

                {/* 비밀번호 */}
                <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm={2}>
                        비밀번호
                    </Form.Label>
                    <Col sm={8}>
                        <Form.Control
                            type="password"
                            name="passwd"
                            value={passwd}
                            ref={pwRef}
                            placeholder="Password"
                            onChange={handleChange}
                        />
                    </Col>
                </Form.Group>

                {/* role : [일반유저: USER, 관리자: ADMIN] */}
                <Form.Group as={Row} className="mb-3">
                    <Form.Label column sm={2}>
                        역 할
                    </Form.Label>
                    <Col sm={8}>
                        <Form.Select name="role" value={role} ref={roleRef} onChange={handleChange}>
                            <option value="">:::역할 선택::</option>
                            <option value="USER">USER</option>
                            <option value="ADMIN">ADMIN</option>
                        </Form.Select>
                    </Col>
                </Form.Group>
                {/* 버튼 */}
                <Row>
                    <Col>
                        <Button variant="info" type="submit">
                            회원가입
                        </Button>

                        <Button variant="secondary" type="button" onClick={handleReset}>
                            다시쓰기
                        </Button>
                    </Col>
                </Row>
            </Form>
        </div>
    );
}
