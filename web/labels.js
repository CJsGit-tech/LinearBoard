import { t, getLanguage } from "./i18n.js";
export const cats = {
  UserStory: "User stories",
  ProductRequirement: "PRDs",
  Design: "Design",
  FrontEnd: "FrontEnd",
  BackEnd: "BackEnd",
};
export const relationLabels = {
  get related() { return t("相關任務"); },
  get blocks() { return t("阻擋"); },
  get supersedes() { return t("取代"); },
  get duplicate() { return t("重複任務"); },
};
export const approvalOptions = [
  { id: "draft", get name() { return t("草稿"); } },
  { id: "approved", get name() { return t("已核准"); } },
  { id: "superseded", get name() { return t("已取代"); } },
  { id: "evidence", get name() { return t("驗證證據"); } },
];
export const dispatchOptions = [
  { id: "review", get name() { return t("計畫審閱"); } },
  { id: "executing", get name() { return t("執行中"); } },
  { id: "completed", get name() { return t("已回報"); } },
  { id: "blocked", get name() { return t("受阻"); } },
  { id: "failed", get name() { return t("失敗"); } },
];
const states = {
  get Backlog() { return t("待安排"); },
  get Todo() { return t("待開始"); },
  get "In Progress"() { return t("進行中"); },
  get "Ready for Test"() { return t("待測試"); },
  get "In Review"() { return t("待審閱"); },
  get Done() { return t("已完成"); },
  get Canceled() { return t("已取消"); },
  get Blocked() { return t("受阻"); },
  get Duplicate() { return t("重複"); },
};
export const statusLabel = (status) =>
  Object.hasOwn(states, status) ? states[status] : status;
export const defaultStatuses = [
  "Backlog",
  "Todo",
  "In Progress",
  "In Review",
  "Done",
  "Canceled",
  "Duplicate",
];
const classes = {
  "In Progress": "progress",
  "In Review": "review",
  Done: "done",
  Canceled: "canceled",
  Blocked: "blocked",
  "Ready for Test": "review",
  Todo: "todo",
  Duplicate: "canceled",
};
export const statusClass = (status) =>
  Object.hasOwn(classes, status) ? classes[status] : "backlog";
export const stamp = (s) =>
  new Date(s).toLocaleString(getLanguage(), {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
