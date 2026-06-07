import type { RouteRecordRaw } from "vue-router";
import Overview from "../views/Overview.vue";
import BattleRecords from "../views/BattleRecords.vue";

export const routes: RouteRecordRaw[] = [
  { path: "/", name: "overview", component: Overview, meta: { label: "运营总览" } },
  { path: "/battles", name: "battles", component: BattleRecords, meta: { label: "约战记录" } },
  { path: "/resources", name: "resources", component: Overview, meta: { label: "资源管理" } },
  { path: "/analytics", name: "analytics", component: Overview, meta: { label: "数据分析" } },
];

export const menuItems = routes.filter((r) => r.meta?.label).map((r) => ({
  path: r.path,
  label: r.meta?.label as string,
  name: r.name as string,
}));
