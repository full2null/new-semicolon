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

  // 인기 질문 데이터 (샘플)
  const hot_questions = [
    {
      id: "1",
      title: "React에서 useState를 사용할 때 비동기 문제를 어떻게 해결하나요?",
      author: "개발자123",
      votes: 5,
      answers: 3,
      views: 142,
      tags: ["react", "javascript", "useState"],
    },
    {
      id: "2",
      title: "SvelteKit에서 서버 사이드 렌더링 최적화 방법",
      author: "프론트엔드러",
      votes: 12,
      answers: 7,
      views: 289,
      tags: ["svelte", "sveltekit", "ssr", "performance"],
    },
    {
      id: "3",
      title: "TypeScript에서 Generic 타입을 효과적으로 사용하는 방법",
      author: "타입마스터",
      votes: 8,
      answers: 5,
      views: 201,
      tags: ["typescript", "javascript"],
    },
  ];

  // 질문 상세로 이동
  function go_to_question(id) {
    dispatch("navigate", { page: "question", id });
  }

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

    <!-- 인기 질문 섹션 -->
    <section class="mb-8">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-bold">인기 질문</h2>
        <button
          class="text-primary hover:underline text-sm"
          on:click={go_to_questions}
        >
          모두 보기 →
        </button>
      </div>
      <div class="space-y-4">
        {#each hot_questions as q (q.id)}
          <div
            class="p-4 bg-card rounded-lg border hover:border-primary transition-colors cursor-pointer"
            on:click={() => go_to_question(q.id)}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && go_to_question(q.id)}
          >
            <h3 class="text-lg font-semibold mb-2 hover:text-primary">
              {q.title}
            </h3>
            <div class="flex items-center gap-4 text-sm text-muted-foreground">
              <span>{q.author}</span>
              <span>•</span>
              <span>답변 {q.answers}</span>
            </div>
          </div>
        {/each}
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
