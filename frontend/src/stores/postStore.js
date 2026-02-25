// postStore.js
// 서버 통신 로직 중심 스토어
import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { apiFetchPostList, apiDeletePost, apiFetchPostById, apiUpdatePost } from '../api/postApi';

export const usePostStore = create(
    devtools((set, get) => ({
        postList: [], //글목록
        totalCount: 0, //총 게시글 수
        totalPages: 0, //총 페이지 수
        page: 1, //현재 페이지 번호
        size: 3, //한 페이지 당 목록 개수
        query: '', //검색어
        post: null, //특정 게시글
        postErr: null, //특정 게시글을 가져오지 못할 경우

        setPage: (page) => set({ page: page }),
        setQuery: (q) => set({ query: q }),
        setSize: (size) => set({ size: size }),
        //글목록 가져오기
        resetPostErr: () => set({ postErr: null }), //에러 메시지 초기화
        fetchPostList: async () => {
            //api호출=> 데이터 받아오면 ==> set()
            const { page, size, query } = get();

            try {
                const data = await apiFetchPostList(page, size, query);
                set({
                    // postList: data.data,
                    // totalCount: data.totalCount,
                    // totalPages: data.totalPages,
                    postList: data.posts,
                    totalCount: data.total,
                    totalPages: data.total_pages,
                });
            } catch (error) {
                alert('목록 가져오기 실패: ' + error.message);
            }
        },
        //글 삭제 하기
        deletePost: async (id) => {
            try {
                await apiDeletePost(id);
                set({ post: null });
                return true;
            } catch (error) {
                alert('글 삭제 실패: ' + error.message);
                return false;
            }
        },
        //글번호로 글 가져오기
        fetchPostById: async (id) => {
            // apiFetchPostById(id)==> set( {post: response.data} )
            try {
                const postData = await apiFetchPostById(id);
                set({ post: postData, postErr: null });
            } catch (error) {
                console.error(error);
                //alert('글 내용보기 실패: 해당 글은 없습니다');
                set({ post: null, postErr: '글 내용 보기 실패: ' + error.response.data.message });
            }
        },
        //글 수정 처리
        updatePost: async (id, formData) => {
            try {
                await apiUpdatePost(id, formData);
                return true;
            } catch (error) {
                console.error(error);
                //alert('수정 실패: ' + error.message);
                return false;
            }
        },
    }))
);
 