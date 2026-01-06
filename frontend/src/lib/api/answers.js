// 답변 관련 API 함수들
import { api_post, api_put, api_delete } from './client.js';

/**
 * 답변 작성하기
 * @param {object} answer_data - 답변 데이터 { question_id, content }
 * @returns {Promise<object>} 생성된 답변 정보
 */
export async function create_answer(answer_data) {
  return api_post('/answers/', answer_data);
}

/**
 * 답변 수정하기
 * @param {number} answer_id - 답변 ID
 * @param {object} answer_data - 수정할 데이터 { content }
 * @returns {Promise<object>} 수정된 답변 정보
 */
export async function update_answer(answer_id, answer_data) {
  return api_put(`/answers/${answer_id}`, answer_data);
}

/**
 * 답변 삭제하기
 * @param {number} answer_id - 답변 ID
 * @returns {Promise<void>}
 */
export async function delete_answer(answer_id) {
  return api_delete(`/answers/${answer_id}`);
}

/**
 * 답변에 투표하기
 * @param {number} answer_id - 답변 ID
 * @param {number} vote - 투표 값 (1: 추천, -1: 비추천)
 * @returns {Promise<object>} 업데이트된 답변 정보
 */
export async function vote_answer(answer_id, vote) {
  return api_post(`/answers/${answer_id}/vote`, { vote });
}

/**
 * 답변 채택하기
 * @param {number} answer_id - 답변 ID
 * @returns {Promise<object>} 채택된 답변 정보
 */
export async function accept_answer(answer_id) {
  return api_post(`/answers/${answer_id}/accept`, {});
}
