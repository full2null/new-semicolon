<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { create_question } from "$lib/api/questions.js";
  import { questions_store } from "$lib/stores/questions.js";
  import { authStore } from "$lib/stores/auth.js";

  const dispatch = createEventDispatcher();

  // 현재 사용자 정보
  let current_user = null;
  authStore.subscribe(s => {
    current_user = s.user;
  });

  // 컴포넌트 마운트 시 로그
  onMount(() => {
    console.log("QuestionForm 마운트됨, 현재 사용자:", current_user);
  });

  // 입력값들
  let q_title = "";
  let q_content = "";
  let is_sending = false;
  let err_msg = "";

  // 취소 버튼
  function on_cancel() {
    console.log("취소 버튼 클릭됨");
    dispatch("cancel");
  }

  // 제출 버튼
  async function on_submit() {
    // 로그인 확인
    if (!current_user) {
      err_msg = "질문을 작성하려면 먼저 로그인해주세요.";
      return;
    }

    // 체크
    if (!q_title.trim()) {
      err_msg = "제목을 입력해주세요.";
      return;
    }
    if (!q_content.trim()) {
      err_msg = "내용을 입력해주세요.";
      return;
    }

    is_sending = true;
    err_msg = "";

    try {
      const data = {
        title: q_title.trim(),
        content: q_content.trim(),
      };

      // API 호출하여 질문 작성
      const result = await create_question(data);
      // API 응답 형식: { success: true, data: {...} }
      const new_question = result.data || result;
      
      // 스토어에 추가
      questions_store.add_question(new_question);

      dispatch("submit", new_question);
      dispatch("cancel"); // 모달 닫기
    } catch (e) {
      console.error("질문 작성 실패:", e);
      err_msg = e.message || "질문 작성에 실패했습니다. 다시 시도해주세요.";
    } finally {
      is_sending = false;
    }
  }
</script>

<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
  <div 
    class="bg-background rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto"
    on:click={(e) => e.stopPropagation()}
    role="dialog"
  >
    <div class="sticky top-0 bg-background border-b p-6">
      <h2 class="text-2xl font-bold">질문하기</h2>
      <p class="text-sm text-muted-foreground mt-1">
        커뮤니티에 질문을 올려보세요. 다른 개발자들이 도와드릴 거예요!
      </p>
    </div>

    <form on:submit|preventDefault={on_submit} class="p-6 space-y-6">
      <!-- 에러 메시지 -->
      {#if err_msg}
        <div class="p-3 bg-destructive/10 border border-destructive/20 rounded-md">
          <p class="text-sm text-destructive">{err_msg}</p>
        </div>
      {/if}

      <!-- 제목 -->
      <div>
        <label for="title" class="block text-sm font-medium mb-2">
          제목 <span class="text-red-500">*</span>
        </label>
        <input
          id="title"
          type="text"
          bind:value={q_title}
          placeholder="질문의 핵심을 간단명료하게 작성해주세요"
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          maxlength="200"
          required
        />
        <p class="text-xs text-muted-foreground mt-1">
          {q_title.length}/200
        </p>
      </div>

      <!-- 내용 -->
      <div>
        <label for="content" class="block text-sm font-medium mb-2">
          내용 <span class="text-red-500">*</span>
        </label>
        <textarea
          id="content"
          bind:value={q_content}
          placeholder="문제 상황, 시도해본 방법, 기대하는 결과 등을 자세히 설명해주세요.&#10;&#10;코드를 포함할 경우 백틱(```)을 사용하여 코드 블록으로 감싸주세요."
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary min-h-[300px] resize-y"
          required
        ></textarea>
        <p class="text-xs text-muted-foreground mt-1">
          마크다운 형식을 지원합니다.
        </p>
      </div>

      <!-- 작성 가이드 -->
      <div class="p-4 bg-muted rounded-lg">
        <h3 class="text-sm font-semibold mb-2">💡 좋은 질문을 위한 팁</h3>
        <ul class="text-sm text-muted-foreground space-y-1">
          <li>• 제목은 문제의 핵심을 명확하게 표현하세요</li>
          <li>• 문제 상황, 기대하는 결과, 실제 결과를 구분하여 작성하세요</li>
          <li>• 관련 코드는 최소한으로 줄여서 포함하세요</li>
          <li>• 에러 메시지가 있다면 전체 내용을 포함하세요</li>
          <li>• 시도해본 해결 방법들을 공유하세요</li>
        </ul>
      </div>

      <!-- 버튼 -->
      <div class="flex gap-3 justify-end pt-4 border-t">
        <button
          type="button"
          on:click={on_cancel}
          class="px-4 py-2 border rounded-md hover:bg-accent transition-colors"
          disabled={is_sending}
        >
          취소
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={is_sending}
        >
          {is_sending ? "작성 중..." : "질문 올리기"}
        </button>
      </div>
    </form>
  </div>
</div>

<style>
  /* 스크롤바 스타일링 */
  textarea::-webkit-scrollbar {
    width: 8px;
  }

  textarea::-webkit-scrollbar-track {
    background: transparent;
  }

  textarea::-webkit-scrollbar-thumb {
    background: #cbd5e0;
    border-radius: 4px;
  }

  textarea::-webkit-scrollbar-thumb:hover {
    background: #a0aec0;
  }
</style>
