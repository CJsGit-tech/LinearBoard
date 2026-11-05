import english from './locales/en.json';

export const supportedLanguages = ['en', 'zh-TW'];
export function resolveLanguage(saved, browserLanguage = 'en') {
  if (supportedLanguages.includes(saved)) return saved;
  return /^zh(?:-|$)/i.test(browserLanguage) ? 'zh-TW' : 'en';
}
let savedLanguage;
try { savedLanguage = localStorage.getItem('lb.language'); } catch {}
let language = resolveLanguage(savedLanguage, navigator.language);
const listeners = new Set();
export const getLanguage = () => language;
export const subscribeLanguage = listener => {
  listeners.add(listener);
  return () => listeners.delete(listener);
};
export function setLanguage(next) {
  if (!supportedLanguages.includes(next) || next === language) return;
  language = next;
  try { localStorage.setItem('lb.language', next); } catch {}
  document.documentElement.lang = next === 'en' ? 'en' : 'zh-Hant';
  for (const listener of listeners) listener();
}
// Only application-owned messages pass through this function. Record contents stay untouched.
export function t(message, ...values) {
  const template = language === 'en' && Object.hasOwn(english, message) ? english[message] : message;
  return template.replace(/\{(\d+)\}/g, (match, index) => index < values.length ? String(values[index]) : match);
}
document.documentElement.lang = language === 'en' ? 'en' : 'zh-Hant';
