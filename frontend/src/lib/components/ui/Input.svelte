<script>
  import { cn } from "$lib/utils.js";

  // input 타입
  export let type = "text";
  // 플레이스홀더
  export let placeholder = "";
  // 값
  export let value = "";
  // 추가 클래스
  export let className = "";
  // 비활성화
  export let disabled = false;

  $: input_class = cn("input", className);
</script>

<input
  class={input_class}
  {type}
  {placeholder}
  bind:value
  {disabled}
  on:input
  on:change
  on:focus
  on:blur
  {...$$restProps}
/>
