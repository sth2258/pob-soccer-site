// Shared behavior for every page: mobile menu, dropdowns, scrollable tables.
(() => {
  const nav = document.getElementById('nav');
  const menuBtn = document.getElementById('menuBtn');
  const items = [...nav.querySelectorAll('.nav-item')];

  const closeAll = except => items.forEach(i => {
    if (i === except) return;
    i.classList.remove('open');
    i.querySelector('.nav-top').setAttribute('aria-expanded', 'false');
  });

  items.forEach(item => {
    const btn = item.querySelector('.nav-top');
    btn.addEventListener('click', () => {
      const open = !item.classList.contains('open');
      closeAll(item);
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });

  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.textContent = open ? '✕' : '☰';
    document.body.style.overflow = open ? 'hidden' : '';
    document.body.classList.toggle('menu-open', open);
    window.dispatchEvent(new Event('menutoggle'));
  });

  document.addEventListener('click', e => { if (!nav.contains(e.target) && e.target !== menuBtn) closeAll(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAll(); });
  nav.addEventListener('click', e => {
    if (e.target.tagName === 'A' && nav.classList.contains('open')) menuBtn.click();
  });

  // wide tables scroll sideways on small screens instead of breaking the layout
  document.querySelectorAll('.prose table').forEach(t => {
    const w = document.createElement('div');
    w.className = 'table-wrap';
    t.replaceWith(w);
    w.appendChild(t);
  });
})();
