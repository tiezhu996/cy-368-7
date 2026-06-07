declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>;
  export default component;
}

declare module "element-plus" {
  const ElementPlus: any;
  export default ElementPlus;
  export const ElMessage: any;
  export const ElMessageBox: any;
  export const ElButton: any;
  export const ElCard: any;
  export const ElTag: any;
  export const ElBadge: any;
  export const ElTabs: any;
  export const ElTabPane: any;
  export const ElEmpty: any;
  export const ElTable: any;
  export const ElTableColumn: any;
}
