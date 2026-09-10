/* 湯気が晴れる — main.js
   保険: GSAP が読めなくても全要素を表示する（opacity:0 のまま放置しない） */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var rv = document.querySelectorAll(".rv");

  function showAll() { for (var i = 0; i < rv.length; i++) rv[i].classList.add("is-in"); }

  if (reduce) { showAll(); return; }

  /* 1. スクロール登場 — GSAP があれば ScrollTrigger、無ければ IntersectionObserver */
  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    rv.forEach(function (el) {
      ScrollTrigger.create({
        trigger: el, start: "top 84%", once: true,
        onEnter: function () { el.classList.add("is-in"); }
      });
    });
  } else if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -14% 0px" });
    rv.forEach(function (el) { io.observe(el); });
  } else { showAll(); }

  /* 保険: スクロールのたびに、画面に入ったものは必ず表示する。
     GSAP も IntersectionObserver も効かなかった場合の最後の砦。
     opacity:0 のまま取り残されるセクションを作らない。 */
  function sweep() {
    var left = 0;
    for (var i = 0; i < rv.length; i++) {
      if (rv[i].classList.contains("is-in")) continue;
      if (rv[i].getBoundingClientRect().top < innerHeight * 0.92) rv[i].classList.add("is-in");
      else left++;
    }
    return left;
  }
  addEventListener("scroll", sweep, { passive: true });
  addEventListener("resize", sweep, { passive: true });
  setTimeout(sweep, 1200);
  setTimeout(sweep, 3000);

  /* 2. 読了プログレスバー */
  var prog = document.getElementById("prog"), ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      prog.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%";
      ticking = false;
    });
  }
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* 3. シグネチャー: ripple — クリック点から同心円が3重に広がる */
  function ripple(x, y) {
    for (var i = 0; i < 3; i++) {
      (function (n) {
        setTimeout(function () {
          var d = document.createElement("div");
          d.className = "ripple";
          d.style.left = x + "px";
          d.style.top = y + "px";
          document.body.appendChild(d);
          setTimeout(function () { d.remove(); }, 1300);
        }, n * 120);
      })(i);
    }
  }
  addEventListener("pointerdown", function (e) {
    if (document.hidden) return;
    if (e.target.closest("a, button, summary, details")) return;
    ripple(e.clientX, e.clientY);
  }, { passive: true });

  /* ヒーローで1回だけ自動発火。終わったら痕跡を残さない */
  addEventListener("load", function () {
    if (document.hidden) return;
    setTimeout(function () { ripple(innerWidth * 0.28, innerHeight * 0.42); }, 900);
  });
})();
