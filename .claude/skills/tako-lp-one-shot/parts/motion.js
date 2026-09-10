/* parts/motion.js — Tako_LP_One-Shot 共通モーション関数
   使い方: 必要な関数だけ main.js にコピーする。GSAP 前提（cdnjs から読み込む）。
   すべて prefers-reduced-motion を尊重する。見た目（色・書体・ヒーロー型）は World と structure で決める。 */

const TM = (() => {
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  const hasGsap = typeof gsap !== "undefined";
  document.documentElement.classList.add(reduced ? "no-motion" : "motion");

  /* 見出しを文字 or 単語に分割。日本語は文字、英数字は単語のまま */
  function split(el) {
    const parts = el.textContent.match(/[A-Za-z0-9,.\-→']+|[^A-Za-z0-9\s]{1}|\s+/g) || [];
    el.innerHTML = parts.map(p => /^\s+$/.test(p) ? p : `<span class="w" style="display:inline-block">${p}</span>`).join("");
    return el.querySelectorAll(".w");
  }

  /* 登場（IntersectionObserver）。.in 要素に is-in を付ける。CSS 側で opacity/transform を書く */
  function reveal(sel = ".in", threshold = .15) {
    const els = document.querySelectorAll(sel);
    if (reduced) { els.forEach(e => e.classList.add("is-in")); return; }
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } }), { threshold });
    els.forEach(e => io.observe(e));
  }

  /* 文字の跳ね登場（GSAP） */
  function popWords(words, opts = {}) {
    if (reduced || !hasGsap) return;
    return gsap.fromTo(words, { y: 40, opacity: 0, rotate: 6 }, { y: 0, opacity: 1, rotate: 0, duration: .7, stagger: .028, ease: "back.out(1.8)", ...opts });
  }

  /* マスクからの浮上。HTML は <span class="mask"><span>text</span></span>、CSS は .mask{overflow:hidden;display:block} */
  function riseMasks(sel, opts = {}) {
    if (reduced || !hasGsap) return;
    gsap.set(sel, { yPercent: 110 });
    return gsap.to(sel, { yPercent: 0, duration: 1.1, stagger: .12, ease: "power4.out", ...opts });
  }

  /* 数字のカウントアップ。facts にある数字にだけ使う */
  function count(el, to, dur = 1800) {
    if (reduced) { el.textContent = to.toLocaleString("en-US"); return; }
    const t0 = performance.now();
    (function tick(now) { const k = Math.min((now - t0) / dur, 1), e = 1 - Math.pow(1 - k, 3); el.textContent = Math.floor(to * e).toLocaleString("en-US"); if (k < 1) requestAnimationFrame(tick); })(t0);
  }
  function countAll(sel = ".js-count") {
    const io = new IntersectionObserver(es => es.forEach(en => { if (!en.isIntersecting) return; io.unobserve(en.target); count(en.target, +en.target.dataset.to); }), { threshold: .5 });
    document.querySelectorAll(sel).forEach(e => io.observe(e));
  }

  /* 文字点灯（スクロールで 1 文字ずつ opacity を上げる）。ScrollTrigger 前提 */
  function illuminate(el) {
    const ws = split(el);
    ws.forEach(w => w.style.opacity = .18);
    if (reduced || typeof ScrollTrigger === "undefined") { ws.forEach(w => w.style.opacity = 1); return; }
    ScrollTrigger.create({ trigger: el, start: "top 85%", end: "bottom 50%", scrub: true, onUpdate: st => { const n = Math.ceil(st.progress * ws.length); ws.forEach((w, i) => w.style.opacity = i < n ? 1 : .18); } });
  }

  /* 画像の視差（親に overflow:hidden、img は height 120%） */
  function parallax(sel = ".js-parallax", strength = .2) {
    if (reduced || typeof ScrollTrigger === "undefined") return;
    document.querySelectorAll(sel).forEach(el => {
      const img = el.querySelector("img"), sp = parseFloat(el.dataset.speed || strength);
      gsap.fromTo(img, { yPercent: -sp * 40 }, { yPercent: sp * 40, ease: "none", scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: true } });
    });
  }

  /* 上から開く（clip-path） */
  function wipeIn(sel = ".js-frame") {
    if (reduced || typeof ScrollTrigger === "undefined") return;
    document.querySelectorAll(sel).forEach(f => gsap.fromTo(f, { clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)", duration: 1.3, ease: "power4.inOut", scrollTrigger: { trigger: f, start: "top 82%", once: true } }));
  }

  /* 磁力ボタン */
  function magnet(sel = "[data-magnet]", k = .16) {
    if (!fine || reduced) return;
    document.querySelectorAll(sel).forEach(el => {
      el.addEventListener("pointermove", e => { const r = el.getBoundingClientRect(); el.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * k}px,${(e.clientY - r.top - r.height / 2) * k}px)`; });
      el.addEventListener("pointerleave", () => el.style.transform = "");
    });
  }

  /* 3D チルト */
  function tilt(sel = ".js-tilt", deg = 14) {
    if (!fine || reduced) return;
    document.querySelectorAll(sel).forEach(el => {
      el.addEventListener("pointermove", e => { const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; el.style.transform = `perspective(900px) rotateY(${x * deg}deg) rotateX(${-y * deg}deg)`; });
      el.addEventListener("pointerleave", () => el.style.transform = "");
    });
  }

  /* カスタムカーソル。World の必須装備にある時だけ */
  function cursor(el, hoverSel = "[data-cursor]") {
    if (!fine || reduced) { el.style.display = "none"; return; }
    let x = 0, y = 0, tx = 0, ty = 0;
    addEventListener("pointermove", e => { tx = e.clientX; ty = e.clientY; });
    (function loop() { x += (tx - x) * .25; y += (ty - y) * .25; el.style.transform = `translate(${x}px,${y}px)`; requestAnimationFrame(loop); })();
    document.querySelectorAll(hoverSel).forEach(t => { t.addEventListener("pointerenter", () => el.classList.add("is-hover")); t.addEventListener("pointerleave", () => el.classList.remove("is-hover")); });
  }

  /* ヘッダーの出し入れ */
  function header(el) {
    let ly = 0;
    addEventListener("scroll", () => { const y = scrollY; el.classList.toggle("is-scrolled", y > 40); el.classList.toggle("is-hidden", y > ly && y > 320); ly = y; }, { passive: true });
  }

  /* 横スクロール固定（PC のみ）。track は flex、pin は親 */
  function horizontal(track, pin, trigger) {
    if (reduced || typeof ScrollTrigger === "undefined" || matchMedia("(max-width: 900px)").matches) return;
    const dist = () => Math.max(0, track.scrollWidth + track.getBoundingClientRect().left - innerWidth + 60);
    gsap.to(track, { x: () => -dist(), ease: "none", scrollTrigger: { trigger, pin, scrub: .8, start: "top top", end: () => "+=" + dist(), invalidateOnRefresh: true, anticipatePin: 1 } });
  }

  /* ローダー（進捗 0→100 or 指標）。done() で消す */
  function loader(el, onDone, render) {
    if (reduced) { el.remove(); onDone(); return; }
    let p = 0; const t = setInterval(() => { p += Math.random() * 12 + 5; if (p >= 100) { p = 100; clearInterval(t); setTimeout(() => { el.classList.add("is-done"); setTimeout(() => el.remove(), 1000); onDone(); }, 350); } render(p); }, 120);
  }

  /* 紙片・コイン・粒の放出（署名演出の付け合わせ） */
  function burst(x, y, n, colors, cls = "bit") {
    if (reduced) return;
    for (let i = 0; i < n; i++) { const p = document.createElement("i"); p.className = cls; p.style.left = x + "px"; p.style.top = y + "px"; p.style.background = colors[i % colors.length]; p.style.setProperty("--dx", (Math.random() - .5) * 240 + "px"); p.style.setProperty("--dy", (Math.random() - .8) * 240 + "px"); document.body.appendChild(p); setTimeout(() => p.remove(), 1000); }
  }

  return { reduced, fine, split, reveal, popWords, riseMasks, count, countAll, illuminate, parallax, wipeIn, magnet, tilt, cursor, header, horizontal, loader, burst };
})();
