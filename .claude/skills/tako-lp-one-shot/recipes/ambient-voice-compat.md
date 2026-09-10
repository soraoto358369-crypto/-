# 環境FX（Ambient）・文体（Voice）・互換表

## 環境FX — 8種、0〜2個。World の必須装備にある時だけ使う

すべて `<canvas class="fx">`（position:fixed; inset:0; pointer-events:none; z-index:1）に描く。`document.hidden` の時は描かない。SP は粒子数を 40% に落とす。

| ID | 見た目 | 実装の要点 | 使う World |
| --- | --- | --- | --- |
| rain | 斜めの雨線 | 線分 120〜220本、風で x を減らす、透明度 .05〜.17 | horror-west, wafu-dark |
| embers | 火の粉 | 橙の点 20〜40、上昇 + sin で揺れ、明滅 | wafu-dark, abyss-gold |
| bubbles | 泡・金の粒 | 金の点 + 赤の輪、上昇、明滅 | abyss-gold |
| dust | 塵 | 白の微粒子 60、ゆっくり漂う、超低透明度 | paper-black, mono-minimal(黒) |
| snow | 雪 | 白の丸、落下 + 横揺れ | wafu-dark（冬）, watercolor |
| scanlines | 走査線 | canvas 不要。`repeating-linear-gradient` を固定要素に、`mix-blend-mode: multiply` | neon-tokyo, horror-west（プレイヤー内のみ） |
| clay-drift | 漂うクレイ玉 | canvas 不要。固定の丸 div 5〜6個をマウスで視差 + GSAP で上下 | pastel-pop-dark, pastel-pop |
| morning-light | 朝の光の帯 | canvas 不要。斜めのグラデ帯を 16 秒で横断、`mix-blend-mode: screen` | paper-black |
| paper-fiber | 紙の繊維 | canvas 不要。feTurbulence の SVG を背景に、透明度 .35〜.5 | paper-black, paper-white, watercolor |

グレイン（`.grain`: feTurbulence + `mix-blend-mode: overlay` + steps アニメ）は **abyss-gold / horror-west / wafu-dark だけ**。

---

## 文体（Voice）— 6種

brief の `voice` を次のどれかに寄せる。SNS を渡された時は本人の投稿から「一人称・語尾・口癖・禁止語」を抜き出して上書きする。

| ID | 一人称/語尾 | 見出しの作り方 | やること | やらないこと |
| --- | --- | --- | --- | --- |
| honest（辛口本音） | 俺・私 / 〜だわ、〜やん | 断言 + 逆張り「〜はいらない」 | 具体的な数字と体験、批判は行動に向ける | 絵文字、敬語のクッション、精神論 |
| trailer（映画予告） | なし / 体言止め | 短い名詞句 + 英字キャプション | 世界観の語彙で統一、対比（去った/残った） | 説明、「〜です」 |
| literary（格調・文学） | 私 / 〜ました | 静かな一文、読点で息継ぎ | 具体的な時刻・場所・物、余白 | 感嘆符、煽り、太字連打 |
| pop（ポップ・友達） | 私・ぼく / 〜だよ、〜してみて | 質問形「〜してませんか？」 | ひらがな多め、1文短く、記号は「！」1回まで | 難語、専門用語、長文 |
| trust（ビジネス・信頼） | 弊社・私たち / 〜します | 主語 + 提供価値 | 実績は出典と単位、手順は番号 | 誇張、比喩、造語 |
| hype（煽り・情報商材） | 俺 / 〜しろ、〜するな | 数字先頭「月100万」「3日で」 | 期限・限定・損失回避、太字と色を交互に | 根拠のない数字（facts 外は絶対に書かない） |

日英比率: ja は見出し日本語・キャプション英語。`lang: ja+en` は見出しに英字 1 語まで。`lang: en` は逆。

---

## 互換表（禁止則）

- `letter` / `editorial` × Ambient は最大 1 個。
- `paper-white` / `mono-minimal` / `brutal` × グレイン・カーソル・グロー = 禁止。
- `pastel-pop*` × グリッチ・雷撃・明朝 = 禁止。
- `subject: person` × 架空数字ブロック（登録者数・残席）= 禁止。
- `use: optin` × CTA 2種類 = 禁止（CTA は 1 種類）。
- `countdown` × `deadline` なし = 骨格を変える。
- `chatgpt` 経路 × 画像 10 枚超 = 枚数を structure の下限に落とす（手動生成の負担を減らす）。
- 直近 3 件（history.json）と structure×world が同じ = structure を第 2 候補に。

## history.json の形式

```json
[{"site":"tako-optin","structure":"deck","world":"pastel-pop-dark","signature":"stamp","date":"2026-09-04"}]
```
先頭が最新。20 件を超えたら古いものから消す。
