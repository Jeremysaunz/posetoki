/*
  Homepage motion.
  1. The hero runs a compressed croquis demo: each pose gets its construction
     (head, line of action, shoulder and hip tilt, plumb line, head-unit ruler)
     drawn in the order an artist lays it in, while a timer line runs out.
  2. The contact sheet of poses scrolls slowly and opens the library.
  3. Course schedules play through bar by bar when they come into view.
  Reduced motion keeps everything still; the motion toggle pauses all of it.
*/
(() => {
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const still = window.matchMedia('(prefers-reduced-motion: reduce)');
  const t = text => window.PoseTokiI18n?.t(text) ?? text;

  // Coordinates are in the 768 x 1152 space of the reference images.
  // The plumb line starts at the torso centre (about 65% of the way from the
  // shoulder midpoint to the hip midpoint), a closer stand-in for the centre
  // of mass than the pit of the neck.
  const DEMO = [
    { id: 'PT029', head: [372, 200, 56, 68, -10], action: 'M150 196C250 320 334 512 392 736S426 958 428 994',
      shoulder: [200, 318, 494, 298], hip: [244, 552, 446, 532], plumb: [346, 460, 1010], ruler: [135, 130, 995],
      tags: [[120, 452, 'start'], [512, 290, 'start'], [464, 566, 'start'], [346, 1062, 'middle']] },
    { id: 'PT018', head: [425, 208, 50, 62, -8], action: 'M96 772C230 660 350 520 392 420S430 230 432 150',
      shoulder: [346, 322, 481, 337], hip: [346, 495, 451, 517], plumb: [404, 444, 960], ruler: [150, 120, 790],
      tags: [[200, 560, 'end'], [330, 300, 'end'], [472, 552, 'start'], [404, 1012, 'middle']] },
    { id: 'PT036', head: [322, 135, 52, 64, -5], action: 'M312 78C246 300 300 650 372 1002',
      shoulder: [225, 262, 472, 270], hip: [290, 520, 470, 500], plumb: [369, 425, 1020], ruler: [75, 120, 1005],
      tags: [[205, 560, 'end'], [490, 248, 'start'], [492, 488, 'start'], [369, 1066, 'middle']] },
    { id: 'PT025', head: [378, 232, 52, 70, 0], action: 'M372 165C392 420 452 640 652 866',
      shoulder: [312, 360, 462, 367], hip: [267, 555, 477, 585], plumb: [377, 498, 995], ruler: [160, 140, 975],
      tags: [[452, 180, 'start'], [478, 338, 'start'], [494, 600, 'start'], [377, 1042, 'middle']] }
  ];
  const HOLD = 6500;
  const poses = window.PoseTokiPoses ?? [];
  const byId = id => poses.find(pose => pose.id === id);

  let paused = false;
  let visible = true;
  let index = 0;
  let timer = null;

  const figure = document.querySelector('.hero-figure');
  const sheet = figure?.querySelector('.figure-sheet');
  const svg = figure?.querySelector('.construction');
  const img = figure?.querySelector('img');
  const source = figure?.querySelector('source');
  const toggle = $('motionToggle');

  function set(el, attrs) { for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value); }

  function drawRuler(group, [top, unit, end]) {
    const count = Math.floor((end - top) / unit);
    let marks = `<line x1="40" x2="40" y1="${top}" y2="${end}"/>`;
    for (let k = 0; k <= count; k++) marks += `<line x1="26" x2="54" y1="${top + unit * k}" y2="${top + unit * k}"/>`;
    marks += `<line x1="26" x2="54" y1="${end}" y2="${end}"/>`;
    for (let k = 0; k < count; k++) marks += `<text x="40" y="${top + unit * k + unit / 2 + 10}">${k + 1}</text>`;
    group.innerHTML = marks;
  }

  function caption(pose) {
    const data = byId(pose.id);
    $('heroCode').textContent = pose.id;
    if (data) {
      $('heroName').textContent = t(data.name.ko);
      img.alt = t(data.name.ko);
    }
  }

  function applyConstruction(pose) {
    const [cx, cy, rx, ry, rot] = pose.head;
    set(svg.querySelector('ellipse'), { cx, cy, rx, ry, transform: `rotate(${rot} ${cx} ${cy})` });
    set(svg.querySelector('.action'), { d: pose.action });
    const [line3, line4] = [svg.querySelector('path.s3'), svg.querySelector('path.s4')];
    const [a, b, c, d] = pose.shoulder;
    set(line3, { d: `M${a} ${b}L${c} ${d}` });
    const joints3 = svg.querySelectorAll('circle.s3');
    set(joints3[0], { cx: a, cy: b }); set(joints3[1], { cx: c, cy: d });
    const [e, f, g, h] = pose.hip;
    set(line4, { d: `M${e} ${f}L${g} ${h}` });
    const joints4 = svg.querySelectorAll('circle.s4');
    set(joints4[0], { cx: e, cy: f }); set(joints4[1], { cx: g, cy: h });
    const [px, top, bottom] = pose.plumb;
    set(svg.querySelector('.plumb'), { d: `M${px} ${top}V${bottom}` });
    set(svg.querySelector('.bob'), { d: `M${px - 12} ${bottom}h24l-12 20z` });
    const centre = svg.querySelector('.com');
    if (centre) set(centre, { cx: px, cy: top });
    svg.querySelectorAll('.tag').forEach((tag, i) => {
      const [x, y, anchor] = pose.tags[i];
      set(tag, { x, y, 'text-anchor': anchor });
    });
    drawRuler(svg.querySelector('.ruler'), pose.ruler);
  }

  function restartDrawing() {
    figure.classList.add('reset');
    void svg.getBoundingClientRect();
    figure.classList.remove('reset');
  }

  function preload(pose) {
    const data = byId(pose.id);
    if (!data) return Promise.resolve();
    const probe = new Image();
    probe.src = data.webp ?? data.image;
    return probe.decode().catch(() => {});
  }

  async function show(next) {
    const pose = DEMO[next];
    const data = byId(pose.id);
    if (!data) return;
    await preload(pose);
    sheet.classList.add('swap');
    await new Promise(resolve => setTimeout(resolve, 280));
    if (source) source.srcset = data.webp;
    img.src = data.image;
    try { await img.decode(); } catch {}
    applyConstruction(pose);
    caption(pose);
    index = next;
    sheet.classList.remove('swap');
    restartDrawing();
    preload(DEMO[(next + 1) % DEMO.length]);
  }

  function schedule() {
    clearTimeout(timer);
    if (paused || !visible || document.hidden || still.matches) return;
    timer = setTimeout(async () => {
      await show((index + 1) % DEMO.length);
      schedule();
    }, HOLD);
  }

  function setPaused(value) {
    paused = value;
    root.classList.toggle('motion-paused', paused);
    if (toggle) {
      toggle.textContent = t(paused ? '움직임 재생' : '움직임 멈추기');
      toggle.setAttribute('aria-pressed', String(paused));
    }
    if (paused) clearTimeout(timer);
    else { restartDrawing(); schedule(); }
  }

  if (figure && svg && img && poses.length) {
    figure.classList.add('is-live');
    if (!still.matches && toggle) toggle.hidden = false;
    toggle?.addEventListener('click', () => setPaused(!paused));
    new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      if (visible) { restartDrawing(); schedule(); } else clearTimeout(timer);
    }).observe(figure);
    document.addEventListener('visibilitychange', schedule);
    still.addEventListener?.('change', () => { if (toggle) toggle.hidden = still.matches; schedule(); });
    window.addEventListener('posetoki-language', () => {
      caption(DEMO[index]);
      if (toggle) toggle.textContent = t(paused ? '움직임 재생' : '움직임 멈추기');
    });
    preload(DEMO[1]);
  }

  $('contactSheet')?.addEventListener('click', () => $('browseLibrary')?.click());

  const courses = document.querySelector('.course-grid');
  if (courses && 'IntersectionObserver' in window) {
    courses.classList.add('rhythm-ready');
    const play = course => {
      course.classList.remove('is-playing');
      void course.offsetWidth;
      course.classList.add('is-playing');
    };
    const watcher = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      courses.querySelectorAll('.course').forEach((course, i) => setTimeout(() => play(course), i * 260));
      watcher.disconnect();
    }), { threshold: .45 });
    watcher.observe(courses);
    courses.querySelectorAll('.course').forEach(course => {
      course.addEventListener('mouseenter', () => play(course));
      course.addEventListener('focus', () => play(course));
    });
  }
})();
