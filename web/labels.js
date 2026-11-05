export const cats = {
  UserStory: "User stories",
  ProductRequirement: "PRDs",
  Design: "Design",
  FrontEnd: "FrontEnd",
  BackEnd: "BackEnd",
};
export const relationLabels = {
  related: "相關任務",
  blocks: "阻擋",
  supersedes: "取代",
  duplicate: "重複任務",
};
export const approvalOptions = [
  { id: "draft", name: "草稿" },
  { id: "approved", name: "已核准" },
  { id: "superseded", name: "已取代" },
  { id: "evidence", name: "驗證證據" },
];
export const dispatchOptions = [
  { id: "review", name: "計畫審閱" },
  { id: "executing", name: "執行中" },
  { id: "completed", name: "已回報" },
  { id: "blocked", name: "受阻" },
  { id: "failed", name: "失敗" },
];
const states = {
  Backlog: "待安排",
  Todo: "待開始",
  "In Progress": "進行中",
  "Ready for Test": "待測試",
  "In Review": "待審閱",
  Done: "已完成",
  Canceled: "已取消",
  Blocked: "受阻",
  Duplicate: "重複",
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
  new Date(s).toLocaleString("zh-TW", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
