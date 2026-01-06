<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  // 태그 데이터 (나중에 api에서 받아올거임)
  const tag_list = [
    { name: "javascript", count: 342, desc: "웹 개발의 핵심 프로그래밍 언어" },
    { name: "react", count: 256, desc: "Facebook이 개발한 UI 라이브러리" },
    { name: "typescript", count: 198, desc: "JavaScript의 타입이 있는 상위 집합" },
    { name: "svelte", count: 145, desc: "컴파일 타임에 최적화되는 프레임워크" },
    { name: "python", count: 287, desc: "다목적 고수준 프로그래밍 언어" },
    { name: "nodejs", count: 223, desc: "JavaScript 런타임 환경" },
    { name: "css", count: 189, desc: "웹 페이지 스타일링 언어" },
    { name: "html", count: 167, desc: "웹 페이지의 구조를 정의하는 마크업 언어" },
    { name: "vue", count: 134, desc: "점진적 JavaScript 프레임워크" },
    { name: "angular", count: 112, desc: "Google이 개발한 웹 애플리케이션 프레임워크" },
    { name: "git", count: 156, desc: "분산 버전 관리 시스템" },
    { name: "docker", count: 143, desc: "컨테이너 기반 가상화 플랫폼" },
  ];

  let search_word = "";

  // 검색어로 필터링
  $: filtered = tag_list.filter((t) =>
    t.name.toLowerCase().includes(search_word.toLowerCase())
  );

  // 태그 클릭하면 해당 태그의 질문목록으로
  function on_tag_click(tag_name) {
    dispatch("navigate", { page: "questions", tag: tag_name });
  }
</script>

<main class="flex-1 p-6 overflow-y-auto">
  <div class="max-w-5xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl font-bold mb-4">태그</h1>
      <p class="text-lg text-muted-foreground mb-6">
        태그는 질문을 분류하고 찾기 쉽게 만듭니다. 관심 있는 태그를 찾아보세요.
      </p>

      <!-- 검색바 -->
      <div class="mb-6">
        <input
          type="text"
          bind:value={search_word}
          placeholder="태그 검색..."
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
    </div>

    <!-- 태그 그리드 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each filtered as t (t.name)}
        <button
          class="tag-card p-4 bg-card rounded-lg border hover:border-primary transition-all text-left"
          on:click={() => on_tag_click(t.name)}
        >
          <div class="flex items-start justify-between mb-2">
            <span class="px-3 py-1 bg-secondary text-secondary-foreground rounded font-mono text-sm">
              {t.name}
            </span>
            <span class="text-sm text-muted-foreground">{t.count} 질문</span>
          </div>
          <p class="text-sm text-muted-foreground mt-2">{t.desc}</p>
        </button>
      {/each}
    </div>

    {#if filtered.length === 0}
      <div class="text-center py-12">
        <p class="text-muted-foreground">검색 결과가 없습니다.</p>
      </div>
    {/if}
  </div>
</main>

<style>
  .tag-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
</style>
