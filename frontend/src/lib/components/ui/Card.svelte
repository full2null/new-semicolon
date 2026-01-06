<script>
  import { cn } from "$lib/utils.js";

  // 추가 클래스
  export let className = "";

  $: card_class = cn("card", className);
</script>

<div class={card_class} {...$$restProps}>
  <slot />
</div>
