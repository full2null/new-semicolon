<script>
  // svelte dispatcher 쓰기
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  const guide_list = [
    {
      title: "질문하기 전에",
      items: [
        "검색을 통해 이미 비슷한 질문이 있는지 확인하세요",
        "문제를 명확하고 구체적으로 설명하세요",
        "최소한의 재현 가능한 예제를 제공하세요",
        "시도해본 방법들을 공유하세요",
      ],
    },
    {
      title: "좋은 질문 작성하기",
      items: [
        "제목은 문제를 잘 설명하는 간결한 제목으로 작성하세요",
        "문제 상황, 기대하는 결과, 실제 결과를 명확히 구분하세요",
        "관련 코드는 코드 블록으로 포맷팅하세요",
        "에러 메시지가 있다면 전체 내용을 포함하세요",
        "관련 태그를 적절히 추가하세요",
      ],
    },
    {
      title: "답변하기",
      items: [
        "질문을 정확히 이해했는지 확인하세요",
        "구체적이고 실행 가능한 해결책을 제시하세요",
        "코드 예제를 포함하면 더 좋습니다",
        "다른 답변과 중복되지 않는지 확인하세요",
        "예의 바르고 건설적인 태도를 유지하세요",
      ],
    },
    {
      title: "커뮤니티 규칙",
      items: [
        "모든 구성원을 존중하세요",
        "비방, 욕설, 차별적 표현을 사용하지 마세요",
        "스팸이나 광고를 게시하지 마세요",
        "개인정보를 공유하지 마세요",
        "저작권을 존중하세요",
      ],
    },
  ];
</script>

<main class="flex-1 p-6 overflow-y-auto">
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl font-bold mb-4">커뮤니티 가이드라인</h1>
      <p class="text-lg text-muted-foreground">
        Semicolon 커뮤니티를 더 나은 곳으로 만들기 위한 가이드라인입니다.
      </p>
    </div>

    <!-- 가이드 목록 -->
    <div class="space-y-6">
      {#each guide_list as sec (sec.title)}
        <div class="p-6 bg-card rounded-lg border">
          <h2 class="text-2xl font-bold mb-4 flex items-center gap-2">
            <span class="w-2 h-8 bg-primary rounded"></span>
            {sec.title}
          </h2>
          <ul class="space-y-3">
            {#each sec.items as txt}
              <li class="flex items-start gap-3">
                <svg
                  class="w-5 h-5 text-primary mt-0.5 flex-shrink-0"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <span class="text-base">{txt}</span>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>

    <div class="mt-8 p-6 bg-primary/10 rounded-lg border border-primary">
      <h3 class="text-xl font-bold mb-3">문제가 있나요?</h3>
      <p class="text-muted-foreground mb-4">
        가이드라인을 위반하는 콘텐츠를 발견하셨다면 신고해주세요.
        커뮤니티 관리자가 검토 후 적절한 조치를 취하겠습니다.
      </p>
      <button
        class="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        on:click={() => dispatch("navigate", { page: "help" })}
      >
        도움말 보기
      </button>
    </div>
  </div>
</main>
