# tear — 紙を破く（シグネチャー実装）

ヒーローの画像を紙で覆い、指でなぞるとギザギザに破けて下の画像が見える。紙片が舞う。World: paper-black / paper-white / watercolor / letterpress / vintage-map など紙の World。
色（紙の色・罫線・キャプション）は World のトークンに置き換える。以下をそのまま貼って動く。

## HTML（ヒーロー内）
```html
<div class="tear" id="tear">
  <img src="assets/img/kv.jpg" alt="…" fetchpriority="high">
  <canvas id="tear-canvas" aria-hidden="true"></canvas>
  <p class="tear__hint">指でなぞって、紙を破く</p>
</div>
```

## CSS
```css
.tear{position:relative;aspect-ratio:4/5;overflow:hidden;background:var(--bg2);user-select:none;-webkit-user-select:none;touch-action:none}
.tear img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tear canvas{position:absolute;inset:0;width:100%;height:100%;cursor:crosshair}
.tear__hint{position:absolute;left:50%;bottom:18px;transform:translateX(-50%);font-size:11px;letter-spacing:.2em;color:var(--ink);background:var(--bg);border:1px solid var(--line);padding:6px 14px;pointer-events:none;transition:opacity .6s;white-space:nowrap}
.tear.is-torn .tear__hint{opacity:0}
.shred{position:fixed;z-index:70;width:10px;height:14px;background:var(--bg2);pointer-events:none;animation:shred 1.1s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes shred{to{transform:translate(var(--dx),var(--dy)) rotate(var(--r));opacity:0}}
@media(max-width:800px){.tear{aspect-ratio:4/4.2}}
```

## JS（GSAP 不要）
```js
(function(){
  var box=document.getElementById("tear"),c=document.getElementById("tear-canvas");if(!box||!c)return;
  var ctx=c.getContext("2d"),dpr=Math.min(devicePixelRatio||1,2),W,H,torn=0;
  var PAPER="#1a1917",FIBER="241,237,228",CAP="rgba(241,237,228,.6)";   // World の --bg2 / --ink / --muted に合わせる
  function paper(){W=c.width=box.clientWidth*dpr;H=c.height=box.clientHeight*dpr;ctx.globalCompositeOperation="source-over";ctx.fillStyle=PAPER;ctx.fillRect(0,0,W,H);
    for(var i=0;i<W*H/700;i++){ctx.fillStyle="rgba("+FIBER+","+(Math.random()*.08)+")";ctx.fillRect(Math.random()*W,Math.random()*H,1.5*dpr,1.5*dpr)}
    ctx.strokeStyle="rgba("+FIBER+",.28)";ctx.lineWidth=dpr;ctx.strokeRect(dpr*10,dpr*10,W-dpr*20,H-dpr*20);
    ctx.fillStyle=CAP;ctx.font=(11*dpr)+"px sans-serif";ctx.fillText("FIG. 1",dpr*22,dpr*32);
    ctx.globalCompositeOperation="destination-out";ctx.fillStyle="#000";}   // 不透明の黒で抜く。半透明だと薄くしか消えない
  paper();addEventListener("resize",paper);
  function rip(x,y,r){ctx.beginPath();var n=9+Math.floor(Math.random()*5);for(var i=0;i<n;i++){var a=i/n*Math.PI*2,rr=r*(.55+Math.random()*.7);ctx.lineTo(x+Math.cos(a)*rr,y+Math.sin(a)*rr)}ctx.closePath();ctx.fill();torn++;if(torn>14)box.classList.add("is-torn")}
  function shred(cx,cy){var s=document.createElement("i");s.className="shred";s.style.left=cx+"px";s.style.top=cy+"px";s.style.setProperty("--dx",(Math.random()-.5)*160+"px");s.style.setProperty("--dy",(60+Math.random()*160)+"px");s.style.setProperty("--r",(Math.random()*360)+"deg");document.body.appendChild(s);setTimeout(function(){s.remove()},1200)}
  var down=false,last=null;
  function pt(e){var r=c.getBoundingClientRect();return{x:(e.clientX-r.left)*dpr,y:(e.clientY-r.top)*dpr}}
  c.addEventListener("pointerdown",function(e){down=true;last=pt(e);rip(last.x,last.y,26*dpr);shred(e.clientX,e.clientY);c.setPointerCapture(e.pointerId)});
  c.addEventListener("pointermove",function(e){if(!down)return;var p=pt(e),dx=p.x-last.x,dy=p.y-last.y,d=Math.hypot(dx,dy),steps=Math.max(1,Math.floor(d/(8*dpr)));for(var i=1;i<=steps;i++){rip(last.x+dx*i/steps+(Math.random()-.5)*10*dpr,last.y+dy*i/steps+(Math.random()-.5)*10*dpr,(22+Math.random()*14)*dpr)}if(Math.random()<.5)shred(e.clientX,e.clientY);last=p});
  ["pointerup","pointercancel","pointerleave"].forEach(function(ev){c.addEventListener(ev,function(){down=false})});
  setTimeout(function(){var x=W*.62,y=H*.3;for(var i=0;i<6;i++)rip(x+i*9*dpr,y+i*13*dpr,14*dpr)},2400);   // 2.4秒後に小さな裂け目を自動で入れて誘う
})();
```

## 注意
- `prefers-reduced-motion` の時は canvas を出さず画像だけ見せる（`html.no-motion .tear canvas{display:none}`）。
- 紙の色は World の `--bg2`、繊維とキャプションは `--ink` の RGB を使う。金や差し色は使わない。
