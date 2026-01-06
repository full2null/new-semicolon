<script>
  import Card from "$lib/components/ui/Card.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Input from "$lib/components/ui/Input.svelte";
  import { onMount } from "svelte";
  import { get_me, update_me, get_me_stats } from "$lib/api/users.js";
  import { ApiError } from "$lib/api/client.js";
  import { authStore } from "$lib/stores/auth.js";
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  /**
   * @typedef {Object} User
   * @property {number} id
   * @property {string} username
   * @property {string} email
   * @property {string} [full_name]
   */

  /** @type {User | null} */
  export let currentUser = null;

  let loading = false;
  let error = null;
  let success_msg = null;
  let stats = { question_count: 0, answer_count: 0 };
  let loading_stats = false;

  // 폼 데이터
  let form_data = {
    username: "",
    email: "",
    full_name: "",
    current_password: "",
    new_password: "",
    confirm_password: "",
  };

  // 사용자 정보 로드
  async function load_user_info() {
    if (currentUser) {
      form_data.username = currentUser.username || "";
      form_data.email = currentUser.email || "";
      form_data.full_name = currentUser.full_name || "";
    }
  }

  // 통계 로드
  async function load_stats() {
    try {
      loading_stats = true;
      stats = await get_me_stats();
      console.log("[DEBUG] 로드된 통계:", stats);
    } catch (err) {
      console.error("통계 로드 실패:", err);
    } finally {
      loading_stats = false;
    }
  }

  // 프로필 업데이트
  async function handle_submit(e) {
    e.preventDefault();
    error = null;
    success_msg = null;

    // 비밀번호 확인
    if (form_data.new_password) {
      if (form_data.new_password !== form_data.confirm_password) {
        error = "새 비밀번호가 일치하지 않습니다.";
        return;
      }
      if (form_data.new_password.length < 8) {
        error = "비밀번호는 8자 이상이어야 합니다.";
        return;
      }
    }

    try {
      loading = true;

      const update_data = {
        username: form_data.username,
        email: form_data.email,
        full_name: form_data.full_name || undefined,
      };

      // 비밀번호 변경이 있으면 추가
      if (form_data.new_password) {
        update_data.password = form_data.new_password;
        console.log("[DEBUG] 비밀번호 변경 포함");
      }

      console.log("[DEBUG] 전송할 데이터:", update_data);
      const updated_user = await update_me(update_data);
      console.log("[DEBUG] 업데이트된 사용자:", updated_user);
      
      // authStore 업데이트
      authStore.update_user(updated_user);
      currentUser = updated_user;
      
      success_msg = "프로필이 업데이트되었습니다.";
      
      // 비밀번호 필드 초기화
      form_data.current_password = "";
      form_data.new_password = "";
      form_data.confirm_password = "";

      // 성공 메시지 3초 후 제거
      setTimeout(() => {
        success_msg = null;
      }, 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        error = err.data?.message || err.message;
      } else {
        error = "프로필 업데이트에 실패했습니다.";
      }
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    console.log("[DEBUG] ProfilePage mounted, currentUser:", currentUser);
    load_user_info();
    load_stats();
  });
</script>

<div class="container mx-auto p-6 max-w-4xl">
  <h1 class="text-3xl font-bold mb-6">내 프로필</h1>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- 왼쪽: 프로필 정보 -->
    <div class="md:col-span-2">
      <Card className="p-6">
        <h2 class="text-xl font-semibold mb-4">프로필 정보</h2>

        {#if error}
          <div class="bg-destructive/10 text-destructive px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        {/if}

        {#if success_msg}
          <div class="bg-green-500/10 text-green-600 px-4 py-3 rounded-lg mb-4">
            {success_msg}
          </div>
        {/if}

        <form on:submit={handle_submit} class="space-y-4">
          <!-- 사용자명 -->
          <div>
            <label for="username" class="block text-sm font-medium mb-2">
              사용자명 *
            </label>
            <Input
              id="username"
              type="text"
              bind:value={form_data.username}
              required
              disabled={loading}
            />
          </div>

          <!-- 이메일 -->
          <div>
            <label for="email" class="block text-sm font-medium mb-2">
              이메일 *
            </label>
            <Input
              id="email"
              type="email"
              bind:value={form_data.email}
              required
              disabled={loading}
            />
          </div>

          <!-- 전체 이름 -->
          <div>
            <label for="full_name" class="block text-sm font-medium mb-2">
              전체 이름 (선택)
            </label>
            <Input
              id="full_name"
              type="text"
              bind:value={form_data.full_name}
              disabled={loading}
            />
          </div>

          <hr class="my-6" />

          <h3 class="text-lg font-semibold mb-3">비밀번호 변경</h3>
          <p class="text-sm text-muted-foreground mb-4">
            비밀번호를 변경하려면 아래 필드를 입력하세요.
          </p>

          <!-- 새 비밀번호 -->
          <div>
            <label for="new_password" class="block text-sm font-medium mb-2">
              새 비밀번호
            </label>
            <Input
              id="new_password"
              type="password"
              bind:value={form_data.new_password}
              placeholder="최소 8자 이상"
              disabled={loading}
            />
          </div>

          <!-- 비밀번호 확인 -->
          <div>
            <label for="confirm_password" class="block text-sm font-medium mb-2">
              비밀번호 확인
            </label>
            <Input
              id="confirm_password"
              type="password"
              bind:value={form_data.confirm_password}
              placeholder="새 비밀번호를 다시 입력하세요"
              disabled={loading}
            />
          </div>

          <div class="flex justify-end pt-4">
            <Button type="submit" disabled={loading}>
              {loading ? "업데이트 중..." : "프로필 업데이트"}
            </Button>
          </div>
        </form>
      </Card>
    </div>

    <!-- 오른쪽: 활동 통계 -->
    <div>
      <Card className="p-6">
        <h2 class="text-xl font-semibold mb-4">활동 통계</h2>
        
        {#if loading_stats}
          <div class="text-center text-muted-foreground py-4">
            로딩 중...
          </div>
        {:else}
          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-muted-foreground">작성한 질문</div>
                  <div class="text-2xl font-bold">{stats.question_count}</div>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-green-500/10 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-muted-foreground">작성한 답변</div>
                  <div class="text-2xl font-bold">{stats.answer_count}</div>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between p-3 bg-muted rounded-lg">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-500/10 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-muted-foreground">총 기여</div>
                  <div class="text-2xl font-bold">{stats.question_count + stats.answer_count}</div>
                </div>
              </div>
            </div>
          </div>
        {/if}
      </Card>
    </div>
  </div>
</div>
