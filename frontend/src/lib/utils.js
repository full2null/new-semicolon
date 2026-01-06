// 클래스명 합쳐주는 함수
export function cn(...classes) {
  return classes.filter(Boolean).join(" ");
}
