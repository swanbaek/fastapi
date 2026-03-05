// PostView.jsx
//useParams, useSearchParams
import { useParams, useNavigate, Link } from 'react-router-dom';
import { usePostStore } from '../../stores/postStore';
import { useAuthStore } from '../../stores/authStore';
import { useEffect } from 'react';

export default function PostView() {
    const { id } = useParams(); //type: string
    const navigate = useNavigate();

    const authUser = useAuthStore((s) => s.authUser);

    const deletePost = usePostStore((s) => s.deletePost);

    //useEffect 훅에서 글번호로 게시글 가져오는 함수 호출 (usePostStore)
    const post = usePostStore((s) => s.post);
    const fetchPostById = usePostStore((s) => s.fetchPostById);
    const postErr = usePostStore((s) => s.postErr);
    const resetPostErr = usePostStore((s) => s.resetPostErr);

    useEffect(() => {
        if (id) fetchPostById(id);
    }, [id]);

    useEffect(() => {
        if (postErr) {
            alert(postErr);
            resetPostErr();
            navigate('/posts');
        }
    }, [postErr]);

    // if (postErr) {
    //     alert(postErr);
    //     navigate('/posts');
    //     return <></>;
    // }

    const handleDelete = async (pid, e) => {
        //alert(pid + '/' + e);
        if (authUser?.email !== post.author?.email) {
            e.preventDefault();
            alert('작성자만 삭제 가능합니다');
            return;
        }
        const yn = confirm(`${pid}번 글을 정말 삭제할까요?`);
        if (!yn) return;
        //
        const result = await deletePost(pid);
        if (result) {
            alert('글이 삭제되었습니다');
            navigate('/posts');
        } else {
            alert('글 삭제 실패');
        }
        // await fetchPostList();
    };
    const go = (e) => {
        if (authUser?.email !== post.author?.email) {
            //이름은 중복될 수 있으니 email로 비교하는 게 더 안전
            e.preventDefault();
            alert('작성자만 수정 가능합니다');
        }
    };

    if (!post)
        return (
            <div className="text-center">
                <h3>Loading ....</h3>
            </div>
        );

    return (
        <div className="post-view">
            <div className="row my-3">
                <div className="col-md-10 offset-md-1 px-3">
                    <h1 className="my-5 text-center">Post View [No. {id}] </h1>

                    {/* 이렇게 변경 */}
                    {authUser?.email === post.author?.email && (
                        <div className="text-end my-2">
                            <Link to={`/postEdit/${id}`}>
                                <button className="btn btn-info mx-2">수정</button>
                            </Link>
                            <button className="btn btn-danger" onClick={(e) => handleDelete(id, e)}>
                                삭제
                            </button>
                        </div>
                    )}

                    <div className="card">
                        <div className="card-body">
                            <h5>
                                [{post.id}] {post.title}{' '}
                            </h5>
                            <hr />
                            <div style={{ marginBottom: '1rem' }} className="text-center">
                                <img
                                    src={`https://myswan.shop${post.file_url ?? '/static/uploads/noimage.png'}`}
                                    alt={`${post.file_url ?? 'noimage'}`}
                                    style={{ maxWidth: '70%', borderRadius: '0.5rem' }}
                                />
                            </div>
                            <div className="cArea px-5">
                                {post.content}
                                <br />
                                <span>♡</span> <span>👎</span>
                            </div>
                        </div>
                        <div className="card-footer">
                            Created on [{post.created_at}] by {post.author.name}
                        </div>
                    </div>
                </div>
            </div>

            <div className="row my-5">
                <div className="col px-5 text-center">
                    <button className="btn mt-4 btn-secondary" onClick={() => navigate('/posts')}>
                        Post List 전체 출력
                    </button>
                    <h3 className="mt-5">댓글영역</h3>
                </div>
            </div>

            <div className="row my-5">
                <div className="col px-5">
                    <h3 className="mt-4">댓글추가</h3>
                </div>
            </div>

            <div className="row my-5">
                <div className="col px-5">댓글 수정 폼</div>
            </div>
        </div>
    );
}
