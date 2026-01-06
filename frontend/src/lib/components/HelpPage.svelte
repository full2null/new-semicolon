<script>
  // svelte dispatcher 쓰기
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  const faq_list = [
    {
      category: "시작하기",
      questions: [
        {
          q: "Semicolon은 무엇인가요?",
          a: "Semicolon은 개발자들이 기술적인 질문과 답변을 공유하는 커뮤니티 플랫폼입니다. 프로그래밍, 개발 도구, 알고리즘 등 다양한 주제에 대해 토론할 수 있습니다.",
        },
        {
          q: "어떻게 회원가입하나요?",
          a: "우측 상단의 '회원가입' 버튼을 클릭하여 이메일과 비밀번호를 입력하면 간단하게 가입할 수 있습니다.",
        },
        {
          q: "무료로 이용할 수 있나요?",
          a: "네, Semicolon의 모든 기능은 완전 무료로 제공됩니다.",
        },
      ],
    },
    {
      category: "질문하기",
      questions: [
        {
          q: "어떻게 질문을 작성하나요?",
          a: "로그인 후 우측 상단의 '질문하기' 버튼을 클릭하세요. 제목, 본문, 관련 태그를 입력하고 게시하면 됩니다.",
        },
        {
          q: "질문을 수정하거나 삭제할 수 있나요?",
          a: "네, 본인이 작성한 질문은 언제든지 수정하거나 삭제할 수 있습니다. 질문 페이지에서 수정/삭제 버튼을 이용하세요.",
        },
        {
          q: "답변을 어떻게 채택하나요?",
          a: "본인의 질문에 달린 답변 중 가장 도움이 된 답변의 채택 버튼(체크 마크)을 클릭하세요.",
        },
      ],
    },
    {
      category: "답변하기",
      questions: [
        {
          q: "답변을 작성하려면 어떻게 해야 하나요?",
          a: "질문 페이지 하단의 답변 작성 영역에서 답변을 작성하고 '답변 게시' 버튼을 클릭하세요.",
        },
        {
          q: "답변에 코드를 포함할 수 있나요?",
          a: "네, 마크다운 문법을 사용하여 코드 블록을 작성할 수 있습니다. 백틱(```)을 사용하여 코드를 감싸주세요.",
        },
      ],
    },
    {
      category: "태그",
      questions: [
        {
          q: "태그는 무엇인가요?",
          a: "태그는 질문을 분류하는 키워드입니다. 프로그래밍 언어, 프레임워크, 주제 등을 나타냅니다.",
        },
        {
          q: "새로운 태그를 만들 수 있나요?",
          a: "네, 질문 작성 시 존재하지 않는 태그를 입력하면 자동으로 새로운 태그가 생성됩니다.",
        },
      ],
    },
  ];

  // 열림 상태
  /** @type {Record<string, boolean>} */
  let open = {};

  // 아코디언 토글
  function toggle_faq(cat_i, q_i) {
    const k = `${cat_i}-${q_i}`;
    open[k] = !open[k];
    open = open; // svelte 반응성 트리거
  }
</script>

<main class="flex-1 p-6 overflow-y-auto">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl font-bold mb-4">도움말</h1>
      <p class="text-lg text-muted-foreground">
        Semicolon 사용에 대한 자주 묻는 질문과 답변입니다.
      </p>
    </div>

    <!-- faq 섹션 -->
    <div class="space-y-6">
      {#each faq_list as cat, cat_i (cat.category)}
        <div class="p-6 bg-card rounded-lg border">
          <h2 class="text-2xl font-bold mb-4 flex items-center gap-2">
            <span class="w-2 h-8 bg-primary rounded"></span>
            {cat.category}
          </h2>
          <div class="space-y-3">
            {#each cat.questions as item, q_i (item.q)}
              {@const k = `${cat_i}-${q_i}`}
              <div class="p-4 bg-card rounded-lg border shadow-sm hover:border-primary/30 transition-colors">
                <button
                  class="w-full text-left group"
                  on:click={() => toggle_faq(cat_i, q_i)}
                >
                  <div class="flex items-start justify-between gap-4">
                    <h3 class="font-semibold group-hover:text-primary transition-colors flex items-center gap-2">
                      <svg
                        class="w-5 h-5 text-primary flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      {item.q}
                    </h3>
                    <svg
                      class="w-5 h-5 text-muted-foreground flex-shrink-0 transition-transform {open[k] ? 'rotate-180' : ''}"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </div>
                </button>
                {#if open[k]}
                  <div class="mt-3 pt-3 border-t text-muted-foreground leading-relaxed">
                    {item.a}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>

    <!-- 빠른 링크 -->
    <div class="mt-8 p-6 bg-card rounded-lg border">
      <h3 class="text-xl font-bold mb-4">빠른 링크</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <button
          class="p-4 bg-background rounded-lg border hover:border-primary transition-colors text-left group"
          on:click={() => dispatch("navigate", { page: "guidelines" })}
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold group-hover:text-primary transition-colors">커뮤니티 가이드라인</div>
              <div class="text-sm text-muted-foreground">규칙과 모범 사례</div>
            </div>
          </div>
        </button>
        <button
          class="p-4 bg-background rounded-lg border hover:border-primary transition-colors text-left group"
          on:click={() => dispatch("navigate", { page: "questions" })}
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold group-hover:text-primary transition-colors">질문 둘러보기</div>
              <div class="text-sm text-muted-foreground">다른 질문들 보기</div>
            </div>
          </div>
        </button>
        <button
          class="p-4 bg-background rounded-lg border hover:border-primary transition-colors text-left group"
          on:click={() => dispatch("navigate", { page: "tags" })}
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold group-hover:text-primary transition-colors">태그 탐색</div>
              <div class="text-sm text-muted-foreground">주제별로 찾기</div>
            </div>
          </div>
        </button>
        <button
          class="p-4 bg-background rounded-lg border hover:border-primary transition-colors text-left group"
          on:click={() => dispatch("navigate", { page: "users" })}
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center text-primary">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold group-hover:text-primary transition-colors">사용자 보기</div>
              <div class="text-sm text-muted-foreground">커뮤니티 멤버들</div>
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- 문의 섹션 -->
    <div class="mt-8 p-6 bg-primary/10 rounded-lg border border-primary">
      <h3 class="text-xl font-bold mb-3">답변을 찾지 못하셨나요?</h3>
      <p class="text-muted-foreground mb-4">
        추가 질문이 있으시면 커뮤니티에 질문을 올려주세요. 다른 사용자들이 도와드릴 것입니다.
      </p>
      <button
        class="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        on:click={() => dispatch("navigate", { page: "ask" })}
      >
        질문하러 가기
      </button>
    </div>
  </div>
</main>
