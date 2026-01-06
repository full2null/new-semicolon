// 질문 관련 전역 상태 관리
import { writable } from 'svelte/store';

/**
 * 질문 목록 스토어
 */
function make_questions_store() {
  const { subscribe, set, update } = writable({
    list: [],           // 질문 목록
    loading: false,     // 로딩 중인지
    error: null,        // 에러 메시지
    total: 0,           // 전체 개수
    page: 1,            // 현재 페이지
    per_page: 20,       // 페이지당 개수
  });

  return {
    subscribe,
    // 목록 설정
    set_list: (questions, total = null) => update(s => ({
      ...s,
      list: questions,
      total: total !== null ? total : questions.length,
      error: null,
    })),
    // 로딩 상태 설정
    set_loading: (loading) => update(s => ({ ...s, loading })),
    // 에러 설정
    set_error: (error) => update(s => ({ ...s, error, loading: false })),
    // 페이지 변경
    set_page: (page) => update(s => ({ ...s, page })),
    // 질문 추가 (새로 작성)
    add_question: (q) => update(s => ({
      ...s,
      list: [q, ...s.list],
      total: s.total + 1,
    })),
    // 질문 업데이트
    update_question: (q_id, q_data) => update(s => ({
      ...s,
      list: s.list.map(q => q.id === q_id ? { ...q, ...q_data } : q),
    })),
    // 질문 삭제
    remove_question: (q_id) => update(s => ({
      ...s,
      list: s.list.filter(q => q.id !== q_id),
      total: s.total - 1,
    })),
    // 초기화
    reset: () => set({
      list: [],
      loading: false,
      error: null,
      total: 0,
      page: 1,
      per_page: 20,
    }),
  };
}

/**
 * 질문 상세 스토어
 */
function make_question_detail_store() {
  const { subscribe, set, update } = writable({
    question: null,     // 질문 정보
    answers: [],        // 답변 목록
    loading: false,     // 로딩 중인지
    error: null,        // 에러 메시지
  });

  return {
    subscribe,
    // 질문 설정
    set_question: (q) => update(s => ({ ...s, question: q, error: null })),
    // 답변 목록 설정
    set_answers: (answers) => update(s => ({ ...s, answers })),
    // 로딩 상태 설정
    set_loading: (loading) => update(s => ({ ...s, loading })),
    // 에러 설정
    set_error: (error) => update(s => ({ ...s, error, loading: false })),
    // 답변 추가
    add_answer: (answer) => update(s => ({
      ...s,
      answers: [...s.answers, answer],
    })),
    // 답변 업데이트
    update_answer: (answer_id, answer_data) => update(s => ({
      ...s,
      answers: s.answers.map(a => a.id === answer_id ? { ...a, ...answer_data } : a),
    })),
    // 답변 삭제
    remove_answer: (answer_id) => update(s => ({
      ...s,
      answers: s.answers.filter(a => a.id !== answer_id),
    })),
    // 초기화
    reset: () => set({
      question: null,
      answers: [],
      loading: false,
      error: null,
    }),
  };
}

export const questions_store = make_questions_store();
export const question_detail_store = make_question_detail_store();
