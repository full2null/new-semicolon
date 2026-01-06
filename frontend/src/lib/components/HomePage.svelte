<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { get_stats } from "$lib/api/client.js";

  const dispatch = createEventDispatcher();

  // 통계 데이터
  let stats = {
    question_count: 0,
    answer_count: 0,
    user_count: 0,
  };

  // 컴포넌트 마운트 시 통계 로드
  onMount(async () => {
    try {
      stats = await get_stats();
    } catch (error) {
      console.error("통계 로드 실패:", error);
    }
  });

  // 질문 목록으로 이동
  function go_to_questions() {
    dispatch("navigate", { page: "questions" });
  }
</script>

<main class="flex-1 p-6 overflow-y-auto">
  <div class="max-w-5xl mx-auto">
    <!-- Welcome Section -->
    <section class="mb-8">
      <h1 class="text-4xl font-bold mb-4">Semicolon에 오신 것을 환영합니다</h1>
      <p class="text-lg text-muted-foreground mb-6">
        개발자들이 모여 질문하고 답변을 나누는 커뮤니티입니다.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="p-4 bg-card rounded-lg border">
          <h3 class="text-2xl font-bold text-primary mb-2">
            {stats.question_count.toLocaleString()}
          </h3>
          <p class="text-sm text-muted-foreground">질문</p>
        </div>
        <div class="p-4 bg-card rounded-lg border">
          <h3 class="text-2xl font-bold text-primary mb-2">
            {stats.answer_count.toLocaleString()}
          </h3>
          <p class="text-sm text-muted-foreground">답변</p>
        </div>
        <div class="p-4 bg-card rounded-lg border">
          <h3 class="text-2xl font-bold text-primary mb-2">
            {stats.user_count.toLocaleString()}
          </h3>
          <p class="text-sm text-muted-foreground">사용자</p>
        </div>
      </div>
    </section>

    <!-- 빠른 시작 버튼들 -->
    <section>
      <h2 class="text-2xl font-bold mb-4">빠른 시작</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button
          class="p-6 bg-card rounded-lg border hover:border-primary transition-colors text-left"
          on:click={go_to_questions}
        >
          <h3 class="text-lg font-semibold mb-2">질문하기</h3>
          <p class="text-sm text-muted-foreground">
            궁금한 것이 있나요? 지금 바로 질문해보세요.
          </p>
        </button>
        <button
          class="p-6 bg-card rounded-lg border hover:border-primary transition-colors text-left"
          on:click={() => dispatch("navigate", { page: "users" })}
        >
          <h3 class="text-lg font-semibold mb-2">사용자 보기</h3>
          <p class="text-sm text-muted-foreground">
            다른 개발자들을 찾아보세요.
          </p>
        </button>
      </div>
    </section>
  </div>
</main>
