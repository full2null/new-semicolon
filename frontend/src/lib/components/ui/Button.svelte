<script>
  import { cn } from "$lib/utils.js";

  // 버튼 스타일
  export let variant = "default";
  // 버튼 크기
  export let size = "default";
  // 추가 클래스
  export let className = "";
  // 비활성화 여부
  export let disabled = false;

  // 버튼 종류별 스타일
  const style_map = {
    default: "btn btn-primary",
    destructive: "btn bg-red-600 text-white hover:bg-red-700",
    outline: "btn btn-outline",
    secondary: "btn btn-secondary",
    ghost: "btn btn-ghost",
    link: "text-blue-600 hover:underline",
  };

  // 크기별 스타일
  const size_map = {
    default: "",
    sm: "btn-sm",
    lg: "btn-lg",
    icon: "w-10 h-10 p-2",
  };

  $: btn_class = cn(style_map[variant], size_map[size], className);
</script>

<button class={btn_class} {disabled} on:click {...$$restProps}>
  <slot />
</button>
