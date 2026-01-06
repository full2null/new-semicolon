<script>
  // ui 컴포넌트들
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Input from "$lib/components/ui/Input.svelte";
  import { createEventDispatcher } from "svelte";
  import { login as loginAPI, get_me } from "$lib/api/auth.js";
  import { authStore } from "$lib/stores/auth.js";

  const dispatch = createEventDispatcher();

  // 입력값들
  let user_name = "";
  let pw = "";
  let is_loading = false;
  let err_msg = "";

  // 로그인 버튼 눌렀을때
  async function do_login() {
    if (!user_name || !pw) {
      err_msg = "사용자명과 비밀번호를 모두 입력해주세요.";
      return;
    }

    is_loading = true;
    err_msg = "";

    try {
      // 서버에 로그인 요청
      const token_res = await loginAPI(user_name, pw);
      const my_token = /** @type {any} */ (token_res).access_token;
      
      // 유저 정보 받아오기
      const user_res = await get_me(my_token);
      const user_info = /** @type {any} */ (user_res).data;

      // 스토어에 저장
      authStore.login(my_token, user_info);

      dispatch("login", user_info);
      dispatch("navigate", { page: "home" });
    } catch (err) {
      const err_text = /** @type {Error} */ (err).message;
      err_msg = err_text || "로그인에 실패했습니다. 사용자명과 비밀번호를 확인해주세요.";
    } finally {
      is_loading = false;
    }
  }

  // 회원가입 페이지로 이동
  function go_to_register() {
    dispatch("navigate", { page: "register" });
  }

  // 엔터치면 로그인 실행
  function on_key_press(event) {
    if (event?.key === "Enter") {
      do_login();
    }
  }
</script>

<div class="min-h-screen bg-background flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <!-- Logo and Title -->
    <div class="text-center mb-8">
      <div
        class="mx-auto w-12 h-12 bg-primary rounded-lg flex items-center justify-center mb-4"
      >
        <span class="text-primary-foreground font-bold text-xl">;</span>
      </div>
      <h1 class="text-2xl font-bold text-foreground">Semicolon에 로그인</h1>
      <p class="text-muted-foreground mt-2">개발자 커뮤니티에 참여하세요</p>
    </div>

    <Card className="p-6">
      <form on:submit|preventDefault={do_login} class="space-y-4">
        {#if err_msg}
          <div
            class="p-3 bg-destructive/10 border border-destructive/20 rounded-md"
          >
            <p class="text-sm text-destructive">{err_msg}</p>
          </div>
        {/if}

        <div class="space-y-2">
          <label for="username" class="text-sm font-medium text-foreground"
            >사용자명</label
          >
          <Input
            id="username"
            type="text"
            placeholder="사용자명을 입력하세요"
            bind:value={user_name}
            disabled={is_loading}
            on:keydown={on_key_press}
          />
        </div>

        <div class="space-y-2">
          <label for="password" class="text-sm font-medium text-foreground"
            >비밀번호</label
          >
          <Input
            id="password"
            type="password"
            placeholder="비밀번호를 입력하세요"
            bind:value={pw}
            disabled={is_loading}
            on:keydown={on_key_press}
          />
        </div>

        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center space-x-2">
            <input type="checkbox" class="rounded border-input" />
            <span class="text-muted-foreground">로그인 상태 유지</span>
          </label>
          <button type="button" class="text-primary hover:underline">
            비밀번호 찾기
          </button>
        </div>

        <Button type="submit" className="w-full" disabled={is_loading}>
          {is_loading ? "로그인 중..." : "로그인"}
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-muted-foreground">
          계정이 없으신가요?
          <button
            class="text-primary hover:underline font-medium"
            on:click={go_to_register}
          >
            회원가입
          </button>
        </p>
      </div>

      <!-- Divider -->
      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-border"></div>
        </div>
        <div class="relative flex justify-center text-xs uppercase">
          <span class="bg-background px-2 text-muted-foreground">또는</span>
        </div>
      </div>

      <!-- Social Login -->
      <div class="space-y-3">
        <Button variant="outline" className="w-full">
          <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Google로 로그인
        </Button>

        <Button variant="outline" className="w-full">
          <svg class="w-5 h-5 mr-2 fill-current" viewBox="0 0 24 24">
            <path
              d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"
            />
          </svg>
          GitHub으로 로그인
        </Button>
      </div>
    </Card>
  </div>
</div>
