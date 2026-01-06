// API 클라이언트 기본 설정
import { get } from 'svelte/store';
import { authStore } from '$lib/stores/auth.js';

// 백엔드 API 기본 URL
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * API 요청 에러
 */
export class ApiError extends Error {
  constructor(message, status, data) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'ApiError';
  }
}

/**
 * API 요청 보내기
 * @param {string} endpoint - API 엔드포인트 (/questions 등)
 * @param {object} options - fetch 옵션
 * @returns {Promise<any>} 응답 데이터
 */
export async function api_request(endpoint, options = {}) {
  const auth = get(authStore);
  
  // 기본 헤더 설정
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // 인증 토큰 있으면 추가
  if (auth.token) {
    headers['Authorization'] = `Bearer ${auth.token}`;
  }

  // 요청 보내기
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // 응답 데이터 파싱
  let data = null;
  const content_type = response.headers.get('content-type');
  if (content_type && content_type.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  // 에러 처리
  if (!response.ok) {
    const error_msg = data?.detail || data?.message || `API 요청 실패: ${response.status}`;
    throw new ApiError(error_msg, response.status, data);
  }

  return data;
}

/**
 * GET 요청
 */
export async function api_get(endpoint, params = null) {
  let url = endpoint;
  if (params) {
    const query = new URLSearchParams(params).toString();
    url = `${endpoint}?${query}`;
  }
  return api_request(url, { method: 'GET' });
}

/**
 * POST 요청
 */
export async function api_post(endpoint, body) {
  return api_request(endpoint, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * PUT 요청
 */
export async function api_put(endpoint, body) {
  return api_request(endpoint, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
}

/**
 * DELETE 요청
 */
export async function api_delete(endpoint) {
  return api_request(endpoint, { method: 'DELETE' });
}
