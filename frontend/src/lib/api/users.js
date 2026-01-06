// 사용자 API
import { api_request } from "./client.js";

/**
 * 현재 로그인한 사용자 정보 조회
 * @returns {Promise<Object>}
 */
export async function get_me() {
  const response = await api_request("/users/me");
  return response.data;
}

/**
 * 현재 로그인한 사용자 정보 업데이트
 * @param {Object} userData - 업데이트할 사용자 데이터
 * @returns {Promise<Object>}
 */
export async function update_me(userData) {
  const response = await api_request("/users/me", {
    method: "PUT",
    body: JSON.stringify(userData),
  });
  return response.data;
}

/**
 * 현재 로그인한 사용자의 통계 조회
 * @returns {Promise<{question_count: number, answer_count: number}>}
 */
export async function get_me_stats() {
  const response = await api_request("/users/me/stats");
  return response.data;
}

/**
 * 특정 사용자 정보 조회
 * @param {number} userId - 사용자 ID
 * @returns {Promise<Object>}
 */
export async function get_user(userId) {
  const response = await api_request(`/users/${userId}`);
  return response.data;
}
