<script>
  import Badge from "$lib/components/ui/Badge.svelte";
  import { createEventDispatcher } from "svelte";

  // 질문 데이터 타입
  /**
   * @typedef {Object} Author
   * @property {number} id
   * @property {string} username
   * @property {string} email
   * @property {string} [full_name]
   */

  /**
   * @typedef {Object} Question
   * @property {number} id
   * @property {string} title
   * @property {string} content
   * @property {Author|string} author - Author 객체 또는 username 문자열
   * @property {string} created_at
   * @property {number} views
   * @property {number} [answers_count] - 답변 수
   * @property {Array} [answers] - 답변 배열
   * @property {number} [votes]
   * @property {Array<string>} [tags]
   * @property {boolean} [hasAcceptedAnswer]
   * @property {boolean} [is_solved]
   */

  /** @type {Question} */
  export let question;

  const dispatch = createEventDispatcher();

  // 질문 클릭하면 상세페이지로
  function on_click() {
    dispatch("navigate", { page: "question", id: question.id });
  }

  // 시간 포맷 변환 (몇시간 전, 며칠 전 이런식으로)
  function parse_date(date_str) {
    if (!date_str) return new Date();
    // 서버에서 TZ가 빠진 경우 UTC로 해석하도록 보정
    const has_tz = /Z|[+-]\d{2}:?\d{2}$/.test(date_str);
    const iso = has_tz ? date_str : `${date_str}Z`;
    return new Date(iso);
  }

  function get_time_text(date_str) {
    const date = parse_date(date_str);
    const now = new Date();
    const diff_hours = Math.floor(
      (now.getTime() - date.getTime()) / (1000 * 60 * 60),
    );

    if (diff_hours < 1) return "방금 전";
    if (diff_hours < 24) return `${diff_hours}시간 전`;
    if (diff_hours < 168) return `${Math.floor(diff_hours / 24)}일 전`;
    return date.toLocaleDateString("ko-KR");
  }

  // author가 객체인지 문자열인지 확인
  $: author_name = typeof question.author === 'string' 
    ? question.author 
    : question.author?.username || '익명';
  
  // 답변 개수
  $: answers_count = question.answers_count || question.answers?.length || 0;
  
  // 태그 배열
  $: tags = question.tags || [];
  
  // 채택된 답변 여부
  $: has_accepted = question.hasAcceptedAnswer || question.is_solved || false;
  
  // 생성 시간 (createdAt 또는 created_at)
  $: created_time = question.createdAt || question.created_at;
</script>

<div
  class="p-4 hover:shadow-md transition-shadow cursor-pointer bg-card border rounded-lg"
  on:click={on_click}
  on:keydown={(e) => e.key === 'Enter' && on_click()}
  role="button"
  tabindex="0"
>
  <div class="flex items-start space-x-4">
    <!-- Stats Column -->
    <div
      class="flex flex-col items-center space-y-2 text-sm text-muted-foreground min-w-[60px]"
    >
      <div class="text-center">
        <div
          class={`font-medium ${has_accepted ? "text-green-600" : "text-foreground"}`}
        >
          {answers_count}
        </div>
        <div>답변</div>
      </div>
    </div>

    <!-- Content Column -->
    <div class="flex-1 min-w-0">
      <h3 class="text-lg font-medium text-foreground mb-2 line-clamp-2">
        {question.title}
      </h3>
      <p class="text-muted-foreground text-sm mb-3 line-clamp-2">
        {question.content}
      </p>

      <!-- Tags -->
      <div class="flex flex-wrap gap-1 mb-3">
        {#each tags as tag (tag)}
          <Badge
            variant="secondary"
            className="text-xs bg-blue-100 text-blue-800"
          >
            {tag}
          </Badge>
        {/each}
      </div>

      <!-- Author and Time -->
      <div
        class="flex items-center justify-between text-xs text-muted-foreground"
      >
        <div class="flex items-center space-x-2">
          <div
            class="w-6 h-6 bg-primary/10 rounded-full flex items-center justify-center"
          >
            <span class="text-xs font-medium text-primary">
              {author_name.charAt(0).toUpperCase()}
            </span>
          </div>
          <span>{author_name}</span>
        </div>
        <span>{get_time_text(created_time)}</span>
      </div>
    </div>
  </div>
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
