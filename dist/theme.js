(() => {
  const key = 'posetoki-theme';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let choice = null;
  try { const saved = localStorage.getItem(key); if (saved === 'light' || saved === 'dark') choice = saved; } catch {}
  const root = document.documentElement;
  const labels = {
    ko: ['다크 모드로 전환', '라이트 모드로 전환'],
    en: ['Switch to dark mode', 'Switch to light mode'],
    ja: ['ダークモードに切り替え', 'ライトモードに切り替え'],
    'zh-TW': ['切換深色模式', '切換淺色模式']
  };
  function updateButton() {
    const buttons = document.querySelectorAll('.theme-toggle');
    const dark = root.dataset.theme === 'dark';
    const label = (labels[root.lang] || labels.en)[dark ? 1 : 0];
    buttons.forEach(button => {
      button.setAttribute('aria-label', label);
      button.setAttribute('title', label);
      button.setAttribute('aria-pressed', String(dark));
    });
  }
  function apply() {
    root.dataset.theme = choice || (system.matches ? 'dark' : 'light');
    updateButton();
  }
  apply();
  system.addEventListener('change', () => { if (!choice) apply(); });
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.theme-toggle').forEach(button => button.addEventListener('click', () => {
      choice = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, choice); } catch {}
      apply();
    }));
    updateButton();
    new MutationObserver(updateButton).observe(root, { attributes: true, attributeFilter: ['lang'] });
  });
})();
