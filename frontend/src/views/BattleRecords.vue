<script setup lang="ts">
import { onMounted, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { fetchBattles, confirmBattle, cancelBattle } from "../api/client";
import { useBattleState } from "../state/battle";
import type { BattleChallenge, BattleListResponse } from "../types";

const { setPendingCount, decrementPendingCount } = useBattleState();

const battleData = ref<BattleListResponse>({
  pending: [],
  confirmed: [],
  pending_count: 0,
});

const loading = ref(false);
const activeTab = ref("pending");

async function loadBattles() {
  loading.value = true;
  try {
    battleData.value = await fetchBattles();
    setPendingCount(battleData.value.pending_count);
  } catch (e) {
    battleData.value = {
      pending: [
        {
          id: 1,
          challenger_team: { id: 1, name: "野狼突击队", leader_name: "张队长", member_count: 8 },
          challenged_team: { id: 2, name: "猎豹特战队", leader_name: "李队长", member_count: 10 },
          venue_name: "丛林战场A区",
          battle_time: "2026-06-10T14:00:00",
          status: "pending",
          message: "约战本周末下午场，5v5标准赛",
          created_at: "2026-06-05T10:00:00",
          updated_at: "2026-06-05T10:00:00",
        },
        {
          id: 2,
          challenger_team: { id: 3, name: "猛虎连", leader_name: "王队长", member_count: 7 },
          challenged_team: { id: 1, name: "野狼突击队", leader_name: "张队长", member_count: 8 },
          venue_name: "城市巷战CQB",
          battle_time: "2026-06-08T10:00:00",
          status: "pending",
          message: "请求友谊赛，新队员练手",
          created_at: "2026-06-04T15:30:00",
          updated_at: "2026-06-04T15:30:00",
        },
      ],
      confirmed: [
        {
          id: 3,
          challenger_team: { id: 2, name: "猎豹特战队", leader_name: "李队长", member_count: 10 },
          challenged_team: { id: 4, name: "幽灵小队", leader_name: "赵队长", member_count: 6 },
          venue_name: "废墟战场B区",
          battle_time: "2026-06-05T09:00:00",
          status: "confirmed",
          message: "已确认，周六上午见",
          created_at: "2026-06-01T09:00:00",
          updated_at: "2026-06-02T11:00:00",
        },
        {
          id: 4,
          challenger_team: { id: 4, name: "幽灵小队", leader_name: "赵队长", member_count: 6 },
          challenged_team: { id: 3, name: "猛虎连", leader_name: "王队长", member_count: 7 },
          venue_name: "夜间战场D区",
          battle_time: "2026-06-12T20:00:00",
          status: "confirmed",
          message: "夜战模式，装备自备",
          created_at: "2026-06-03T18:00:00",
          updated_at: "2026-06-03T20:00:00",
        },
      ],
      pending_count: 2,
    };
    setPendingCount(2);
  } finally {
    loading.value = false;
  }
}

function formatDateTime(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

async function handleConfirm(challenge: BattleChallenge) {
  try {
    await ElMessageBox.confirm(
      `确定要接受「${challenge.challenger_team.name}」的约战挑战吗？\n对战时间：${formatDateTime(challenge.battle_time)}\n场地：${challenge.venue_name}`,
      "确认应战",
      {
        confirmButtonText: "确认应战",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await confirmBattle(challenge.id);
    decrementPendingCount();
    ElMessage.success("已确认应战");
    loadBattles();
  } catch (e: any) {
    if (e !== "cancel") {
      ElMessage.error(e.message || "操作失败");
    }
  }
}

async function handleCancel(challenge: BattleChallenge) {
  try {
    await ElMessageBox.confirm(
      `确定要取消这场约战吗？\n「${challenge.challenger_team.name}」 vs 「${challenge.challenged_team.name}」`,
      "取消约战",
      {
        confirmButtonText: "确定取消",
        cancelButtonText: "保留",
        type: "error",
      }
    );
    await cancelBattle(challenge.id);
    if (challenge.status === "pending") {
      decrementPendingCount();
    }
    ElMessage.success("已取消约战");
    loadBattles();
  } catch (e: any) {
    if (e !== "cancel") {
      ElMessage.error(e.message || "操作失败");
    }
  }
}

function getStatusTag(status: string) {
  const map: Record<string, { type: string; text: string }> = {
    pending: { type: "warning", text: "待确认" },
    confirmed: { type: "success", text: "已生效" },
    cancelled: { type: "info", text: "已取消" },
  };
  return map[status] || { type: "info", text: status };
}

onMounted(() => {
  loadBattles();
});
</script>

<template>
  <div class="battle-records">
    <div class="page-header">
      <h2>约战记录</h2>
      <p class="subtitle">跟踪和管理所有战队约战状态，队长可在此确认或取消对战</p>
    </div>

    <el-tabs v-model="activeTab" class="battle-tabs">
      <el-tab-pane label="待确认" name="pending">
        <template #label>
          <span>待确认</span>
          <el-badge v-if="battleData.pending.length > 0" :value="battleData.pending.length" class="badge" />
        </template>
        <div v-loading="loading" class="battle-list">
          <el-empty v-if="battleData.pending.length === 0" description="暂无待确认的约战" />
          <el-card
            v-for="item in battleData.pending"
            :key="item.id"
            class="battle-card"
            shadow="hover"
          >
            <div class="card-header">
              <div class="teams">
                <span class="team-name challenger">{{ item.challenger_team.name }}</span>
                <span class="vs">VS</span>
                <span class="team-name challenged">{{ item.challenged_team.name }}</span>
              </div>
              <el-tag :type="getStatusTag(item.status).type" effect="light">
                {{ getStatusTag(item.status).text }}
              </el-tag>
            </div>
            <div class="card-body">
              <div class="info-row">
                <span class="label">发起方</span>
                <span class="value">{{ item.challenger_team.leader_name }} ({{ item.challenger_team.member_count }}人)</span>
              </div>
              <div class="info-row">
                <span class="label">应战方</span>
                <span class="value">{{ item.challenged_team.leader_name }} ({{ item.challenged_team.member_count }}人)</span>
              </div>
              <div class="info-row">
                <span class="label">对战场地</span>
                <span class="value">{{ item.venue_name }}</span>
              </div>
              <div class="info-row">
                <span class="label">对战时间</span>
                <span class="value highlight">{{ formatDateTime(item.battle_time) }}</span>
              </div>
              <div v-if="item.message" class="info-row message">
                <span class="label">留言</span>
                <span class="value">{{ item.message }}</span>
              </div>
            </div>
            <div class="card-footer">
              <span class="created-at">发起于 {{ formatDateTime(item.created_at) }}</span>
              <div class="actions">
                <el-button type="danger" plain size="small" @click="handleCancel(item)">
                  取消约战
                </el-button>
                <el-button type="primary" size="small" @click="handleConfirm(item)">
                  确认应战
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="已生效" name="confirmed">
        <div v-loading="loading" class="battle-list">
          <el-empty v-if="battleData.confirmed.length === 0" description="暂无已生效的约战" />
          <el-card
            v-for="item in battleData.confirmed"
            :key="item.id"
            class="battle-card"
            shadow="hover"
          >
            <div class="card-header">
              <div class="teams">
                <span class="team-name challenger">{{ item.challenger_team.name }}</span>
                <span class="vs">VS</span>
                <span class="team-name challenged">{{ item.challenged_team.name }}</span>
              </div>
              <el-tag :type="getStatusTag(item.status).type" effect="light">
                {{ getStatusTag(item.status).text }}
              </el-tag>
            </div>
            <div class="card-body">
              <div class="info-row">
                <span class="label">发起方</span>
                <span class="value">{{ item.challenger_team.leader_name }} ({{ item.challenger_team.member_count }}人)</span>
              </div>
              <div class="info-row">
                <span class="label">应战方</span>
                <span class="value">{{ item.challenged_team.leader_name }} ({{ item.challenged_team.member_count }}人)</span>
              </div>
              <div class="info-row">
                <span class="label">对战场地</span>
                <span class="value">{{ item.venue_name }}</span>
              </div>
              <div class="info-row">
                <span class="label">对战时间</span>
                <span class="value highlight">{{ formatDateTime(item.battle_time) }}</span>
              </div>
              <div v-if="item.message" class="info-row message">
                <span class="label">留言</span>
                <span class="value">{{ item.message }}</span>
              </div>
            </div>
            <div class="card-footer">
              <span class="created-at">确认于 {{ formatDateTime(item.updated_at) }}</span>
              <div class="actions">
                <el-button type="danger" plain size="small" @click="handleCancel(item)">
                  取消对战
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.battle-records {
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.subtitle {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.battle-tabs {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
}

.battle-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 300px;
}

.battle-card {
  border-radius: 8px;
}

.battle-card :deep(.el-card__body) {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.teams {
  display: flex;
  align-items: center;
  gap: 12px;
}

.team-name {
  font-size: 18px;
  font-weight: 600;
}

.team-name.challenger {
  color: #b84a37;
}

.team-name.challenged {
  color: #546a7b;
}

.vs {
  font-size: 14px;
  font-weight: 700;
  color: var(--el-text-color-secondary);
  background: var(--el-fill-color-light);
  padding: 4px 12px;
  border-radius: 4px;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.info-row {
  display: flex;
  gap: 16px;
  font-size: 14px;
}

.info-row .label {
  min-width: 80px;
  color: var(--el-text-color-secondary);
}

.info-row .value {
  color: var(--el-text-color-primary);
}

.info-row .value.highlight {
  font-weight: 600;
  color: #b84a37;
}

.info-row.message .value {
  font-style: italic;
  color: var(--el-text-color-secondary);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.created-at {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.actions {
  display: flex;
  gap: 8px;
}

.badge {
  margin-left: 8px;
}
</style>
