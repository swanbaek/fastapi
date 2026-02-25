import { useAuthStore } from '../../stores/authStore'; // authStore 가져오기
//App에서 requestAuthUser()로 인증사용자 요청을 이미 해서 authUser에 넣어주었으므로 MyPage에서는 authUser만 해도됨
export default function MyPage() {
    const authUser = useAuthStore((s) => s.authUser);
    return (
        <div className="container py-4">
            <h1 className="my-4">MyPage</h1>

            {authUser ? (
                <div className="alert alert-primary p-3">
                    <h3>회원번호: {authUser.id} </h3>
                    <h3>이 름 : {authUser.name} </h3>
                    <h3>이 메 일 : {authUser.email} </h3>
                    <h3>ROLE : {authUser.role} </h3>
                </div>
            ) : (
                <div className="alert alert-danger p-3">
                    <h3>로그인한 사용자만 확인할 수 있어요</h3>
                </div>
            )}
        </div>
    );
}
