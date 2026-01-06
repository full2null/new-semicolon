<script>
  import { cn } from "$lib/utils.js";

  // 배지 스타일
  export let variant = "default";
  // 추가 클래스
  export let className = "";

  // 스타일 맵
  const style_map = {
    default: "badge badge-primary",
    secondary: "badge badge-secondary",
    destructive: "badge bg-red-600 text-white",
    outline: "badge border-gray-300 bg-white text-gray-700",
  };

  $: badge_class = cn(style_map[variant], className);
</script>

<div class={badge_class} {...$$restProps}>
  <slot />
</div>
