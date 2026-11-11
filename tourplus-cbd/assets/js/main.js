/* 琥珀の環 — main.js
   保険: GSAP が読めなくても、画面に入った要素は必ず表示する */
(function () {
  "use strict";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var rv = document.querySelectorAll(".rv");
  var hero = document.querySelector(".hero");
  var spot = document.getElementById("spot");
  var prog = document.getElementById("prog");

  if (reduce) { for (var i = 0; i < rv.length; i++) rv[i].classList.add("is-in"); return; }

  /* 最初の画面に入っているものは最初から見せる */
  rv.forEach(function (el) {
    if (el.getBoundingClientRect().top < innerHeight) el.classList.add("is-in");
  });

  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    rv.forEach(function (el) {
      ScrollTrigger.create({ trigger: el, start: "top 86%", once: true,
        onEnter: function () { el.classList.add("is-in"); } });
    });
  } else if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -12% 0px" });
    rv.forEach(function (el) { io.observe(el); });
  }

  /* 最後の砦: スクロール・リサイズのたびに、画面に入ったものを表示する */
  function sweep() {
    for (var i = 0; i < rv.length; i++) {
      if (!rv[i].classList.contains("is-in") &&
          rv[i].getBoundingClientRect().top < innerHeight * 0.94) rv[i].classList.add("is-in");
    }
  }
  addEventListener("resize", sweep, { passive: true });
  setTimeout(sweep, 1200); setTimeout(sweep, 3000);

  /* 読了プログレス */
  var ticking = false;
  function onScroll() {
    sweep();
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement.scrollHeight - innerHeight;
      prog.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%";
      /* シグネチャー: spotlight はヒーローの上だけ。抜けたら消す */
      /* ヒーローを抜けたら消す。点けるのは pointermove を受けてから
         （読み込み直後にページ全体を暗くしないため） */
      if (!hero.getBoundingClientRect().bottom > innerHeight * 0.35) spot.classList.remove("is-on");
      if (hero.getBoundingClientRect().bottom <= innerHeight * 0.35) spot.classList.remove("is-on");
      ticking = false;
    });
  }
  var hasPointer = matchMedia("(hover:hover) and (pointer:fine)").matches;
  addEventListener("scroll", onScroll, { passive: true });

  addEventListener("pointermove", function (e) {
    if (!hasPointer || document.hidden) return;
    var r = document.documentElement;
    r.style.setProperty("--x", e.clientX + "px");
    r.style.setProperty("--y", e.clientY + "px");
    if (hero.getBoundingClientRect().bottom > innerHeight * 0.35) spot.classList.add("is-on");
  }, { passive: true });

  onScroll();
})();
