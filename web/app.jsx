import { t, getLanguage, subscribeLanguage } from "./i18n.js";
import React, { useEffect, useSyncExternalStore } from "react";
import { createRoot } from "react-dom/client";
import {
  S,
  subscribe,
  snapshot,
  boot,
  startNavigation,
  newIssue,
  action,
  notify,
  canGoBack,
  backObject,
} from "./model.js";
import { Page } from "./pages.jsx";
import { Shell } from "./workspace.jsx";
import { Dialog } from "./forms.jsx";
import { Button } from "./ui.jsx";
function App() {
  useSyncExternalStore(subscribe, snapshot);
  useSyncExternalStore(subscribeLanguage, getLanguage);
  useEffect(() => {
    const stop = startNavigation();
    boot();
    const shortcuts = (e) => {
      const editing = e.target instanceof Element && (
        e.target.isContentEditable || e.target.closest("input, textarea, select, [role='textbox'], [role='combobox']")
      );
      if (e.defaultPrevented || e.isComposing || e.keyCode === 229 || editing) return;
      if (e.altKey && !e.metaKey && !e.ctrlKey && e.key === "ArrowLeft" && canGoBack()) {
        e.preventDefault();
        backObject();
        return;
      }
      if (
        document.querySelector("dialog[open]") ||
        document.querySelector('.action-menu[data-state="open"]') ||
        document.querySelector('.select-menu[role="listbox"]') ||
        e.metaKey ||
        e.ctrlKey
      )
        return;
      if (e.key === "/") {
        e.preventDefault();
        action("focus-search").catch((error) => notify(error.message, true));
      }
      if (e.key.toLowerCase() === "c") {
        e.preventDefault();
        newIssue();
      }
    };
    document.addEventListener("keydown", shortcuts);
    return () => {
      stop();
      document.removeEventListener("keydown", shortcuts);
    };
  }, []);
  if (S.bootError)
    return (
      <section className="welcome">
        <h1>{t("無法開啟工作區")}</h1>
        <p>{S.bootError}</p>
        <Button action="reload">{t("重新載入")}</Button>
      </section>
    );
  if (!S.db) return <p className="boot">{t("正在開啟工作區…")}</p>;
  return (
    <>
      <Shell>
        <Page />
      </Shell>
      <Dialog />
      <div
        id="toast"
        role="status"
        aria-live="polite"
        className={S.toast ? "visible" + (S.toast.error ? " error" : "") : ""}
        style={S.toast?.retry ? { pointerEvents: "auto" } : undefined}
      >
        {S.toast?.message}
        {S.toast?.retry && (
          <>
            {" "}
            <Button action="retry-navigation">{t("重試")}</Button>
          </>
        )}
      </div>
    </>
  );
}
createRoot(document.getElementById("app")).render(<App />);
