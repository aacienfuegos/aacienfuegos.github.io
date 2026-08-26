(() => {
  'use strict';

  const STORE_KEY = 'lang';
  const LANGS = ['es', 'en'];
  const nodes = document.querySelectorAll('[data-es][data-en]');
  const toggle = document.getElementById('lang-toggle');
  const opts = toggle ? toggle.querySelectorAll('.lang-opt') : [];

  const stored = () => {
    try { return localStorage.getItem(STORE_KEY); } catch { return null; }
  };
  const remember = (lang) => {
    try { localStorage.setItem(STORE_KEY, lang); } catch { /* modo privado */ }
  };

  const initial = () => {
    const fromQuery = new URLSearchParams(location.search).get('lang');
    if (LANGS.includes(fromQuery)) return fromQuery;
    const saved = stored();
    if (LANGS.includes(saved)) return saved;
    return (navigator.language || 'es').toLowerCase().startsWith('es') ? 'es' : 'en';
  };

  const apply = (lang) => {
    document.documentElement.lang = lang;
    nodes.forEach((el) => { el.textContent = el.dataset[lang]; });
    opts.forEach((o) => o.classList.toggle('on', o.dataset.lang === lang));
    if (toggle) toggle.setAttribute('aria-label', lang === 'es' ? 'Switch to English' : 'Cambiar a español');
  };

  let current = initial();
  apply(current);

  if (toggle) {
    toggle.addEventListener('click', () => {
      current = current === 'es' ? 'en' : 'es';
      apply(current);
      remember(current);
    });
  }

  const reveals = document.querySelectorAll('.reveal');
  const motionOk = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (motionOk && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      let step = 0;
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.style.transitionDelay = `${Math.min(step * 55, 220)}ms`;
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
        step += 1;
      });
    }, { rootMargin: '0px 0px 14% 0px', threshold: 0 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('in'));
  }

  const bar = document.querySelector('.topbar');
  if (bar) {
    const onScroll = () => bar.classList.toggle('stuck', window.scrollY > 8);
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  const year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
