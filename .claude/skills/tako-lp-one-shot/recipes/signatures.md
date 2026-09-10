# シグネチャー演出（Signature）— 10種、1サイト1つ

「そのサイトだけの一発」。ユーザーの操作に応える。**必ずヒーローで1回は自動発火させ、操作のヒントを1行置く**（例:「クリックで信号弾。長押しで溜める。」）。色は World のトークンから取る。`prefers-reduced-motion` では全部無効にする。

共通: `document.addEventListener("pointerdown")` で `a, button, input, form` の上は無視する。

---

## 1. lightning — 雷撃
クリックで落雷（ジグザグ線 + 白フラッシュ）、長押しで溜めて太くなる。World: wafu-dark / horror-west。
```js
function bolt(x,y,power){const c=document.createElement("canvas");c.className="fx-bolt";c.width=innerWidth;c.height=innerHeight;
 Object.assign(c.style,{position:"fixed",inset:0,pointerEvents:"none",zIndex:92,mixBlendMode:"screen"});document.body.appendChild(c);
 const g=c.getContext("2d");let px=x,py=-20;g.strokeStyle="#fff";g.lineWidth=1.5+power*4;g.shadowColor=ACCENT;g.shadowBlur=24+power*40;g.beginPath();g.moveTo(px,py);
 while(py<y){px+=(Math.random()-.5)*60;py+=20+Math.random()*30;g.lineTo(px,py)}g.stroke();
 flash(.25+power*.4);setTimeout(()=>c.remove(),180+Math.random()*120)}
function flash(o){const f=document.createElement("div");Object.assign(f.style,{position:"fixed",inset:0,background:"#fff",opacity:o,pointerEvents:"none",zIndex:91,transition:"opacity .45s"});document.body.appendChild(f);requestAnimationFrame(()=>f.style.opacity=0);setTimeout(()=>f.remove(),500)}
```
長押し: `pointerdown` で時刻を記録、`pointerup` で `power=min((now-t0)/1200,1)`。

## 2. ink-splat — 墨・信号弾
クリック点から液体が弾ける（円の拡大 + 画面フラッシュ）。World: abyss-gold / wafu-dark / horror-west（信号弾は accent 色）。
```css
.splat{position:fixed;z-index:92;pointer-events:none;width:8px;height:8px;border-radius:50%;background:var(--accent);transform:translate(-50%,-50%);
 box-shadow:0 0 30px 10px color-mix(in srgb,var(--accent) 50%,transparent);animation:splat 1s cubic-bezier(.22,1,.36,1) forwards}
@keyframes splat{0%{transform:translate(-50%,-50%) scale(.2);opacity:1}70%{opacity:.9}100%{transform:translate(-50%,-50%) scale(var(--s,30));opacity:0}}
```
```js
function splat(x,y,size){const a=document.createElement("div");a.className="splat";a.style.left=x+"px";a.style.top=y+"px";a.style.setProperty("--s",size);document.body.appendChild(a);setTimeout(()=>a.remove(),1100)}
```

## 3. spotlight — スポットライト
暗い画面をカーソルの光が照らす。隠し文言が光の中でだけ読める。World: paper-black / abyss-gold / neon-tokyo / mono-minimal(黒)。
```css
.spot{position:fixed;inset:0;z-index:5;pointer-events:none;background:radial-gradient(circle 220px at var(--x,50%) var(--y,50%),transparent 0,rgba(0,0,0,.82) 100%)}
.hidden-line{color:transparent;-webkit-text-stroke:1px var(--accent)}
```
```js
addEventListener("pointermove",e=>{document.documentElement.style.setProperty("--x",e.clientX+"px");document.documentElement.style.setProperty("--y",e.clientY+"px")});
```
ヒーローの上でだけ有効にし、スクロールで消す（`opacity` を ScrollTrigger で 0 に）。

## 4. tear — 紙を破く
ヒーローの画像を紙で覆い、ドラッグでギザギザに破ける。紙片が舞う。World: paper-black / paper-white / watercolor。
実装は `parts/sig-tear.md` をそのまま使う。要点: canvas に紙を塗る → `globalCompositeOperation="destination-out"`、`fillStyle="#000"`（不透明にしないと半透明にしか消えない）→ pointermove で多角形を fill。ロード後 2 秒で小さな裂け目を自動で入れて誘う。

## 5. ripple — 水面の波紋
クリック点から同心円が広がり、下の画像が歪む。World: pastel-pop / watercolor / retro-future。
```css
.ripple{position:fixed;z-index:92;pointer-events:none;width:20px;height:20px;border-radius:50%;border:2px solid var(--accent);transform:translate(-50%,-50%);animation:rip 1.2s ease-out forwards}
@keyframes rip{to{transform:translate(-50%,-50%) scale(18);opacity:0;border-width:.5px}}
```
3重に 120ms ずらして出す。画像の歪みは SVG `feDisplacementMap` を持つ `filter` を 400ms だけ適用。

## 6. letters-fall — 文字崩壊
タイトルの文字が重力で落ちて転がり、スクロールで元に戻る。World: brutal / mono-minimal / wafu-dark / paper-black。
```js
// 見出しを文字に分割しておく（parts/motion.js の split）
function fall(h){const ws=h.querySelectorAll(".w");gsap.to(ws,{y:()=>innerHeight*.6+Math.random()*80,rotation:()=>(Math.random()-.5)*120,x:()=>(Math.random()-.5)*60,duration:1.2,ease:"bounce.out",stagger:{each:.03,from:"random"}})}
function rise(h){gsap.to(h.querySelectorAll(".w"),{y:0,x:0,rotation:0,duration:.9,ease:"back.out(1.4)",stagger:{each:.02,from:"random"}})}
```
クリックで `fall`、ScrollTrigger の `onEnterBack` で `rise`。

## 7. card-flip — カード裏返し
ホバー（SP はタップ）でカードが裏返り、裏面に本音・裏話が出る。World: pastel-pop / retro-future / brutal。
```css
.flip{perspective:1000px}.flip__in{position:relative;transform-style:preserve-3d;transition:transform .8s cubic-bezier(.34,1.56,.64,1)}
.flip:hover .flip__in,.flip.is-on .flip__in{transform:rotateY(180deg)}
.flip__f,.flip__b{backface-visibility:hidden;position:absolute;inset:0}.flip__b{transform:rotateY(180deg)}
```
表と裏で色を反転させる。裏には 1 行だけ。

## 8. stamp — スタンプ
タップで「それな」「承認」などの判子が押され、紙片が弾ける。押した数で返事が変わる。World: pastel-pop / brutal / watercolor / retro-future。
実装は `parts/sig-stamp.md` をそのまま使う。判子の文言と色は World と voice に合わせる（brutal は「YES」を黒で、watercolor は朱で）。

## 9. neon-power — ネオン点灯
ホバーした要素だけ通電してチカチカ点く。World: neon-tokyo。
```css
.neon{color:transparent;-webkit-text-stroke:1px var(--accent);transition:color .1s}
.neon.is-on{color:var(--accent);text-shadow:0 0 8px var(--accent),0 0 24px var(--accent),0 0 60px color-mix(in srgb,var(--accent) 60%,transparent);animation:flick .9s steps(2) 1}
@keyframes flick{0%,20%,45%{opacity:.2}10%,30%,100%{opacity:1}}
```
`pointerenter` で `is-on` を付け、離れて 1 秒後に外す。Web Audio で短い「バチッ」（ノイズ 40ms）を鳴らしてよい（サウンドONの時だけ）。

## 10. none — なし
演出を持たないことが演出。mono-minimal / paper-white の標準。ホバーの罫線と、画像の 1 回だけの開きに留める。ヒントの文言も置かない。

---

## 互換（World → 使える Signature）

| World | 使える |
| --- | --- |
| abyss-gold | ink-splat, spotlight, lightning(金色), letters-fall |
| pastel-pop / pastel-pop-dark | stamp, card-flip, ripple |
| paper-black | tear, spotlight, letters-fall |
| paper-white | tear, none |
| wafu-dark | lightning, ink-splat, letters-fall |
| neon-tokyo | neon-power, spotlight |
| brutal | stamp, letters-fall, card-flip |
| retro-future | card-flip, ripple, stamp |
| mono-minimal | none, letters-fall |
| watercolor | tear, ripple, stamp |
| horror-west | lightning(信号弾), ink-splat |
| その他の World | `recipes/worlds.md` の各項「使える演出」に従う（明るい World は none / tear / ripple / stamp 寄り、暗い World は spotlight / letters-fall / glitch 寄り） |
