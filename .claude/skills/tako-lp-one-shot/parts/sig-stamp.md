# stamp — スタンプ（シグネチャー実装）

「こんな人向け」のチェック項目をタップすると判子が押され、紙片が弾ける。押した数で返事が変わる。World: pastel-pop / pastel-pop-dark / brutal / watercolor / retro-future / kawaii-sticker / letterpress など。
判子の文言と色は World と voice に合わせる（brutal は「YES」を黒で、watercolor / letterpress は朱で、pastel は黄）。GSAP を使う（無ければ `gsap.fromTo` の2行を消しても動く）。

## HTML
```html
<ul class="checks" id="checks">
  <li><button class="check" type="button">レシートが財布にたまっている<span class="stamp">それな</span></button></li>
  <li><button class="check" type="button">月末に「なんでお金ないの？」となる<span class="stamp">それな</span></button></li>
  <li><button class="check" type="button">アプリを3つ以上入れたことがある<span class="stamp">それな</span></button></li>
  <li><button class="check" type="button">貯金はしたい。でも我慢はしたくない<span class="stamp">それな</span></button></li>
</ul>
<p class="verdict" id="verdict" hidden></p>
```

## CSS（`--stamp` を World の差し色に）
```css
.checks{display:grid;gap:12px;margin-top:22px;text-align:left;--stamp:var(--accent);--bounce:cubic-bezier(.34,1.56,.64,1)}
.check{position:relative;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:16px 20px 16px 70px;font-weight:700;font-size:16px;text-align:left;transition:transform .2s var(--bounce),border-color .3s,background .3s;width:100%;color:var(--ink);cursor:pointer}
.check:hover{transform:scale(1.02);border-color:var(--stamp)}
.check::before{content:"";position:absolute;left:20px;top:50%;transform:translateY(-50%);width:32px;height:32px;border-radius:50%;border:2px dashed var(--stamp);opacity:.7}
.check.is-stamped{border-color:var(--stamp)}
.stamp{position:absolute;left:10px;top:50%;width:54px;height:54px;border-radius:50%;border:3px solid var(--stamp);color:var(--stamp);display:grid;place-items:center;font-weight:900;font-size:12px;letter-spacing:.04em;transform:translateY(-50%) rotate(-14deg) scale(3);opacity:0;pointer-events:none}
.stamp::after{content:"";position:absolute;inset:4px;border-radius:50%;border:1px solid var(--stamp)}
.check.is-stamped .stamp{animation:stampIn .45s var(--bounce) forwards}
@keyframes stampIn{0%{opacity:0;transform:translateY(-50%) rotate(-30deg) scale(3)}60%{opacity:1;transform:translateY(-50%) rotate(-12deg) scale(.9)}100%{opacity:1;transform:translateY(-50%) rotate(-14deg) scale(1)}}
.verdict{margin-top:20px;min-height:2.4em;font-weight:900;color:var(--stamp);font-size:18px}
.verdict[hidden]{display:none}
.bit{position:fixed;z-index:60;width:8px;height:8px;border-radius:2px;pointer-events:none;animation:bit .9s cubic-bezier(.2,.8,.4,1) forwards}
@keyframes bit{to{transform:translate(var(--dx),var(--dy)) rotate(540deg);opacity:0}}
```

## JS
```js
(function(){
  var reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
  var stamped=0,verdict=document.getElementById("verdict");if(!verdict)return;
  var msgs={1:"1つでも当てはまれば、向いています。",2:"2つ。かなり「がんばる前提」になっているかも。",3:"3つ！ 意志ではなく仕組みの問題です。",4:"全部！ 大丈夫、作った本人も全部当てはまっていました。"};   // copy.md の voice に合わせて書き換える
  var cols=["#a9e8d1","#ffb7c9","#ffe08a","#b9d2ff"];   // World のパレット4色
  document.querySelectorAll(".check").forEach(function(b){b.addEventListener("click",function(){if(b.classList.contains("is-stamped"))return;b.classList.add("is-stamped");stamped++;verdict.hidden=false;verdict.textContent=msgs[Math.min(stamped,4)];
    if(window.gsap){gsap.fromTo(verdict,{y:10,opacity:0},{y:0,opacity:1,duration:.5,ease:"back.out(2)"});gsap.fromTo(b,{scale:.96},{scale:1,duration:.5,ease:"elastic.out(1,.4)"})}
    var r=b.getBoundingClientRect();burst(r.left+36,r.top+r.height/2,14)})});
  function burst(x,y,n){if(reduced)return;for(var i=0;i<n;i++){var p=document.createElement("i");p.className="bit";p.style.left=x+"px";p.style.top=y+"px";p.style.background=cols[i%4];p.style.setProperty("--dx",(Math.random()-.5)*220+"px");p.style.setProperty("--dy",(Math.random()-.8)*220+"px");document.body.appendChild(p);setTimeout(function(q){q.remove()},1000,p)}}
})();
```

## 注意
- 項目は4つ。5つ以上にすると返事が薄まる。項目の文は brief の `pains`（悩み）から取る。
- 押した後に元に戻す UI は付けない（押した事実が残るのが気持ちいい）。
