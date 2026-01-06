import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// 인증 스토어 만들기
function make_auth_store() {
  // 브라우저면 로컨 스토리지에서 불러오기
  const saved_token = browser ? localStorage.getItem('token') : null;
  const saved_user = browser ? localStorage.getItem('user') : null;

  const { subscribe, set, update } = writable({
    token: saved_token,
    user: saved_user ? JSON.parse(saved_user) : null,
  });

  return {
    subscribe,
    // 로그인
    login: (token, user) => {
      if (browser) {
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
      }
      set({ token, user });
    },
    // 로그아웃
    logout: () => {
      if (browser) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
      set({ token: null, user: null });
    },
    // 유저 정보 업데이트
    update_user: (user) => {
      if (browser) {
        localStorage.setItem('user', JSON.stringify(user));
      }
      update(s => ({ ...s, user }));
    },
  };
}

export const authStore = make_auth_store();
