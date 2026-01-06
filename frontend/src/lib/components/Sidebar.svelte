<script>
  import { createEventDispatcher, onMount } from "svelte";
  import { cn } from "$lib/utils.js";
  import { get_stats } from "$lib/api/stats.js";

  /** @type {string} */
  export let currentPage = "home";

  const dispatch = createEventDispatcher();

  // 통계 데이터
  let stats = {
    question_count: 0,
    answer_count: 0,
    user_count: 0,
  };
  let loading_stats = false;

  // 통계 불러오기
  async function load_stats() {
    try {
      loading_stats = true;
      stats = await get_stats();
    } catch (error) {
      console.error("통계 로드 실패:", error);
    } finally {
      loading_stats = false;
    }
  }

  // 컴포넌트 마운트 시 통계 로드
  onMount(() => {
    load_stats();
  });

  // 페이지 이동
  function go_to(page) {
    dispatch("navigate", { page });
  }

  // 메인 메뉴 아이템들
  const main_menu = [
    {
      id: "home",
      label: "홈",
      icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m0 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V10M9 21h6",
    },
    {
      id: "questions",
      label: "질문",
      icon: "M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    },
    {
      id: "users",
      label: "사용자",
      icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z",
    },
  ];

  // 커뮤니티 메뉴
  const sub_menu = [
    {
      id: "guidelines",
      label: "가이드라인",
      icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    },
    {
      id: "help",
      label: "도움말",
      icon: "M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
    },
  ];
</script>

<aside class="w-64 bg-background border-r min-h-screen">
  <div class="p-4">
    <!-- 메인 메뉴 -->
    <nav class="space-y-2">
      {#each main_menu as item (item.id)}
        <button
          class={cn("nav-button", currentPage === item.id ? "active" : "")}
          on:click={() => go_to(item.id)}
        >
          <svg
            class="w-5 h-5 mr-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d={item.icon}
            />
          </svg>
          {item.label}
        </button>
      {/each}
    </nav>

    <!-- 구분선 -->
    <div class="my-6 border-t"></div>

    <!-- 커뮤니티 섹션 -->
    <div>
      <h3
        class="px-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3"
      >
        커뮤니티
      </h3>
      <nav class="space-y-2">
        {#each sub_menu as item (item.id)}
          <button
            class={cn("nav-button", currentPage === item.id ? "active" : "")}
            on:click={() => go_to(item.id)}
          >
            <svg
              class="w-5 h-5 mr-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d={item.icon}
              />
            </svg>
            {item.label}
          </button>
        {/each}
      </nav>
    </div>

    <!-- 활동 통계 -->
    <div class="mt-8 p-3 bg-muted rounded-lg">
      <h4 class="text-sm font-medium mb-2">활동 통계</h4>
      {#if loading_stats}
        <div class="text-center text-sm text-muted-foreground py-2">
          로딩 중...
        </div>
      {:else}
        <div class="space-y-2 text-sm text-muted-foreground">
          <div class="flex justify-between">
            <span>질문</span>
            <span>{stats.question_count.toLocaleString()}</span>
          </div>
          <div class="flex justify-between">
            <span>답변</span>
            <span>{stats.answer_count.toLocaleString()}</span>
          </div>
          <div class="flex justify-between">
            <span>사용자</span>
            <span>{stats.user_count.toLocaleString()}</span>
          </div>
        </div>
      {/if}
    </div>
  </div>
</aside>

<style>
  .nav-button {
    width: 100%;
    display: flex;
    align-items: center;
    padding: 0.5rem 0.75rem;
    font-size: 0.875rem;
    font-weight: 500;
    border-radius: 0.375rem;
    transition: background-color 0.15s ease-in-out;
    border: none;
    cursor: pointer;
    background-color: transparent;
    color: inherit;
    text-align: left;
  }

  .nav-button:hover {
    background-color: rgba(0, 0, 0, 0.08);
  }

  .nav-button:active {
    background-color: rgba(0, 0, 0, 0.15);
  }

  .nav-button.active {
    background-color: var(--primary);
    color: var(--primary-foreground);
  }

  .nav-button.active:hover {
    background-color: var(--primary);
    opacity: 0.9;
  }

  :global(.dark) .nav-button:hover {
    background-color: rgba(255, 255, 255, 0.08);
  }

  :global(.dark) .nav-button:active {
    background-color: rgba(255, 255, 255, 0.15);
  }
</style>
