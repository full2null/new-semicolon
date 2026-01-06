<script>
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Badge from "$lib/components/ui/Badge.svelte";
  import { createEventDispatcher, onMount } from "svelte";
  import { question_detail_store } from "$lib/stores/questions.js";
  import { get_question, get_question_answers } from "$lib/api/questions.js";
  import { create_answer } from "$lib/api/answers.js";
  import { ApiError } from "$lib/api/client.js";

  /** @type {string} */
  export let questionId;

  // 유저 타입
  /**
   * @typedef {Object} User
   * @property {number} id
   * @property {string} username
   * @property {string} [full_name]
   */

  /** @type {User | null} */
  export let currentUser = null;

  const dispatch = createEventDispatcher();

  // 스토어 구독
  let q_data = null;
  let ans_list = [];
  let loading = false;
  let error = null;

  question_detail_store.subscribe(s => {
    q_data = s.question;
    ans_list = s.answers;
    loading = s.loading;
    error = s.error;
  });

  function normalize_answer(ans) {
    const author = typeof ans?.author === "string"
      ? ans.author
      : ans?.author?.username || ans?.author?.full_name || "익명";

    return {
      ...ans,
      comments: ans?.comments || [],
      createdAt: ans?.createdAt || ans?.created_at || new Date().toISOString(),
      votes: ans?.votes ?? ans?.vote ?? 0,
      author,
      id: ans?.id ?? `tmp-${Date.now()}`,
    };
  }

  // 페이지 이동
  function go_to(page) {
    dispatch("navigate", { page });
  }

  // API에서 질문 정보 불러오기
  async function load_question() {
    try {
      question_detail_store.set_loading(true);
      
      // 질문 상세 정보
      const q_result = await get_question(questionId);
      // API 응답 형식: { success: true, data: {...} }
      const q = q_result.data || q_result;
      question_detail_store.set_question(q);
      
      // 답변 목록
      const ans_result = await get_question_answers(questionId);
      const answers = ans_result.data || ans_result;
      question_detail_store.set_answers(
        (Array.isArray(answers) ? answers : []).map(normalize_answer)
      );
      
    } catch (err) {
      console.error('질문 불러오기 실패:', err);
      question_detail_store.set_error(err.message);
    } finally {
      question_detail_store.set_loading(false);
    }
  }

  // 컴포넌트 마운트될 때 불러오기
  onMount(() => {
    load_question();
  });

  // questionId 바뀔면 다시 불러오기
  $: if (questionId) {
    load_question();
  }

  // 답변 작성 및 UI 상태 변수
  let new_ans = "";
  let sending_answer = false;
  /** @type {Record<string, boolean>} */
  let show_cmt_form = {}; // 답변별 댓글폼 보이기
  /** @type {Record<string, string>} */
  let new_cmt = {}; // 답변별 댓글 내용

  // 샘플 데이터 제거됨 (이제 API 사용)
  /*const q_data = {
    id: questionId,
    title: "React에서 useState를 사용할 때 비동기 문제를 어떻게 해결하나요?",
    content: `setState를 호출한 후 바로 state 값을 참조하면 이전 값이 나오는 문제가 있습니다.

예를 들어:
\`\`\`javascript
const [count, setCount] = useState(0);

const handleClick = () => {
  setCount(count + 1);
  console.log(count); // 여전히 이전 값이 출력됨
};
\`\`\`

이런 상황에서 업데이트된 값을 즉시 사용하려면 어떻게 해야 할까요?`,
    author: "개발자123",
    author_point: 1250,
    createdAt: "2024-01-15T10:30:00Z",
    views: 142,
    votes: 5,
    tags: ["react", "javascript", "useState"],
    has_best: true,
  };*/

  // 추천/비추 처리
  function do_vote(val) {
    if (!currentUser) {
      alert("로그인이 필요합니다.");
      return;
    }
    my_vote = my_vote === val ? 0 : val;
  }

  // 답변 제출
  async function send_answer() {
    if (!currentUser) {
      alert("로그인이 필요합니다.");
      return;
    }

    const content = new_ans.trim();
    if (!content) {
      alert("답변 내용을 입력해주세요.");
      return;
    }

    sending_answer = true;

    try {
      const payload = { question_id: Number(questionId), content };
      const created = await create_answer(payload);
      const created_answer = normalize_answer(created.data || created);

      question_detail_store.add_answer(created_answer);
      new_ans = "";

      const latest = await get_question_answers(questionId);
      const answers = latest.data || latest;
      question_detail_store.set_answers(
        (Array.isArray(answers) ? answers : []).map(normalize_answer)
      );
    } catch (err) {
      console.error("답변 등록 실패:", err);
      let msg = "답변 등록에 실패했습니다. 잠시 후 다시 시도해주세요.";

      if (err instanceof ApiError) {
        const detail = err.data?.detail;
        msg = detail?.message || detail || err.message || msg;

        if (err.status === 401) {
          msg = "로그인이 필요합니다. 로그인 후 다시 시도해주세요.";
          dispatch("navigate", { page: "login" });
        }
      }

      alert(msg);
    } finally {
      sending_answer = false;
    }
  }

  // 댓글폼 열기/닫기
  function toggle_cmt(ans_id) {
    if (!currentUser) {
      alert("로그인이 필요합니다.");
      return;
    }
    show_cmt_form[ans_id] = !show_cmt_form[ans_id];
  }

  // 댓글 제출
  function send_cmt(ans_id) {
    if (!new_cmt[ans_id]?.trim()) {
      alert("댓글 내용을 입력해주세요.");
      return;
    }

    console.log(`답변 ${ans_id}에 댓글:`, new_cmt[ans_id]);
    
    // 댓글 추가 (실제로는 api 호출 후에)
    const ans = ans_list.find(a => a.id === ans_id);
    if (ans && currentUser) {
      const name = (currentUser).username || (currentUser).full_name || "사용자";
      ans.comments = [...ans.comments, {
        id: `c${Date.now()}`,
        content: new_cmt[ans_id],
        author: name,
        createdAt: new Date().toISOString(),
      }];
    }

    new_cmt[ans_id] = "";
    show_cmt_form[ans_id] = false;
  }

  function parse_date(date_str) {
    if (!date_str) return new Date();
    const has_tz = /Z|[+-]\d{2}:?\d{2}$/.test(date_str);
    const iso = has_tz ? date_str : `${date_str}Z`;
    return new Date(iso);
  }

  // 시간 포맷
  function get_time(date_str) {
    if (!date_str) return "방금 전";
    const date = parse_date(date_str);
    const now = new Date();
    const diff_h = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60 * 60),
    );

    if (diff_h < 1) return "방금 전";
    if (diff_h < 24) return `${diff_h}시간 전`;
    if (diff_h < 168) return `${Math.floor(diff_h / 24)}일 전`;
    return date.toLocaleDateString("ko-KR");
  }

  function get_answer_author(ans) {
    if (!ans) return "익명";
    const a = ans.author;
    if (typeof a === "string") return a || "익명";
    return a?.username || a?.full_name || "익명";
  }

  // author 처리 (객체 또는 문자열)
  $: author_name = q_data && (typeof q_data.author === 'string' 
    ? q_data.author 
    : q_data.author?.username || '익명');
  
  // 생성 시간
  $: created_time = q_data && (q_data.createdAt || q_data.created_at);
  
  // 태그
  $: tags = q_data?.tags || [];

</script>

<main class="flex-1 p-6">
  <div class="max-w-4xl mx-auto">
    <!-- 경로 표시 -->
    <nav class="mb-6 text-sm text-muted-foreground">
      <button
        class="hover:text-foreground"
        on:click={() => go_to("home")}
      >
        홈
      </button>
      <span class="mx-2">/</span>
      <button
        class="hover:text-foreground"
        on:click={() => go_to("questions")}
      >
        질문
      </button>
      <span class="mx-2">/</span>
      <span class="text-foreground">질문 상세</span>
    </nav>

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
          <Button on:click={() => load_question()}>다시 시도</Button>
        </div>
      </div>
    {:else if !q_data}
      <!-- 질문이 없음 -->
      <div class="flex items-center justify-center py-12">
        <div class="text-center">
          <p class="text-muted-foreground mb-4">질문을 찾을 수 없습니다.</p>
          <Button on:click={() => go_to("questions")}>질문 목록으로</Button>
        </div>
      </div>
    {:else}
    <!-- 질문 -->
    <Card className="p-6 mb-6">
      <div class="flex items-start space-x-4">
        <!-- 내용 -->
        <div class="flex-1">
          <h1 class="text-2xl font-bold text-foreground mb-4">
            {q_data.title}
          </h1>

          <div class="prose max-w-none mb-4">
            {#each q_data.content.split("\n") as paragraph}
              {#if paragraph.startsWith("```")}
                <pre class="bg-muted p-3 rounded text-sm overflow-x-auto"><code
                    >{paragraph
                      .replace(/```\w*\n?/, "")
                      .replace(/```$/, "")}</code
                  ></pre>
              {:else if paragraph.trim()}
                <p class="mb-3">{paragraph}</p>
              {/if}
            {/each}
          </div>

          <!-- 태그 -->
          <div class="flex flex-wrap gap-2 mb-4">
            {#each tags as tag (tag)}
              <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                {tag}
              </Badge>
            {/each}
          </div>

          <!-- 작성자 정보 -->
          <div
            class="flex items-center justify-between text-sm text-muted-foreground"
          >
            <div class="flex items-center space-x-4">
              <span>{get_time(created_time)}에 질문됨</span>
            </div>
            <div class="flex items-center space-x-2">
              <div
                class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center"
              >
                <span class="text-sm font-medium text-primary">
                  {author_name.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <div class="font-medium text-foreground">{author_name}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>

    <!-- 답변 헤더 -->
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-semibold">
        {ans_list.length}개의 답변
      </h2>
    </div>

    <!-- 답변 목록 -->
    <div class="space-y-6 mb-8">
      {#each ans_list as ans (ans.id)}
        <Card className="p-6">
          {@const ans_author = get_answer_author(ans)}
          <div class="flex items-start space-x-4">
            <!-- 투표 -->
            <div class="flex flex-col items-center space-y-2">
              <button
                class="p-1 rounded hover:bg-accent text-muted-foreground"
                aria-label="추천"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z" />
                </svg>
              </button>
              <span class="text-lg font-medium">{ans.votes}</span>
              <button
                class="p-1 rounded hover:bg-accent text-muted-foreground"
                aria-label="비추천"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6z" />
                </svg>
              </button>
              <!-- 채택 아이콘 -->
              {#if ans.is_best}
                <div
                  class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center"
                  title="채택된 답변"
                >
                  <svg
                    class="w-5 h-5 text-green-600"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
                    />
                  </svg>
                </div>
              {/if}
            </div>

            <!-- 본문 -->
            <div class="flex-1">
              <div class="prose max-w-none mb-4">
                {#each ans.content?.split("\n") || [] as p}
                  {#if p.startsWith("```")}
                    <pre
                      class="bg-muted p-3 rounded text-sm overflow-x-auto"><code
                        >{p
                          .replace(/```\w*\n?/, "")
                          .replace(/```$/, "")}</code
                      ></pre>
                  {:else if p.trim()}
                    <p class="mb-3">{p}</p>
                  {/if}
                {/each}
              </div>

              <!-- 작성자 -->
              <div
                class="flex items-center justify-between text-sm text-muted-foreground"
              >
                    <span>{get_time(ans.createdAt || ans.created_at)}에 답변됨</span>
                <div class="flex items-center space-x-2">
                  <div
                    class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center"
                  >
                    <span class="text-sm font-medium text-primary">
                          {ans_author.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <div>
                    <div class="font-medium text-foreground">
                          {ans_author}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 댓글들 -->
              {#if ans.comments && ans.comments.length > 0}
                <div class="mt-4 space-y-2 border-t border-border pt-4">
                  {#each ans.comments as cmt (cmt.id)}
                    <div class="flex items-start space-x-2 text-sm">
                      <div class="flex-1 bg-muted/50 rounded px-3 py-2">
                        <span class="text-foreground">{cmt.content}</span>
                        <span class="text-muted-foreground mx-2">–</span>
                        <button
                          class="text-primary hover:underline font-medium"
                          on:click={() => go_to("profile")}
                        >
                          {cmt.author}
                        </button>
                        <span class="text-muted-foreground text-xs ml-2">
                          {get_time(cmt.createdAt)}
                        </span>
                      </div>
                    </div>
                  {/each}
                </div>
              {/if}

              <!-- 댓글 추가 버튼 -->
              <div class="mt-3">
                <button
                  class="text-sm text-muted-foreground hover:text-primary"
                  on:click={() => toggle_cmt(ans.id)}
                >
                  댓글 추가
                </button>
              </div>

              <!-- 댓글 폼 -->
              {#if show_cmt_form[ans.id]}
                <div class="mt-3 flex items-start space-x-2">
                  <input
                    type="text"
                    bind:value={new_cmt[ans.id]}
                    placeholder="댓글을 입력하세요..."
                    class="flex-1 px-3 py-2 text-sm border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring"
                    on:keydown={(e) => {
                      if (e.key === 'Enter') {
                        send_cmt(ans.id);
                      }
                    }}
                  />
                  <Button
                    size="sm"
                    on:click={() => send_cmt(ans.id)}
                  >
                    등록
                  </Button>
                  <Button
                    size="sm"
                    variant="ghost"
                    on:click={() => {
                      show_cmt_form[ans.id] = false;
                      new_cmt[ans.id] = "";
                    }}
                  >
                    취소
                  </Button>
                </div>
              {/if}
            </div>
          </div>
        </Card>
      {/each}
    </div>

    <!-- 답변 작성 폼 -->
    <Card className="p-6">
      <h3 class="text-lg font-semibold mb-4">답변 작성</h3>
      {#if currentUser}
        <div class="space-y-4">
          <textarea
            bind:value={new_ans}
            placeholder="답변을 작성해주세요..."
            class="w-full h-32 p-3 border border-input rounded-md bg-background resize-none focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
          ></textarea>
          <div class="flex justify-end">
            <Button on:click={send_answer} disabled={sending_answer}>
              {sending_answer ? "등록 중..." : "답변 등록"}
            </Button>
          </div>
        </div>
      {:else}
        <div class="text-center py-8">
          <p class="text-muted-foreground mb-4">
            답변을 작성하려면 로그인이 필요합니다.
          </p>
          <Button on:click={() => go_to("login")}>로그인</Button>
        </div>
      {/if}
    </Card>
    {/if}
  </div>
</main>
