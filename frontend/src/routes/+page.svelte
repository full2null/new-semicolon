<script>
  import Header from "$lib/components/Header.svelte";
  import Sidebar from "$lib/components/Sidebar.svelte";
  import HomePage from "$lib/components/HomePage.svelte";
  import QuestionList from "$lib/components/QuestionList.svelte";
  import QuestionDetail from "$lib/components/QuestionDetail.svelte";
  import QuestionForm from "$lib/components/QuestionForm.svelte";
  import TagsPage from "$lib/components/TagsPage.svelte";
  import GuidelinesPage from "$lib/components/GuidelinesPage.svelte";
  import HelpPage from "$lib/components/HelpPage.svelte";
  import LoginPage from "$lib/components/LoginPage.svelte";
  import RegisterPage from "$lib/components/RegisterPage.svelte";
  import ProfilePage from "$lib/components/ProfilePage.svelte";
  import { authStore } from "$lib/stores/auth.js";

  // 상태 변수들
  let cur_page = "home";
  let show_q_form = false;
  let sel_q_id = null;
  let cur_user = null;
  let sidebar_open = false;
  let search_query = undefined;

  // 스토어 구독
  authStore.subscribe(s => {
    cur_user = s.user;
  });

  // 페이지 이동
  function on_nav(e) {
    const { page, id, search } = e.detail;
    
    console.log("페이지 이동:", page, id, search);
    
    // 질문하기는 모달로
    if (page === "ask") {
      console.log("질문하기 모달 열기, show_q_form =", show_q_form);
      show_q_form = true;
      console.log("질문하기 모달 열림, show_q_form =", show_q_form);
      return;
    }
    
    cur_page = page;
    sel_q_id = id || null;
    search_query = search || undefined;
    sidebar_open = false;
  }

  // 질문 작성 완료
  function on_q_submit(e) {
    console.log("질문 작성 완료:", e.detail);
    show_q_form = false;
    cur_page = "questions";
  }

  // 질문 작성 취소
  function on_q_cancel() {
    show_q_form = false;
  }

  // 로그인
  function on_login(e) {
    cur_user = e.detail;
  }

  // 로그아웃
  function on_logout() {
    authStore.logout();
    cur_page = "home";
  }

  // 사이드바 토글
  function toggle_sidebar() {
    sidebar_open = !sidebar_open;
  }

  $: is_auth_page = cur_page === "login" || cur_page === "register";
</script>

<svelte:head>
  <title>Semicolon - 개발자 커뮤니티</title>
  <meta name="description" content="개발자들의 질문과 답변을 나누는 커뮤니티" />
</svelte:head>

{#if is_auth_page}
  {#if cur_page === "login"}
    <LoginPage on:navigate={on_nav} on:login={on_login} />
  {:else if cur_page === "register"}
    <RegisterPage on:navigate={on_nav} on:login={on_login} />
  {/if}
{:else}
  <div class="min-h-screen bg-background">
    <Header
      currentUser={cur_user}
      onToggleSidebar={toggle_sidebar}
      on:navigate={on_nav}
      on:logout={on_logout}
    />

    <div class="flex min-h-screen">
      <div
        class={`${sidebar_open ? "block" : "hidden"} md:block fixed md:relative z-40 md:z-auto`}
      >
        <!-- 모바일 오버레이 -->
        {#if sidebar_open}
          <div
            class="md:hidden fixed inset-0 bg-black/50"
            on:click={() => (sidebar_open = false)}
            on:keydown={(e) => e.key === "Escape" && (sidebar_open = false)}
            role="button"
            tabindex="0"
          ></div>
        {/if}
        <Sidebar currentPage={cur_page} on:navigate={on_nav} />
      </div>

      {#if cur_page === "home"}
        <HomePage on:navigate={on_nav} />
      {:else if cur_page === "questions"}
        <QuestionList searchQuery={search_query} on:navigate={on_nav} />
      {:else if cur_page === "question"}
        <QuestionDetail
          questionId={sel_q_id || "1"}
          currentUser={cur_user}
          on:navigate={on_nav}
        />
      {:else if cur_page === "tags"}
        <TagsPage on:navigate={on_nav} />
      {:else if cur_page === "guidelines"}
        <GuidelinesPage on:navigate={on_nav} />
      {:else if cur_page === "help"}
        <HelpPage on:navigate={on_nav} />
      {:else if cur_page === "profile"}
        <ProfilePage currentUser={cur_user} on:navigate={on_nav} />
      {:else}
        <HomePage on:navigate={on_nav} />
      {/if}
    </div>
  </div>
{/if}

<!-- 질문 작성 모달 -->
{#if show_q_form}
  <QuestionForm 
    on:submit={on_q_submit} 
    on:cancel={on_q_cancel} 
  />
{/if}
