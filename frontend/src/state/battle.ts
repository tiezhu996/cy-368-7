import { ref, readonly } from "vue";

const pendingBattleCount = ref(0);

export function useBattleState() {
  function setPendingCount(count: number) {
    pendingBattleCount.value = count;
  }

  function decrementPendingCount() {
    if (pendingBattleCount.value > 0) {
      pendingBattleCount.value--;
    }
  }

  return {
    pendingBattleCount: readonly(pendingBattleCount),
    setPendingCount,
    decrementPendingCount,
  };
}
