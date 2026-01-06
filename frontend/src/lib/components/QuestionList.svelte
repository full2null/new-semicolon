<script>
  import QuestionCard from "$lib/components/QuestionCard.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import { createEventDispatcher, onMount } from "svelte";
  import { questions_store } from "$lib/stores/questions.js";
  import { get_questions } from "$lib/api/questions.js";

  /** @type {string | undefined} */
  export let searchQuery = undefined;

  const dispatch = createEventDispatcher();

  // 질문 스토어 구독
  let q_list = [];
  let loading = false;
  let error = null;
  let total = 0;
  let cur_page = 1;

  questions_store.subscribe(s => {
    q_list = s.list;
    loading = s.loading;
    error = s.error;
    total = s.total;
    cur_page = s.page;
  });

  // 네비게이션 이벤트 전달하는 함수
  function on_nav(event) {
    dispatch("navigate", event.detail);
  }

  // API에서 질문 목록 가져오기
  async function load_questions(page = 1) {
    try {
      questions_store.set_loading(true);
      questions_store.set_page(page);
      
      const params = {
        skip: (page - 1) * 20,
        limit: 20,
      };
      
      // 검색어 추가
      if (searchQuery && searchQuery.trim()) {
        params.q = searchQuery.trim();
        console.log('검색 파라미터 추가:', params.q);
      }
      
      const result = await get_questions(params);
      console.log('검색:', searchQuery, '파라미터:', params, 'API 응답:', result);
      
      // API 응답 형식: { success: true, data: [...] }
      // data가 배열인지 확인
      let questions = [];
      if (Array.isArray(result)) {
        questions = result;
      } else if (result.data && Array.isArray(result.data)) {
        questions = result.data;
      } else if (result.items && Array.isArray(result.items)) {
        questions = result.items;
      }
      
      console.log('추출된 질문 목록:', questions);
      const total_count = result.total || questions.length;
      questions_store.set_list(questions, total_count);
    } catch (err) {
      console.error('질문 목록 불러오기 실패:', err);
      questions_store.set_error(err.message);
    } finally {
      questions_store.set_loading(false);
    }
  }

  // 컴포넌트 마운트될 때 질문 목록 가져오기
  onMount(() => {
    load_questions();
  });

  // searchQuery 변경시 재검색
  $: if (searchQuery !== undefined) {
    load_questions(1);
  }

  // 샘플 데이터 제거 (이제 API 사용)
  /*const q_list = [
    {
      id: "1",
      title: "React에서 useState를 사용할 때 비동기 문제를 어떻게 해결하나요?",
      content:
        "setState를 호출한 후 바로 state 값을 참조하면 이전 값이 나오는 문제가 있습니다. 이를 해결하는 방법이 궁금합니다.",
      author: "개발자123",
      createdAt: "2024-01-15T10:30:00Z",
      views: 142,
      answers: 3,
      votes: 5,
      tags: ["react", "javascript", "useState"],
      hasAcceptedAnswer: true,
    },
    {
      id: "2",
      title: "SvelteKit에서 서버 사이드 렌더링 최적화 방법",
      content:
        "페이지 로딩 속도를 개선하기 위해 SSR을 최적화하고 싶습니다. 어떤 방법들이 있을까요?",
      author: "프론트엔드러",
      createdAt: "2024-01-15T09:15:00Z",
      views: 89,
      answers: 1,
      votes: 8,
      tags: ["svelte", "sveltekit", "ssr", "performance"],
      hasAcceptedAnswer: false,
    },
    {
      id: "3",
      title: "TypeScript에서 Generic 타입을 효과적으로 사용하는 방법",
      content:
        "복잡한 데이터 구조를 다룰 때 Generic을 어떻게 활용하면 좋을지 조언 부탁드립니다.",
      author: "타입스크립터",
      createdAt: "2024-01-15T08:45:00Z",
      views: 203,
      answers: 7,
      votes: 12,
      tags: ["typescript", "generics", "type-safety"],
      hasAcceptedAnswer: true,
    },
    {
      id: "4",
      title: "CSS Grid vs Flexbox: 언제 어떤 것을 사용해야 할까요?",
      content:
        "레이아웃을 구성할 때 Grid와 Flexbox 중 어떤 것을 선택해야 하는지 기준이 궁금합니다.",
      author: "CSS마스터",
      createdAt: "2024-01-15T07:20:00Z",
      views: 156,
      answers: 4,
      votes: 9,
      tags: ["css", "grid", "flexbox", "layout"],
      hasAcceptedAnswer: false,
    },
    {
      id: "5",
      title: "Node.js에서 메모리 누수를 방지하는 방법",
      content:
        "대용량 데이터를 처리하는 Node.js 애플리케이션에서 메모리 누수가 발생하는 문제를 해결하고 싶습니다.",
      author: "백엔드개발자",
      createdAt: "2024-01-15T06:10:00Z",
      views: 78,
      answers: 2,
      votes: 6,
      tags: ["nodejs", "memory-management", "performance"],
      hasAcceptedAnswer: false,
    },
  ];*/

  let sort_type = "newest";
  const sort_list = [
    { value: "newest", label: "최신순" },
    { value: "answers", label: "답변순" },
  ];

  // 정렬 방식 변경시 다시 로드
  let prev_sort = sort_type;
  $: if (sort_type !== prev_sort) {
    prev_sort = sort_type;
    load_questions(cur_page);
  }

  // 페이지 변경
  function go_to_page(page) {
    if (page >= 1 && page <= total_pages) {
      load_questions(page);
    }
  }

  // 총 페이지 수 계산
  $: total_pages = Math.ceil(total / 20) || 1;
  
  // 페이지 번호 목록 생성 (현재 페이지 주변 5개)
  $: page_nums = Array.from({ length: Math.min(5, total_pages) }, (_, i) => {
    const start = Math.max(1, Math.min(cur_page - 2, total_pages - 4));
    return start + i;
  }).filter(p => p <= total_pages);
</script>

<main class="flex-1 p-6">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-foreground mb-2">질문</h1>
        <p class="text-muted-foreground">
          개발자들의 질문과 답변을 나누는 공간입니다.
        </p>
      </div>
      <Button
        variant="default"
        on:click={() => dispatch("navigate", { page: "ask" })}
      >
        질문하기
      </Button>
    </div>

    <!-- 로딩 중 -->
    {#if loading}
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p class="text-muted-foreground">질문을 불러오는 중...</p>
        </div>
      </div>
    {:else if error}
      <!-- 에러 발생 -->
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <p class="text-destructive mb-4">❌ {error}</p>
          <Button on:click={() => load_questions(cur_page)}>다시 시도</Button>
        </div>
      </div>
    {:else}
    <!-- 필터랑 정렬 -->
    <div class="flex items-center justify-between mb-6 pb-4 border-b">
      <div class="flex items-center space-x-4">
        <span class="text-sm text-muted-foreground">
          총 {total}개의 질문
        </span>
      </div>

      <div class="flex items-center space-x-2">
        <span class="text-sm text-muted-foreground">정렬:</span>
        <select
          bind:value={sort_type}
          class="text-sm border border-input rounded-md px-3 py-1 bg-background"
        >
          {#each sort_list as opt (opt.value)}
            <option value={opt.value}>{opt.label}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- 질문 리스트 -->
    {#if q_list.length === 0}
      <div class="text-center py-12">
        <p class="text-muted-foreground mb-4">아직 질문이 없습니다.</p>
        <Button on:click={() => dispatch("navigate", { page: "ask" })}>
          첫 질문 작성하기
        </Button>
      </div>
    {:else}
      <div class="space-y-4">
        {#each q_list as q (q.id)}
          <QuestionCard question={q} on:navigate={on_nav} />
        {/each}
      </div>

      <!-- Pagination -->
      <div class="flex items-center justify-center mt-8 space-x-2">
        <Button 
          variant="outline" 
          size="sm" 
          disabled={cur_page === 1}
          on:click={() => go_to_page(cur_page - 1)}
        >
          이전
        </Button>
        
        {#each page_nums as page_num}
          <Button 
            variant={page_num === cur_page ? "default" : "outline"} 
            size="sm"
            on:click={() => go_to_page(page_num)}
          >
            {page_num}
          </Button>
        {/each}
        
        <Button 
          variant="outline" 
          size="sm" 
          disabled={cur_page === total_pages}
          on:click={() => go_to_page(cur_page + 1)}
        >
          다음
        </Button>
      </div>
    {/if}
    {/if}
  </div>
</main>
