<script>
  import Button from "$lib/components/ui/Button.svelte";
  import Input from "$lib/components/ui/Input.svelte";
  import Badge from "$lib/components/ui/Badge.svelte";
  import { createEventDispatcher } from "svelte";

  /**
   * @typedef {Object} User
   * @property {number} id - 사용자 ID
   * @property {string} username - 사용자명
   * @property {string} email - 이메일
   * @property {string} [full_name] - 전체 이름
   * @property {boolean} is_active - 활성 상태
   */

  /** @type {User | null} */
  export let currentUser = null;
  /** @type {() => void} */
  export let onToggleSidebar = () => {};

  const dispatch = createEventDispatcher();

  // 페이지 이동
  function go_to_page(page) {
    dispatch("navigate", { page });
  }

  // 로그아웃
  function do_logout() {
    dispatch("logout");
  }

  let search_text = "";
  let show_menu = false;

  // 검색 제출
  function handle_search(e) {
    e.preventDefault();
    if (search_text.trim()) {
      dispatch("navigate", { page: "questions", search: search_text.trim() });
    }
  }

  // 메뉴 토글
  function toggle_menu() {
    show_menu = !show_menu;
  }

  // 바깥 클릭시 메뉴 닫기
  function on_click_outside(e) {
    if (show_menu && !e.target.closest('.user-menu-container')) {
      show_menu = false;
    }
  }
</script>

<svelte:window on:click={on_click_outside} />

<header class="border-b bg-background sticky top-0 z-50">
  <div class="container mx-auto px-4 py-3">
    <div class="flex items-center justify-between gap-4">
      <!-- 모바일 메뉴 & 로고 -->
      <div class="flex items-center space-x-2">
        <Button
          variant="ghost"
          size="sm"
          className="md:hidden"
          on:click={onToggleSidebar}
        >
          <!-- 메뉴 아이콘 -->
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </Button>
        <div
          class="flex items-center space-x-3 cursor-pointer"
          on:click={() => go_to_page("home")}
          on:keydown={(e) => e.key === "Enter" && go_to_page("home")}
          role="button"
          tabindex="0"
        >
          <!-- Logo placeholder -->
          <div
            class="h-8 w-8 bg-primary rounded flex items-center justify-center text-primary-foreground font-bold"
          >
            ;
          </div>
          <span class="font-bold text-lg whitespace-nowrap">Semicolon</span>
        </div>
      </div>

      <!-- 검색바 -->
      <div class="max-w-md w-full hidden md:block">
        <form on:submit={handle_search} class="relative">
          <Input
            type="search"
            placeholder="질문 검색..."
            className="pr-10"
            bind:value={search_text}
          />
          <button
            type="submit"
            class="absolute right-3 top-1/2 transform -translate-y-1/2"
            aria-label="검색"
          >
            <svg
              class="text-muted-foreground w-4 h-4 hover:text-foreground"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </button>
        </form>
      </div>

      <!-- 네비게이션 & 유저 버튼들 -->
      <div class="flex items-center space-x-2 sm:space-x-4">
        {#if currentUser}
          <div class="relative user-menu-container">
            <div
              class="flex items-center space-x-2 cursor-pointer hover:bg-accent rounded-lg p-2"
              on:click={toggle_menu}
              on:keydown={(e) => e.key === "Enter" && toggle_menu()}
              role="button"
              tabindex="0"
            >
              <div
                class="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center"
              >
                <!-- User Icon -->
                <svg
                  class="w-4 h-4 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <div class="text-sm hidden sm:block">
                <div class="font-medium">{currentUser.full_name || currentUser.username}</div>
                <div class="text-muted-foreground text-xs">
                  @{currentUser.username}
                </div>
              </div>
            </div>

            <!-- 유저 드롭다운 메뉴 -->
            {#if show_menu}
              <div class="absolute right-0 mt-2 w-56 bg-background border border-border rounded-lg shadow-lg py-2 z-50">
                <button
                  class="w-full text-left px-4 py-2 hover:bg-accent flex items-center space-x-2"
                  on:click={() => { go_to_page("profile"); show_menu = false; }}
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>내 프로필</span>
                </button>
                <hr class="my-2 border-border" />
                <button
                  class="w-full text-left px-4 py-2 hover:bg-accent text-destructive flex items-center space-x-2"
                  on:click={() => { do_logout(); show_menu = false; }}
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>로그아웃</span>
                </button>
              </div>
            {/if}
          </div>
        {:else}
          <Button
            variant="ghost"
            size="sm"
            on:click={() => go_to_page("login")}
            className="hidden sm:inline-flex"
          >
            로그인
          </Button>
          <Button
            variant="default"
            size="sm"
            on:click={() => go_to_page("register")}
          >
            <span class="hidden sm:inline">회원가입</span>
            <span class="sm:hidden">가입</span>
          </Button>
        {/if}
      </div>
    </div>
  </div>
</header>
