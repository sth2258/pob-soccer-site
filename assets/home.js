(() => {
  const logo = document.getElementById('logo');
  const slot = document.getElementById('logoSlot');
  const header = document.getElementById('header');
  const brand = document.getElementById('brand');
  const nav = document.getElementById('nav');
  const heroCopy = document.getElementById('heroCopy');
  const cue = document.getElementById('cue');
  const curtain = document.getElementById('curtain');
  const skip = document.getElementById('skip');

  const DOCK = { x: 24, y: 10, size: 56 };   // logo position/size in the header
  let start = { x: 0, y: 0, size: 300 };      // logo position/size in the hero
  let introDone = false;

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  function measure() {
    const vw = innerWidth, vh = innerHeight;
    const size = Math.round(Math.min(vh * 0.42, vw * 0.62, 400));
    document.documentElement.style.setProperty('--logo-size', size + 'px');
    logo.style.width = size + 'px';
    logo.style.height = Math.round(size * 1.0236) + 'px';
    // slot position at scrollY = 0
    const r = slot.getBoundingClientRect();
    start = { x: r.left, y: r.top + scrollY, size };
    render();
  }

  function render() {
    // progress 0 → 1 over the first ~55% of the viewport height of scrolling
    // with the mobile menu open, dock the logo so it doesn't cover the menu
    const docked = document.body.classList.contains('menu-open');
    const p = !introDone ? 0 : docked ? 1 : clamp(scrollY / (innerHeight * 0.55), 0, 1);
    const e = ease(p);
    const x = lerp(start.x, DOCK.x, e);
    const y = lerp(start.y, DOCK.y, e);
    const s = lerp(1, DOCK.size / start.size, e);
    logo.style.transform = `translate(${x}px, ${y}px) scale(${s})`;

    if (!introDone) return;
    heroCopy.style.opacity = 1 - clamp(p * 1.8, 0, 1);
    heroCopy.style.transform = `translateY(${-p * 40}px)`;
    cue.style.opacity = 1 - clamp(p * 4, 0, 1);
    header.classList.toggle('solid', p > 0.85);
    const b = clamp((p - 0.75) / 0.25, 0, 1);
    brand.style.opacity = b;
    brand.style.transform = `translateX(${(1 - b) * -8}px)`;
  }

  function finishIntro() {
    if (introDone) return;
    introDone = true;
    logo.classList.remove('phase-fade', 'phase-grow');
    logo.classList.add('done');
    curtain.classList.add('gone');
    skip.classList.add('gone');
    heroCopy.classList.add('show');
    cue.classList.add('show');
    nav.classList.add('show');
    document.body.classList.remove('locked');
    // let the CSS reveal play, then hand hero-copy opacity to the scroll handler
    setTimeout(() => { heroCopy.style.transition = 'none'; cue.style.transition = 'none'; render(); }, 950);
    render();
  }

  function playIntro() {
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || scrollY > 10) { finishIntro(); return; }
    // 1) fade in from black at medium size
    requestAnimationFrame(() => requestAnimationFrame(() => logo.classList.add('phase-fade')));
    // 2) grow from medium to large
    setTimeout(() => { logo.classList.add('phase-grow'); }, 1500);
    // 3) lift the curtain, reveal the hero, unlock scroll
    setTimeout(finishIntro, 2900);
  }

  skip.addEventListener('click', finishIntro);
  addEventListener('keydown', e => { if (!introDone && (e.key === 'Escape' || e.key === ' ')) finishIntro(); });
  addEventListener('scroll', () => requestAnimationFrame(render), { passive: true });
  addEventListener('resize', measure);
  addEventListener('menutoggle', render);
  logo.addEventListener('click', e => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); });

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  scrollTo(0, 0);
  measure();
  // wait for fonts and the crest image so the fade-in starts with the logo ready
  const crest = logo.querySelector('img');
  Promise.all([
    document.fonts ? document.fonts.ready : null,
    crest.decode ? crest.decode().catch(() => {}) : null,
  ]).then(() => { measure(); playIntro(); });
})();
