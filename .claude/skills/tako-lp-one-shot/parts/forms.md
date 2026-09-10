# CTA とフォーム — 自動設置（`cta: auto`）と 4方式

静的サイトなので送信処理は外部に任せる。**既定は `cta: auto`**: ユーザーが貼った URL や埋め込みコードから種類を判定し、最も体験の良い方式で設置する。見た目は World に合わせる。**どの方式でも、ボタン文言は `goal` から1つに固定し、骨格が指定する回数だけ反復する。**

## 0. `cta: auto` — URL・コードを貼るだけで自動設置

ヒアリングの質問3（行動と受け皿）に貼られたものを `scripts/formprobe.py "<貼られたもの>"` に渡し、結果の `kind` / `method` で分岐する。

| 貼られたもの | 判定 | 設置 |
| --- | --- | --- |
| `https://lin.ee/...` `line.me/...` | line | 「1. line」 |
| `<form>` `<iframe>` `<script>` を含むコード | embed | 「2. embed」 |
| フォームがあるページ URL（UTAGE / MyASP / オレンジメール / Google フォーム 等） | formpage | 下の順で試す |
| フォームが無いページ URL | page | 「4. link」 |
| 何も貼られない | — | 「3. gform（Google フォーム）」を提案し、断られたら link |

formpage の設置順（formprobe の `method`）:

1. **native** — ページの `<form action method>` と `<input name>` が取れ、CSRF トークンや CAPTCHA が無い時。LP 内に同じ `name` の入力欄を World のデザインで再構築し、`action` に直接 POST する。hidden 項目は値ごと引き継ぐ。送信後は元サービスの完了ページに遷移する（`target` は付けない）。**設置後に必ずテスト送信を1回して、元サービスの管理画面に届いたかをユーザーに確認してもらう**（報告に書く）。
2. **iframe** — native が無理で、`X-Frame-Options` / `frame-ancestors` で拒否されていない時。`<iframe src="URL" loading="lazy" title="登録フォーム">` を LP のフォーム位置に置き、`min-height` をフォームの高さに合わせる（不明なら 640px、SP 760px）。枠線なし、背景は World の card 色。
3. **link** — どちらも無理な時。ボタンで遷移。

判定結果は1行で報告する（例:「UTAGE のフォームを直接埋め込みました（お名前・メール、送信後は UTAGE の完了ページへ）」「Google フォームは iframe で埋め込みました」）。

UTAGE の補足: 登録ページ URL（`utage-system.com/p/...`）は多くの場合 iframe 可。UTAGE 側の「フォーム埋め込みコード」（`<script>` 付き）が取れるなら、そちらを `embed` で貼るほうが軽い。ユーザーが UTAGE を使っていると分かったら「管理画面の『埋め込みコード』があればそれを貼ってください。無ければ URL のままで大丈夫です」と1回だけ添える。

## 1. `cta: line` — LINE 公式アカウントに登録させる

必要なもの: `link:` に友だち追加 URL（`https://lin.ee/xxxx` か `https://line.me/R/ti/p/@xxxx`）。任意で `line_qr:` に QR 画像（LINE Official Account Manager で発行した PNG）。

```html
<a class="btn btn--line" href="https://lin.ee/xxxx" target="_blank" rel="noopener">
  <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12 2C6.5 2 2 5.6 2 10c0 3.9 3.5 7.2 8.2 7.9.3.1.8.2.9.5.1.3.1.7 0 1l-.2 1c-.1.3-.2 1 .9.6 1.1-.5 5.9-3.5 8.1-6 1.5-1.6 2.1-3.2 2.1-5C22 5.6 17.5 2 12 2z"/></svg>
  LINEで受け取る
</a>
<p class="cta__note">タップで LINE が開きます。PCの方は QR を読み取ってください。</p>
<img class="cta__qr" src="assets/img/line-qr.png" alt="LINE 友だち追加 QR" width="140" height="140">
```

- ボタン色は LINE 緑 `#06C755` を使ってよい（World の色より優先。読者が「LINE だ」と分かることが大事）。ただし他の要素には使わない。
- `.cta__qr` は `@media (hover:hover) and (pointer:fine)` の時だけ表示、SP では隠す。
- 登録後の特典配布は LINE 側の自動応答（キーワード応答）で行う。ページには「登録後に『○○』と送ってください」を書く（brief の `keyword:` があれば）。

## 2. `cta: embed` — メール配信ツールのフォームを埋め込む

必要なもの: `form_embed:` にサービスが発行する埋め込み HTML（UTAGE / MyASP / オレンジメール / ConvertKit / Brevo / Mailchimp など）。

- 埋め込みコードは `<div class="form-embed">` の中にそのまま置く。**改変しない**（送信先やトークンが壊れる）。
- 見た目だけ CSS で寄せる: `.form-embed input, .form-embed button` に World のトークンを当てる。`!important` は使ってよい（外部 CSS に勝つため）。
- `<script>` を含む埋め込みは QA の外部通信チェックで弾かれる。`qa.py` に `--allow <host>` を付けて、そのサービスのホストだけ許可する（例: `--allow utage-system.com`）。
- 埋め込みが iframe の場合は高さを `min-height` で確保し、`loading="lazy"` を付ける。

## 3. `cta: gform` — Google フォームを埋め込む（配信ツール未導入の人向け）

無料・無制限。回答は Google スプレッドシートに溜まり、メール通知も設定できる。公開先を選ばない（Cloudflare Pages でも動く）。

手順（ユーザーにやってもらうのは 1〜3 だけ）:
1. https://forms.google.com で新しいフォームを作り、「メールアドレス」の質問を1つ入れる（必須にする）
2. 右上「送信」→ `<>`（埋め込み）タブ → 表示された `<iframe …>` をコピー
3. その iframe を貼ってもらう（`form_embed:` に入れる）
4. スキル側: LP のフォーム位置に `<iframe src="…" loading="lazy" title="登録フォーム">` を置き、`min-height` を確保。World の色に合わせて周囲をカードで囲む（iframe の中身は Google の見た目のまま）
5. 送信後の完了表示は Google 側に任せる。特典の配布は Google フォームの「確認メッセージ」に特典 URL（`gift_link:`）を書いてもらう

- 見た目を完全に World に合わせたい人は `embed`（UTAGE などのコード）か `link`（登録ページへ遷移）を勧める
- QA では iframe の `src` が `docs.google.com` なので `--allow docs.google.com` を付ける
- `cta: netlify`（Netlify Forms）は廃止。Cloudflare Pages では動かないため、既存の brief で `netlify` が来たら `gform` に読み替えて提案する

## 4. `cta: link` — 外部の登録ページへ飛ばす（既定）

`link:` へ遷移するだけ。見た目のフォームを置きたい時は、メール欄 + ボタンを描き、送信時に `location.href = link + "?email=" + encodeURIComponent(v)` **はしない**（メールアドレスを URL に載せない）。単に `link` へ遷移する。

- 見た目のフォームを置く場合は、`placeholder` に「登録ページで入力します」と分かるようにする。
- Google フォーム / Notion フォーム / UTAGE の登録ページはこの方式。

## 共通の約束

- ボタンは `goal` の言葉で書く。「送信」「Submit」は禁止。「7日間講座を受け取る」「LINEで特典をもらう」。
- 完了後の演出（コイン・紙片・チェック）は World のシグネチャーに合わせる。
- プライバシー文言を1行添える:「いつでも解除できます。売り込みメールは送りません。」
- メールアドレスを URL パラメータやログに残さない。
