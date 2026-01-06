// 통계 API
import { api_request } from "./client.js";

/**
 * 전체 통계 조회 (질문 수, 답변 수, 사용자 수)
 * @returns {Promise<{question_count: number, answer_count: number, user_count: number}>}
 */
export async function get_stats() {
  const response = await api_request("/stats");
  return response.data;
}
