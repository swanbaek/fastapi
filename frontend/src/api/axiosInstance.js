import axios from 'axios';
//사용자 인증이나 인가가 필요없는 서비스 요청시 사용
const axiosInstance = axios.create({
    baseURL: ``,  // 프록시 설정으로 baseURL 제거
    //baseURL: `https://myswan.shop`, //https설정시 문제 발생하면 이걸로 변경
    headers: {
        'Content-Type': 'application/json',
    },
});
export default axiosInstance;
