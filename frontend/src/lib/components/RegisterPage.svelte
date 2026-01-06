<script>
  // ui 컴포넌트들 가져오기
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Input from "$lib/components/ui/Input.svelte";
  import { createEventDispatcher } from "svelte";
  import { register as registerAPI, login as loginAPI, get_me } from "$lib/api/auth.js";
  import { authStore } from "$lib/stores/auth.js";

  const dispatch = createEventDispatcher();

  // 입력 폼 데이터 저장하는 변수
  let form_data = {
    username: "",
    email: "",
    password: "",
    confirm_pw: "",
    full_name: "",
  };
  let is_loading = false;
  /** @type {Record<string, string>} */
  let err_msg = {};

  // 입력값 체크하는 함수
  function check_form() {
    err_msg = {};

    // 유저네임 비어있는지 체크
    if (!form_data.username.trim()) {
      err_msg.username = "사용자명을 입력해주세요.";
    } else if (form_data.username.length < 3) {
      err_msg.username = "사용자명은 3자 이상이어야 합니다.";
    }

    // 이메일 체크
    if (!form_data.email.trim()) {
      err_msg.email = "이메일을 입력해주세요.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form_data.email)) {
      err_msg.email = "올바른 이메일 형식이 아닙니다.";
    }

    // 비번 체크
    if (!form_data.password) {
      err_msg.password = "비밀번호를 입력해주세요.";
    } else if (form_data.password.length < 8) {
      err_msg.password = "비밀번호는 8자 이상이어야 합니다.";
    }

    // 비번 확인 체크
    if (!form_data.confirm_pw) {
      err_msg.confirm_pw = "비밀번호 확인을 입력해주세요.";
    } else if (form_data.password !== form_data.confirm_pw) {
      err_msg.confirm_pw = "비밀번호가 일치하지 않습니다.";
    }

    return Object.keys(err_msg).length === 0;
  }

  // 회원가입 버튼 누르면 실행되는 함수
  async function do_register() {
    if (!check_form()) {
      return;
    }

    is_loading = true;

    try {
      // api 호출해서 가입 처리
      await registerAPI({
        username: form_data.username,
        email: form_data.email,
        password: form_data.password,
        full_name: form_data.full_name || form_data.username,
      });

      // 가입 완료되면 바로 로그인 시키기
      const token_res = await loginAPI(form_data.username, form_data.password);
      const my_token = /** @type {any} */ (token_res).access_token;
      const user_res = await get_me(my_token);
      const user_info = /** @type {any} */ (user_res).data;

      // 스토어에 저장해둠
      authStore.login(my_token, user_info);

      dispatch("login", user_info);
      dispatch("navigate", { page: "home" });
    } catch (err) {
      const err_text = /** @type {Error} */ (err).message;
      err_msg.general = err_text || "회원가입에 실패했습니다. 다시 시도해주세요.";
    } finally {
      is_loading = false;
    }
  }

  // 로그인 페이지 가기
  function go_to_login() {
    dispatch("navigate", { page: "login" });
  }

  // 엔터치면 제출
  function on_key_press(event) {
    if (event?.key === "Enter") {
      do_register();
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
      <h1 class="text-2xl font-bold text-foreground">Semicolon에 가입하기</h1>
      <p class="text-muted-foreground mt-2">
        개발자 커뮤니티의 일원이 되어보세요
      </p>
    </div>

    <Card className="p-6">
      <form on:submit|preventDefault={do_register} class="space-y-4">
        {#if err_msg.general}
          <div
            class="p-3 bg-destructive/10 border border-destructive/20 rounded-md"
          >
            <p class="text-sm text-destructive">{err_msg.general}</p>
          </div>
        {/if}

        <div class="space-y-2">
          <label for="username" class="text-sm font-medium text-foreground"
            >사용자명</label
          >
          <Input
            id="username"
            type="text"
            placeholder="사용자명을 입력하세요 (3자 이상)"
            bind:value={form_data.username}
            disabled={is_loading}
            className={err_msg.username ? "border-destructive" : ""}
            on:keydown={on_key_press}
          />
          {#if err_msg.username}
            <p class="text-sm text-destructive">{err_msg.username}</p>
          {/if}
        </div>

        <div class="space-y-2">
          <label for="email" class="text-sm font-medium text-foreground"
            >이메일</label
          >
          <Input
            id="email"
            type="email"
            placeholder="example@email.com"
            bind:value={form_data.email}
            disabled={is_loading}
            className={err_msg.email ? "border-destructive" : ""}
            on:keydown={on_key_press}
          />
          {#if err_msg.email}
            <p class="text-sm text-destructive">{err_msg.email}</p>
          {/if}
        </div>

        <div class="space-y-2">
          <label for="password" class="text-sm font-medium text-foreground"
            >비밀번호</label
          >
          <Input
            id="password"
            type="password"
            placeholder="8자 이상의 비밀번호"
            bind:value={form_data.password}
            disabled={is_loading}
            className={err_msg.password ? "border-destructive" : ""}
            on:keydown={on_key_press}
          />
          {#if err_msg.password}
            <p class="text-sm text-destructive">{err_msg.password}</p>
          {/if}
        </div>

        <div class="space-y-2">
          <label
            for="confirm_pw"
            class="text-sm font-medium text-foreground">비밀번호 확인</label
          >
          <Input
            id="confirm_pw"
            type="password"
            placeholder="비밀번호를 다시 입력하세요"
            bind:value={form_data.confirm_pw}
            disabled={is_loading}
            className={err_msg.confirm_pw ? "border-destructive" : ""}
            on:keydown={on_key_press}
          />
          {#if err_msg.confirm_pw}
            <p class="text-sm text-destructive">{err_msg.confirm_pw}</p>
          {/if}
        </div>

        <div class="flex items-start space-x-2">
          <input
            type="checkbox"
            id="terms"
            class="mt-1 rounded border-input"
            required
          />
          <label for="terms" class="text-sm text-muted-foreground">
            <a href="/terms" class="text-primary hover:underline">이용약관</a>과
            <a href="/privacy" class="text-primary hover:underline"
              >개인정보처리방침</a
            >에 동의합니다.
          </label>
        </div>

        <Button type="submit" className="w-full" disabled={is_loading}>
          {is_loading ? "가입 중..." : "회원가입"}
        </Button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-muted-foreground">
          이미 계정이 있으신가요?
          <button
            class="text-primary hover:underline font-medium"
            on:click={go_to_login}
          >
            로그인
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

      <!-- Social Registration -->
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
          Google로 가입
        </Button>

        <Button variant="outline" className="w-full">
          <svg class="w-5 h-5 mr-2 fill-current" viewBox="0 0 24 24">
            <path
              d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"
            />
          </svg>
          GitHub으로 가입
        </Button>
      </div>
    </Card>
  </div>
</div>
