// PostList.jsx
import { usePostStore } from '../../stores/postStore';
import { useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function PostList() {
    const postList = usePostStore((s) => s.postList);
    const totalCount = usePostStore((s) => s.totalCount);
    const fetchPostList = usePostStore((s) => s.fetchPostList);
    const totalPages = usePostStore((s) => s.totalPages);
    const setPage = usePostStore((s) => s.setPage);
    const page = usePostStore((s) => s.page);
    useEffect(() => {
        fetchPostList();
    }, [page]);

    // 페이지 계산
    const blockSize = 5;
    const startPage = Math.floor((page - 1) / blockSize) * blockSize + 1;
    const endPage = Math.min(startPage + (blockSize - 1), totalPages);

    /**
     * [1][2][3][4][5] >|< [6][7][8][9][10] >|<[11][12][13][14][15] >[16][17][18]
     *
     * page         blockSize       startPage       endPage
     * 1 ~5             5           1               5
     * 6~ 10            5           6               10
     * 11 ~15           5           11              15
     *
     * startPage = Math.floor((page-1)/blockSize) * blockSize +1
     */

    return (
        <div className="post-list">
            <h3 className="my-3">
                {' '}
                총 게시글 수: {totalCount} 개 {'     '} {page} page / {totalPages} pages
            </h3>

            {(postList && postList.length === 0) && <div>데이터가 없습니다</div>}
            {postList && postList.length > 0 &&
                postList.map((post, index) => (
                    <div
                        className="my-3"
                        key={post.id ?? index}
                        style={{ backgroundColor: '#efefef', borderRadius: '10px', display: 'flex' }}
                    >
                        <div style={{ width: '30%' }} className="text-center">
                            {post.file_url ? (
                                <img
                                src={`https://myswan.shop${post.file_url}`}
                                alt={post.file_name}
                                style={{ width: '90%' }}
                                className="img-thumbnail"
                            />
                            ) : (
                                <img
                                    src={`https://myswan.shop/static/uploads/noimage.png`}
                                    alt={post.file ?? 'noimage'}
                                    style={{ width: '90%' }}
                                    className="img-thumbnail"
                                />
                            )}
                        </div>
                        <div style={{ width: '70%' }} className="p-3">
                            <h5>
                                {post.author.name} {'   '}
                                <small>
                                    <i className="text-muted">Posted on {post.created_at.split('T')[0]} {post.created_at.split('T')[1]}</i>
                                </small>
                            </h5>
                            <Link to={`/posts/${post.id}`} style={{ textDecoration: 'none' }}>
                                <h3>{post.title}</h3>
                            </Link>

                            {/* <p>{post.content}</p> */}
                            {/* <div className="d-flex justify-content-center">
                                <button className="btn btn-outline-info mx-1">Edit</button>
                                <button className="btn btn-outline-danger" onClick={() => handleDelete(post.id)}>
                                    Delete
                                </button>
                            </div> */}
                        </div>
                    </div>
                ))}
            {/* 페이지네이션 */}
            <div className="text-center">
                {startPage > 1 && (
                    <button className="btn btn-outline-primary" onClick={() => setPage(startPage - 1)}>
                        Prev
                    </button>
                )}
                {Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i).map((n) => (
                    <button
                        className={`mx-1 btn ${n === page ? 'btn-primary' : 'btn-outline-primary'}`}
                        onClick={() => setPage(n)}
                    >
                        {n}
                    </button>
                ))}
                {endPage < totalPages && (
                    <button className="btn btn-outline-primary" onClick={() => setPage(endPage + 1)}>
                        Next
                    </button>
                )}
            </div>
        </div>
    );
}
