<script setup lang="ts">
import { onMounted, ref, computed, watch } from "vue";
import { fetchOverview } from "../api/client";
import { REQUEST_MESSAGES } from "../constants/messages";
import { createFallbackOverview } from "../state/dashboard";
import { useBattleState } from "../state/battle";
import type { OverviewResponse } from "../types";
import FeatureStrip from "../components/FeatureStrip.vue";
import MetricGrid from "../components/MetricGrid.vue";
import OperationsTable from "../components/OperationsTable.vue";

const { pendingBattleCount } = useBattleState();

const overview = ref<OverviewResponse>(createFallbackOverview());
const notice = ref(REQUEST_MESSAGES.overviewFallback);

const mergedKpis = computed(() => {
  const kpis = [...overview.value.kpis];
  const pendingIndex = kpis.findIndex((k) => k.label === "待处理");
  if (pendingIndex !== -1 && pendingBattleCount.value > 0) {
    kpis[pendingIndex] = {
      ...kpis[pendingIndex],
      value: String(pendingBattleCount.value),
    };
  }
  return kpis;
});

watch(
  () => pendingBattleCount.value,
  (newVal) => {
    const pendingIndex = overview.value.kpis.findIndex((k) => k.label === "待处理");
    if (pendingIndex !== -1) {
      overview.value.kpis[pendingIndex].value = String(newVal);
    }
  }
);

onMounted(async () => {
  try {
    overview.value = await fetchOverview();
    notice.value = "后端服务已联通，当前展示实时接口数据。";
  } catch {
    notice.value = REQUEST_MESSAGES.overviewFallback;
  }
});
</script>

<template>
  <main class="overview-page">
    <section class="workspace">
      <div class="lead-grid">
        <article class="hero-panel">
          <span class="pill">{{ notice }}</span>
          <h2>{{ overview.appName }}</h2>
          <p>{{ overview.description }}</p>
        </article>
        <MetricGrid :items="mergedKpis" />
      </div>
      <FeatureStrip :items="overview.features" />
      <section class="work-panel">
        <h2>运营任务流</h2>
        <OperationsTable :records="overview.records" />
      </section>
    </section>
  </main>
</template>

<style scoped>
.overview-page {
  min-height: 100vh;
}

.workspace {
  width: min(1180px, calc(100vw - 32px));
  margin: 0 auto;
  padding: clamp(24px, 5vw, 56px) 0 64px;
}

.lead-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
  gap: clamp(18px, 3vw, 32px);
}

.hero-panel,
.work-panel {
  border: 1px solid color-mix(in srgb, #1d2229 13%, transparent);
  background: color-mix(in srgb, #f5f6f1 86%, white 14%);
  box-shadow: 0 18px 50px color-mix(in srgb, #1d2229 10%, transparent);
  border-radius: 8px;
  padding: clamp(22px, 4vw, 42px);
}

.hero-panel p {
  color: color-mix(in srgb, #1d2229 72%, #546a7b 28%);
  font-size: clamp(16px, 2vw, 19px);
  line-height: 1.8;
}

.pill {
  display: inline-flex;
  border-radius: 999px;
  padding: 6px 12px;
  background: color-mix(in srgb, #546a7b 14%, transparent);
  color: #1d2229;
  font-weight: 700;
}

.work-panel {
  margin-top: 26px;
}

@media (max-width: 860px) {
  .lead-grid {
    grid-template-columns: 1fr;
  }
}
</style>
