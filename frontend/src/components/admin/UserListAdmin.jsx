// UserListAdmin.jsx
import { Table, Container, Button } from 'react-bootstrap';
import { useState, useEffect } from 'react';
// import axios from 'axios';
import axiosAuthInstance from '../../api/axiosAuthInstance';
import { useAuthStore } from '../../stores/authStore';
import { useNavigate } from 'react-router-dom';
const UserListAdmin = () => {
    const [users, setUsers] = useState([]);
    const authUser = useAuthStore((s) => s.authUser);
    const navigate = useNavigate();
    useEffect(() => {
        if (!authUser || authUser.role !== 'ADMIN') {
            alert('관리자로 로그인해야 이용 가능해요');
            navigate('/');
        } else {
            getAllUser();
        }
    }, [authUser]);

    const getAllUser = async () => {
        try {
            const url = `http://localhost:7777/api/admin/users`;
            const response = await axiosAuthInstance.get(url);
            //alert(JSON.stringify(response));
            setUsers(response.data);
        } catch (error) {
            console.error('error: ', error);
            //alert(error.message);
        }
    };

    const getBgClass = (role) => {
        if (role === 'ADMIN') return 'table-info';
        else return 'table-light';
    };

    if (!authUser || authUser.role !== 'ADMIN') {
        return (
            <div className="alert alert-danger">
                <h3>관리자 전용 페이지 입니다</h3>
            </div>
        );
    }

    return (
        <>
            <Container className="my-4">
                <h2 className="text-center my-4">전체 회원 목록 [Admin Page]</h2>

                <Table striped>
                    <thead>
                        <tr>
                            <th>번호</th>
                            <th>이름</th>
                            <th>이메일</th>
                            <th>가입일</th>
                            <th>ROLE</th>
                            <th>수정|삭제</th>
                        </tr>
                    </thead>
                    <tbody>
                        {!users ||
                            (users.length === 0 && (
                                <tr>
                                    <td colSpan={6}>데이터가 없습니다</td>
                                </tr>
                            ))}
                        {users &&
                            users.length > 0 &&
                            users.map((user) => (
                                <tr key={user.id} className={getBgClass(user.role)}>
                                    <td>{user.id}</td>
                                    <td>{user.name}</td>
                                    <td>{user.email}</td>
                                    <td>{user.createdAt}</td>
                                    <td>{user.role}</td>
                                    <td>
                                        <Button variant="info" className="mx-1">
                                            수정
                                        </Button>
                                        <Button variant="danger">삭제</Button>
                                    </td>
                                </tr>
                            ))}
                    </tbody>
                </Table>
            </Container>
        </>
    );
};
export default UserListAdmin;
