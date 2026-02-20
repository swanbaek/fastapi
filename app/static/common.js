// common.js: JWT 토큰 파싱 및 API 요청 인터셉터 함수

// JWT 토큰의 payload를 파싱해서 객체로 반환
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) { return null; }
}

// JWT 기반 API 요청 인터셉터 함수
async function apiFetch(url, options = {}, retry = true) {
    const accessToken = localStorage.getItem('accessToken');
    if (!options.headers) options.headers = {};
    if (accessToken) {
        options.headers['Authorization'] = 'Bearer ' + accessToken;
    }
    ///////////////////////////
    const originalBody = options.body; // 추가: body 미리 저장. body가 변형됐을 경우를 대비한 방어적 코드
    ///////////////////////////
    let response = await fetch(url, options);
    // accessToken 만료 시 refreshToken으로 재발급 시도
    if ((response.status === 401  || response.status === 403) && retry) {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
            const refreshRes = await fetch('/auth/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refreshToken })
            });
            if (refreshRes.ok) {
                const data = await refreshRes.json();
                if (data.accessToken) {
                    localStorage.setItem('accessToken', data.accessToken);
                    // 재시도
                    options.headers['Authorization'] = 'Bearer ' + data.accessToken;
                    options.body = originalBody; 
                    // body 복원 (옵션) body가 변형됐을 경우를 대비한 방어적 코드

                    return fetch(url, options);
                }
            } else {
                // refreshToken도 만료: 로그아웃 처리
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                window.location.reload();
            }
        }
    }
    return response;
}
// window 전역에 등록
window.apiFetch = apiFetch;
window.parseJwt = parseJwt;
