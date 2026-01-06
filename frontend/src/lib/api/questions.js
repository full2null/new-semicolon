// 질문 관련 API 함수들
import { api_get, api_post, api_put, api_delete } from './client.js';

/**
 * 질문 목록 가져오기
 * @param {object} params - 쿼리 파라미터 (skip, limit, tag 등)
 * @returns {Promise<Array>} 질문 목록
 */
export async function get_questions(params = {}) {
  return api_get('/questions/', params);
}

/**
 * 질문 상세 정보 가져오기
 * @param {number} question_id - 질문 ID
 * @returns {Promise<object>} 질문 상세 정보
 */
export async function get_question(question_id) {
  return api_get(`/questions/${question_id}`);
}

/**
 * 질문 작성하기
 * @param {object} q_data - 질문 데이터 { title, content, tags }
 * @returns {Promise<object>} 생성된 질문 정보
 */
export async function create_question(q_data) {
  return api_post('/questions/', q_data);
}

/**
 * 질문 수정하기
 * @param {number} question_id - 질문 ID
 * @param {object} q_data - 수정할 데이터 { title, content, tags }
 * @returns {Promise<object>} 수정된 질문 정보
 */
export async function update_question(question_id, q_data) {
  return api_put(`/questions/${question_id}`, q_data);
}

/**
 * 질문 삭제하기
 * @param {number} question_id - 질문 ID
 * @returns {Promise<void>}
 */
export async function delete_question(question_id) {
  return api_delete(`/questions/${question_id}`);
}

/**
 * 질문의 답변 목록 가져오기
 * @param {number} question_id - 질문 ID
 * @returns {Promise<Array>} 답변 목록
 */
export async function get_question_answers(question_id) {
  return api_get(`/questions/${question_id}/answers`);
}

/**
 * 질문에 투표하기
 * @param {number} question_id - 질문 ID
 * @param {number} vote - 투표 값 (1: 추천, -1: 비추천)
 * @returns {Promise<object>} 업데이트된 질문 정보
 */
export async function vote_question(question_id, vote) {
  return api_post(`/questions/${question_id}/vote`, { vote });
}
