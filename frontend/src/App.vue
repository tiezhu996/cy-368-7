<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { APP_CODE, APP_NAME } from "./constants/app";
import { REQUEST_MESSAGES } from "./constants/messages";
import { menuItems } from "./routes";
import { useBattleState } from "./state/battle";
import { fetchBattles } from "./api/client";

const route = useRoute();
const router = useRouter();
const { pendingBattleCount, setPendingCount } = useBattleState();

const activeMenu = computed(() => route.path);

function navigate(path: string) {
  router.push(path);
}

function goHealth() {
  window.location.href = REQUEST_MESSAGES.healthPath;
}

async function loadPendingCount() {
  try {
    const data = await fetchBattles();
    setPendingCount(data.pending_count);
  } catch {
    setPendingCount(2);
  }
}

onMounted(() => {
  loadPendingCount();
});
</script>

<template>
  <div class="app-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="brand-code">{{ APP_CODE }}</span>
        <h1 class="brand-title">{{ APP_NAME }}</h1>
      </div>
      <nav class="sidebar-nav">
        <div
          v-for="item in menuItems"
          :key="item.path"
          class="nav-item"
          :class="{ active: activeMenu === item.path }"
          @click="navigate(item.path)"
        >
          <span class="nav-label">{{ item.label }}</span>
          <el-badge
            v-if="item.path === '/battles' && pendingBattleCount > 0"
            :value="pendingBattleCount"
            class="nav-badge"
          />
        </div>
      </nav>
      <div class="sidebar-footer">
        <el-button type="primary" size="small" @click="goHealth">API Health</el-button>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--el-bg-color-page);
}

.sidebar {
  width: 240px;
  background: #1d2229;
  color: #f5f6f1;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-header {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header .brand-code {
  display: inline-block;
  font-size: 12px;
  color: #b84a37;
  font-weight: 700;
  letter-spacing: 2px;
  margin-bottom: 4px;
}

.sidebar-header .brand-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #f5f6f1;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: rgba(245, 246, 241, 0.7);
  font-size: 14px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #f5f6f1;
}

.nav-item.active {
  background: rgba(184, 74, 55, 0.2);
  color: #f5f6f1;
  font-weight: 500;
}

.nav-label {
  flex: 1;
}

.nav-badge {
  margin-left: 8px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  overflow-y: auto;
}
</style>
