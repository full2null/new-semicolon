// 인증 관련 api

const API_URL = 'http://localhost:8000/api/v1';

// 회원가입
export async function register(user_data) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(user_data),
  });

  const data = await res.json();

  if (!res.ok) {
    // 에러 처리
    const err_msg = data.detail?.message || data.message || '회원가입 실패';
    throw new Error(err_msg);
  }

  return data;
}

// 로그인
export async function login(user_name, pw) {
  const form = new URLSearchParams();
  form.append('username', user_name);
  form.append('password', pw);

  const res = await fetch(`${API_URL}/auth/token`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: form,
  });

  const data = await res.json();

  if (!res.ok) {
    const err_msg = data.detail?.message || data.message || '로그인 실패';
    throw new Error(err_msg);
  }

  // OAuth2 표준 형식: { access_token, token_type }
  return data;
}

// 내 정보 가져오기
export async function get_me(token) {
  const res = await fetch(`${API_URL}/users/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  const data = await res.json();

  if (!res.ok) {
    const err_msg = data.detail?.message || data.message || '사용자 정보 가져오기 실패';
    throw new Error(err_msg);
  }

  return data;
}
