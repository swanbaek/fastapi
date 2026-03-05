//postApi.js
import axios from 'axios';
let baseUrl = ``; 
import axiosInstance from './axiosInstance';
import axiosAuthInstance from './axiosAuthInstance';

//---post 글쓰기 (파일업로드 x)---------------
export const apiCreatePost = async (data) => {
    // 백엔드 /api/posts 로 post방식으로 요청 보내서 응답 받기
    const response = await axiosAuthInstance.post(`${baseUrl}/posts`, data, {
        headers: {
            'Content-Type': 'application/json', //파일업로드시 multipart/form-data로 전송해야 함
        },
    });
    return response.data;
};
//multipart/form-data는 axios가 자동으로 boundary 포함해서 넣어주므로
//지정할 필요없음. 그래서 아래처럼 간단히 작성해도 됨.
export const apiCreatePostFileUp = async (data) => {
    //인증받은 사용자만 글쓰기 가능하므로 axiosAuthInstance 사용
    return await axiosAuthInstance.post(`${baseUrl}/posts/`, data);
};
//--- post 목록 가져오기 ------------------------------
export const apiFetchPostList = async (page = 1, size = 3, query = undefined) => {
    console.log('page=====', page);
    //alert(page);
    const response = await axiosInstance.get(`/posts`, { params: { page, size, query } });
                                    // `/posts?page=${page}&size=${size}&query=${query}`
    //alert('목록 가져오기 성공: ' + JSON.stringify(response.data));                                    
    return response.data;
};
//---post 단건 가져오기 -----------------------------
export const apiFetchPostById = async (id) => {
    const response = await axiosInstance.get(`/posts/${id}`);
    // const data = response.data?.data;
    // if (data && data.length > 0) {
    //     return data[0];
    // }
    // return null;

    // API가 단건 객체를 바로 반환하므로 response.data 그대로 사용
    return response.data;
};
//---post 글 삭제하기 ----------------------------------
// 삭제는 인증이 필요하므로 axiosAuthInstance 사용
export const apiDeletePost = async (id) => {
    const response = await axiosAuthInstance.delete(`/posts/${id}`);
    return response.data;
};

//---post 글 수정하기 -----------------------------------
// 수정도 인증이 필요하므로 axiosAuthInstance 사용
export const apiUpdatePost = async (id, formData) => {
    const response = await axiosAuthInstance.put(`/posts/${id}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

