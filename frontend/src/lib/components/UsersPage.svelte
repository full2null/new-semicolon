<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  // 유저 데이터 (나중에 서버에서 받아올거임)
  const user_list = [
    {
      id: "1",
      name: "개발자123",
      email: "dev123@example.com",
      point: 1250,
      q_count: 45,
      a_count: 128,
      join_date: "2024. 3. 15.",
    },
    {
      id: "2",
      name: "프론트엔드러",
      email: "frontend@example.com",
      point: 2340,
      q_count: 67,
      a_count: 203,
      join_date: "2023. 11. 8.",
    },
    {
      id: "3",
      name: "타입마스터",
      email: "typemaster@example.com",
      point: 1890,
      q_count: 32,
      a_count: 165,
      join_date: "2024. 1. 22.",
    },
    {
      id: "4",
      name: "백엔드개발",
      email: "backend@example.com",
      point: 1540,
      q_count: 28,
      a_count: 142,
      join_date: "2024. 2. 10.",
    },
    {
      id: "5",
      name: "풀스택닌자",
      email: "fullstack@example.com",
      point: 3100,
      q_count: 89,
      a_count: 267,
      join_date: "2023. 8. 5.",
    },
    {
      id: "6",
      name: "리액트러버",
      email: "reactlover@example.com",
      point: 980,
      q_count: 21,
      a_count: 87,
      join_date: "2024. 5. 3.",
    },
  ];

  let search_word = "";
  let sort_type = "questions";

  // 검색하고 정렬하기
  $: filtered = user_list
    .filter((u) =>
      u.name.toLowerCase().includes(search_word.toLowerCase())
    )
    .sort((a, b) => {
      if (sort_type === "questions") return b.q_count - a.q_count;
      if (sort_type === "answers") return b.a_count - a.a_count;
      return 0;
    });
</script>

<main class="flex-1 p-6 overflow-y-auto">
  <div class="max-w-5xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl font-bold mb-4">사용자</h1>
      <p class="text-lg text-muted-foreground mb-6">
        우리 커뮤니티의 멤버들을 만나보세요.
      </p>

      <div class="flex flex-col md:flex-row gap-4 mb-6">
        <!-- 검색바 -->
        <input
          type="text"
          bind:value={search_word}
          placeholder="사용자 검색..."
          class="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        />

        <!-- 정렬 옵션 -->
        <select
          bind:value={sort_type}
          class="px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="questions">질문 수 순</option>
          <option value="answers">답변 수 순</option>
        </select>
      </div>
    </div>

    <!-- 유저 그리드 -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#each filtered as u (u.id)}
        <div class="user-card p-6 bg-card rounded-lg border hover:border-primary transition-all">
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                <span class="text-xl font-bold text-primary">
                  {u.name[0]}
                </span>
              </div>
              <div>
                <h3 class="text-lg font-semibold">{u.name}</h3>
                <p class="text-sm text-muted-foreground">{u.email}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4 pt-4 border-t">
            <div class="text-center">
              <div class="text-lg font-semibold">{u.q_count}</div>
              <div class="text-xs text-muted-foreground">질문</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-semibold">{u.a_count}</div>
              <div class="text-xs text-muted-foreground">답변</div>
            </div>
            <div class="text-center">
              <div class="text-xs text-muted-foreground mt-2">
                가입일<br />{u.join_date}
              </div>
            </div>
          </div>
        </div>
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
  .user-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
</style>
