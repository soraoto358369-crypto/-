---
name: tako-lp-one-shot
description: ヒアリング（おまかせ6問 / 詳細20問）か、SNS・自己紹介記事の URL を貼るだけで、デザイン10案を提示し、選んだ案で公開できる高品質 LP フォルダを一撃生成する。セールスレター / オプトイン / 簡易ホームページ / 自己紹介 / ポートフォリオ入口 / リンクまとめ の6用途。骨格7種 × 世界観100種（+独自）× シグネチャー演出10種。画像は Codex 自動 / ChatGPT 手動 / 持ち込み / 画像なし→プロンプト書き出し。「セットアップ」「スタート」「たこLP」「移行して」「公開して」「LPを作って」「オプトインページを作って」「自己紹介サイトを作って」「セールスレターのページを作って」「リンクまとめページを作って」「ポートフォリオの入口を作って」と言われたら必ず使う。「スタート」とだけ打たれたら、まずメニューを出す。「セットアップ」と打たれたら、ターミナルを使わせずにスキルが環境を全部入れる。
---

# Tako_LP_One-Shot — 手順書

このスキルの仕事は1つ。**ユーザーが質問に答える（か、SNS・記事の URL を貼る）だけで、10案から選んだデザインで、Cloudflare Pages にアップすれば公開できる LP フォルダを完成させる。**

品質の基準は完成例3サイト（下の公開URL。`examples/` フォルダは配布版に無い）。**あれより手を抜いたものは納品しない。**

完成例3サイト（公開URL。フォルダは同梱しない）:
- 架空映画の公式サイト「Tide Log」（journey × horror-west × flare）: https://tide-log-film.pages.dev/
- オプトイン「まめ家計簿」（deck × pastel-pop-dark × stamp）: https://mame-kakeibo.pages.dev/
- 自己紹介「高瀬凛」（editorial × paper-black × tear）: https://takase-rin-photo.pages.dev/

止まってよいのは次の3回だけ: ①ヒアリングの回答待ち（詳細モードは2回） ②10案の選択 ③ChatGPT 手動で画像を作る間。それ以外は聞かずに最後まで走る。

---

## セットアップ（「セットアップ」と打たれた時。メニュー 8 も同じ）

ユーザーはターミナルを使わない前提（Claude Code / Codex のデスクトップアプリだけ）。**スキルが代わりに全部実行する。** 聞くのは Codex のログインの1回だけ。

1. 「環境を整えます。数分かかります。途中で許可のダイアログが出たら「はい」「許可」を押してください」と1行伝える
2. Windows: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/setup.ps1 -Agent <claude|codex|both>` / Mac: `bash scripts/setup.sh <claude|codex|both>` を実行（自分が Codex 上で動いているなら codex、分からなければ both）。出力の `[OK ]/[NG ]/[.. ]/[-- ]` 行をそのまま見せる
   - 入るもの: Node.js / Python + Pillow / Codex CLI（Codex アプリ同梱を優先）/ **HyperFrames（必須。スキルとレンダ用ブラウザ）**
3. Codex CLI があってログイン前なら: 「画像を自動生成するために ChatGPT のログインが必要です。ブラウザが開くので Authorize を押してください」と伝えてから `codex login` を実行。開かない時は表示された URL を案内
4. `scripts/doctor` を実行して最終結果を見せ、`config.json` に `"setup_done": true` を書く
5. `[NG ]` が残っていれば、その項目の入れ方を1行で示す（ダウンロードページの URL とインストーラーを開くだけの手順）。残っていなければ「「スタート」と打つと始まります」で終える

## スタートメニュー（「スタート」「たこLP」と打たれた時）

### 先に環境チェック（毎回、1秒）

`scripts/doctor.ps1`（Windows）/ `scripts/doctor.sh`（Mac）を実行し、`[OK ]/[NG ]/[-- ]` の行をそのまま見せる。

- `[NG ]` が Node か Python にある、または HyperFrames が `[-- ]` → 「「セットアップ」と打つと全部入ります（数分）」と案内して止まる。`config.json` に `"setup_done": true` があるのに `[NG ]` なら入れ方を1行で示す。
- （旧仕様）HyperFrames が `[-- ]` で `config.json` に `"hf_asked": true` が無い → 聞かずにセットアップを案内する: 「ヒーロー動画（キービジュアルが映像として動く）を使うには HyperFrames が必要です。今入れますか？ 1 入れる（2〜3分） / 2 あとで / 3 使わない」。1 → `npx hyperframes skills` → `npx hyperframes doctor`。3 → `config.json` に `{"hf_asked":true,"hero_video":"no"}`。
- Codex / Playwright は聞かない。

### メニュー

```
Tako_LP_One-Shot ── 何をしますか？
1  新しくLPを作る
2  brief.md から作る（すでに書いてある人）
3  完成例を見る（3サイト + 世界観の見本帳100種）
4  作ったLPを直す
5  画像だけ作る（プロンプトを渡す）
6  使い方を読む
7  公開する（Cloudflare Pages。無料・帯域制限なし）
8  環境を整える（HyperFrames / Codex を入れる）
9  続きから（前回の途中を再開）
```

| 番号 | やること |
| --- | --- |
| 1 | 次を聞く: 「作り方を選んでください。 1 おまかせ（6問、5分） / 2 詳細ヒアリング（20問、15分。仕上がりにこだわる人） / 3 素材を貼る（SNS・自己紹介記事・既存LPの URL や文章。質問はほぼ不要）」。→ 「1. Intake」へ |
| 2 | カレントフォルダの `brief.md` を探す。無ければパスを聞く。→ 「1-d」へ |
| 3 | 完成例3サイトの公開URL（上の「0. 絶対ルール」の直前にある3本。用途とレシピを添えて表で）+ 「0 世界観の見本帳（100種・10グループ）」を出す。見本帳は特典の別フォルダ `Tako_LP_Lookbook`（スキルには入っていない）。「特典の Tako_LP_Lookbook フォルダの index.html をダブルクリックで開いてください」と伝える。「これで作る」と言われたら、その完成例のレシピ（骨格×世界観×演出）を引き継いで 1 へ。見本帳で「この世界観で」と id を言われたら 1 へ進み brief の `world:` に固定 |
| 4 | 「しょぼい」「単調」「ださい」「クオリティ上げて」なら `recipes/quality-up.md` の診断→修正の順で直す（聞き返さない）。サイトのフォルダを聞く（1回）。`<site>-src/recipe.json` を読み、修正指示を受けて編集。「このURLのフォームを付けて」→ `cta: auto`。「画像を入れた」→ prompts-handoff.md の差し替え。「台本を反映して」→ `scripts/apply-copy.py`。QA を通して報告 |
| 5 | 画像の説明を聞き、World を選ばせ、`prompts.json` を作って「4. Assets」の経路で生成。LP は作らない |
| 6 | 「`MANUAL.html` をダブルクリックするとブラウザで読めます」と案内し、`MANUAL.html` の 01〜08 章の要約（導入 → スタート → 作り方 → 10案 → 公開）を表示 |
| 7 | 「Netlify から移行して」「取り出して」なら `MIGRATE.html` の手順（`scripts/migrate-netlify.py` で取り出し → 点検 → publish）。それ以外はサイトのフォルダとプロジェクト名（英小文字・数字・ハイフン。無ければサイト名から提案）を確認し、`scripts/publish.ps1 -Dir <folder> -Name <name>`（Mac: `publish.sh <folder> <name>`）を実行する。初回はブラウザでログイン画面が開くので「Allow を押してください」と伝える。出力の `[OK ] 公開しました → URL` をそのまま見せる。自分で上げたい人には「`PUBLISH.html` をダブルクリックで開いてください」と案内し、その 1〜2 章（ドラッグ&ドロップ）を要約して表示 |
| 8 | 上の「セットアップ」を実行する（聞かずに全部入れる） |
| 9 | カレントの `*-src/recipe.json` を探し、`status` が `paused` のものを列挙して選ばせる。`brief.md` `copy.md` `prompts.md` を読み、止まった工程から再開 |

「スタート」以外（「LPを作って」など）で来た時はメニューを飛ばし、1 の「作り方を選ぶ」から入る。

## 0. 絶対ルール

1. **1サイトにシグネチャー演出は1つ。**
2. **数字は brief の `facts`（と `numbers_ok`）にあるものだけ。** でっち上げ禁止。`subject: work` の時だけ演出用の数字を許可し、フッターに「架空」明記。
3. **グレイン・カーソル・グリッチ・パララックスは World の必須装備にある時だけ。**
4. **フォントは World が決める。**
5. **画像の画風は World の接頭辞だけ。**
6. **実在人物の顔は生成しない。** 本人写真は使ってよい（顔出し OK と答えた時）。生成アイコン（エンブレム等）は **10案でその案が選ばれた時だけ**。`avoid:` にあれば案にも出さない。
7. **送信処理を自作しない。** `cta:` に従う（parts/forms.md）。メールアドレスを URL に載せない。
8. **直近3件と同じ 骨格×世界観 は選ばない。** `history.json`。
9. **納品前に QA を通す。** `scripts/qa.py` が全部 PASS になるまで納品しない。
10. **ブラウザペインのスクリーンショットを信用しない。** DOM を JS で読むか `scripts/shot.js`。裏タブではアニメが止まる。
11. **死んだリンクを納品しない。** URL が無い項目は行ごと省く。`href="#"` のプレースホルダは禁止。
12. **工程ごとに1行で進捗を言う。**「画像を生成中（3枚、約3分）。その間に本体を組みます」のように、何をしていて何分かかるかを伝える。
13. **`recipes/taste.md` を10案の前と Build の前に必ず読む。** 写実の象徴物（紋章・メダル）禁止、文字が主役、1サイト1つの比喩、中央揃えの縦積み禁止、強い色は1か所。これに反する案は出さない・組まない。

---

## 1. Intake — 入力を揃える

### 1-a. おまかせ（6問）
`recipes/hearing.md` の6問を1メッセージで聞く。`links` の時は回答後に 1-c のリンク一覧を追加で聞く。

### 1-b. 詳細ヒアリング（20問）
`recipes/hearing.md` の A・B を1メッセージ、C・D・E + 用途別追加を1メッセージで聞く。「分からない項目は空欄で OK」を添える。

### 1-c. `use: links` のリンク一覧（おまかせ・詳細どちらでも）
```
並べるリンクを教えてください。使うものだけ、URLを貼ってください。並べた順に表示します。
・LINE公式 ・メルマガ / メール登録（UTAGE など） ・note ・X（旧Twitter） ・Instagram ・Threads ・YouTube ・その他（表示名とURL）
一番押したいものを1つ教えてください。それを金のボタンにします。
```
URL の無い項目は行ごと省く。

### 1-d. 素材貼り付け（単独でも、1-a/1-b と併用でも）
`recipes/materials.md` に従い、URL・文章・画像から `name / facts / voice / audience / timeline / links / offers / avoid / 既存の色` を抽出して `brief.md` に書く。**抽出結果は 10案と同じメッセージで見せ、確認してもらう。** 足りない必須項目（用途・行動・受け皿）だけ、10案の前に1行で聞く。

### 1-f. 方向性を選ぶ（10案の前に1回。1-a/1-b の回答に方向性があれば飛ばす）
素材貼り付けだけで来た時、方向性が空欄・「おまかせ」の時、brief.md に `direction:` が無い時は、次を1メッセージで聞く。

```
デザインの方向性を選んでください（番号。2つまで可。「おまかせ」でも可）
①ダーク・壮大  ②明るい・上品  ③かわいい・ポップ  ④レトロ  ⑤和・自然
⑥ビジネス・テック  ⑦ジャンル（ホラー・SF・ゲーム）  ⑧ミニマル  ⑨かっこいい・クール  ⑩商材屋（ギラギラ）
（特典の見本帳 Tako_LP_Lookbook/index.html を開くと、各グループの世界観を画像で見比べられます）
```

返事の番号を brief の `direction:` に書き（例: `direction: [gira, dark]`）、`recipes/hearing.md` の「方向性 → 世界観の絞り込み」の規則で10案の World を決める。「おまかせ」なら audience から推定（女性寄り → cute/nature、男性寄り → cool/dark、ビジネス → business/light、稼ぐ系 → gira/dark）して、その旨を10案の冒頭に1行書く。

### 1-e. brief.md がある場合
必須6項目（`use` `name` `goal` `link` `facts` `audience`）が揃っていれば 2 へ。欠けていれば欠けた項目だけ1回で聞く。

答えは `brief.md` に書き起こす（`brief.template.md` の形式）。空欄はスキルが決め、納品時に「補完した箇所」として列挙する。

---

## 2. Proposals — デザイン10案を見せて選んでもらう（必ず止まる）

`recipes/taste.md` を読んでから、`recipes/proposals.md` の規則で10案を作り、表 + 各案1〜2行で提示する。各案に「アイデア（比喩）」「文字の主役」「レイアウトの型」を必ず書く。多様性の規則（世界観は最大2案同じ、画像なし案2つ以上、5方向カバー、`avoid:` を除外、生成アイコンは明記）を守る。

10案の末尾に「見本帳で見比べる用」として No. の縦リスト（`No.023` を1行1つ、案の順）をコードブロックで必ず付ける。見本帳の検索欄にそのまま貼れる。

ユーザーの返事: 番号 / 「おまかせ」→1番 / 「2と5を混ぜて」 / 「3で色だけ金」。採用内容を1行で確認して（返事は待たず）3へ。

---

## 3. Recipe — 5軸を確定する

選ばれた案から `recipe.json` を書く。

```json
{ "title":"黒金の一枚看板", "use":"links", "subject":"person", "structure":"deck", "world":"abyss-gold",
  "signature":"spotlight", "ambient":["bubbles"], "voice":"honest", "images":"codex", "icon":"photo",
  "cta":"line", "lang":"ja", "status":"building", "created":"2026-09-04" }
```

`images` は brief と環境で決める: `auto` → Codex があれば `codex`、無ければ **`later`**（画像なしで完成 → prompts.md）。ユーザーが「ChatGPT で自分で作る」と言った時だけ `chatgpt`（途中で止まる経路）。`icon` は 10案の「アイコン」列（photo / logo / emblem / none）。

---

## 4. Copy — 全文を書く

`copy.md` に全セクションの文言を先に書き切る。
- 見出しは日本語主、英語はキャプションと数字のアクセントのみ。
- 1セクション1メッセージ。見出し20字以内、本文2文まで。
- `facts` の数字は単位付き、brief の表現を変えない。
- voice（materials で抽出した口調を最優先）の禁止語・口癖を守る。
- CTA 文言は `goal` から1つ。
- 数字を含む言い回し（「3ステップ」「24時間」）を書くなら、brief の `numbers_ok:` に追記してから使う（QA が見る）。

---

## 5. Assets — 画像（5経路）

枚数と比率は structure が指定。プロンプト = World の接頭辞 + 被写体 + `no text, no letters, no watermark, no logo`。人物の顔は生成しない。

| `images:` | やること |
| --- | --- |
| `codex` | `scripts/gen-images.ps1` / `.sh` に `prompts.json` を渡してバックグラウンド実行。1枚約1分。終わるまで Build を進める。FAIL は1回だけ言い換えて再試行 |
| `later`（既定の代替） | **画像なしで完成させる**（`parts/prompts-handoff.md` の仮の絵）→ `<site>-src/prompts.md` を書き出し → 納品メッセージに「画像の入れ方」を書く。「画像を入れた」で差し替え |
| `chatgpt` | `prompts.md` を出して止まる。「続けて」で `images/` を読んで差し替え |
| `./folder/` | 手持ち画像を取り込む。足りないスロットは `later` の仮の絵 + prompts.md |
| `none` | 画像なしで完成。prompts.md も出さない（letter / links の標準） |

ヒーロー動画（`hero_video: auto` + HyperFrames OK）: KV から10秒ループを `npx hyperframes` で作り `assets/video/hero.mp4` に。失敗したら CSS ズームに降格し報告に書く。

生成・持ち込みとも `scripts/convert.py` で JPG 化・OGP・EXIF 除去。元画像は `<site>-src/` に退避。

---

## 6. Build — 組み立てる

出力: `<site>/index.html` `assets/css/style.css` `assets/js/main.js` `assets/img/`。

CTA は `cta:` に従う（parts/forms.md）: `auto` → `scripts/formprobe.py` で判定 → line / embed / native / iframe / link。native・iframe は「テスト送信して届くか確認」を報告に必ず書く。

必ず入れる: `<title>` `description` OGP `theme-color` `favicon.svg`（World の色）/ Google Fonts は World の書体のみ / GSAP は cdnjs / `prefers-reduced-motion` で全停止・全文可読 / `html{overflow-x:clip}` / フッターに © と（架空なら）明記。

組む前に `recipes/taste.md` を読み直す。文字の大きさの差、重ね・散らし、強い色1か所、比喩から決めた演出、を満たしているかを自分で点検してから書く。

モーションの品質基準（完成例3サイトと同等）:
1. **開幕** 0.8〜2.5秒。
2. **ヒーローの装置** は structure が決め、World の色と書体で。見出しは文字か行単位で登場。
3. **スクロール連動** を各セクションに1つ。`opacity:0` のまま放置しない（GSAP が読めなければ全部表示する保険を入れる）。
4. **シグネチャー** はヒーローで1回自動発火。終わったら全要素を同じ状態に戻す（灯りっぱなし・落ちっぱなしを防ぐ）。
5. **ホバー** は要素種別ごとに1種類。
6. 裏タブでは rAF が止まる。タイマー依存の演出は `document.hidden` を見る。
7. **金グラデ文字を1文字ずつ動かす時**は、グラデを文字の span 側に持たせる（親の `background-clip:text` は子の transform で効かなくなる）。
8. **PowerShell スクリプトは UTF-8 BOM 付き**で保存する。
9. **組み終わったら `python scripts/copyify.py <site>` を実行**し、文言要素に `data-t` を振って `<site>-src/台本.md` を書き出す。ユーザーはこのファイルを直して保存するだけで文言を差し替えられる（`scripts/watch-copy.py <site>` を動かしておけば保存のたびに自動反映）。

---

## 7. QA — 合格するまで直す

```
python scripts/qa.py <site> <site>-src/brief.md [--allow host]
node scripts/shot.js <site>
```
PASS 条件: タグ整合 / 参照ファイル存在 / 3MB 以下 / 通信は許可ホストのみ（`<a href>` のリンク先は対象外）/ メタ4点 / reduced-motion / EXIF なし / 数字は facts + numbers_ok 由来 / 架空明記（該当時）。FAIL は直して再実行。ユーザーに聞かない。

---

## 8. Deliver — 納品する

1. `<site>/README.md`: 公開手順、差し替え方、画像の入れ方（`later` の時）、再生成方法。
2. `<site>-src/` に `recipe.json`（`status: done`）`brief.md` `copy.md` `台本.md` `prompts.md` `qa-report.md`。納品メッセージに「文言は `台本.md` を編集して保存すれば反映」と、`python scripts/watch-copy.py <site>` の起動方法を書く。
3. `history.json` に追記（最大20件）。
4. 報告: 採用した案の名前とレシピ1行 / 何が動くか5点以内 / 公開手順 / **補完した箇所**（brief に無くて決めたこと）/ 残タスク（未投入の画像、テスト送信、URL 未提供の行を省いたこと）。

---

## 9. Codex CLI で動かす場合（Claude Code 以外）

このスキルは SKILL.md + スクリプトの構成なので、SKILL.md を読める AI コーディングツールなら動く。Codex CLI では `~/.codex/skills/tako-lp-one-shot/` に置く。違いは次の3点だけ。

1. **画像生成**: `scripts/gen-images.*` は Codex を外から呼ぶ用。Codex の中で動いている時は使わず、`prompts.json` の各プロンプトを自分の画像生成でそのまま作り、`<site>-src/<name>.png` に保存してから `scripts/convert.py` を実行する。
2. **プレビュー**: ブラウザペインは無いので `npx -y serve <site>` を起動し、URL をユーザーに示す。確認は `scripts/qa.py` と DOM を読むスクリプトで行う。
3. **文言の「Claude に頼む」**は「AI に頼む」と読み替える。手順・規則・10案・QA はすべて同じ。

## 10. 参照ファイル

| ファイル | 中身 |
| --- | --- |
| `MANUAL.html` | 使い方マニュアル（ブラウザで開く）。メニュー 6 |
| `recipes/quality-up.md` | 「しょぼい」「単調」と言われた時の診断→修正手順と、言い方の解釈表 |
| `PUBLISH.html` / `MIGRATE.html` / `SETUP.md` / `TROUBLESHOOTING.md` | 公開手順（Cloudflare Pages）/ Netlify からの移行 / 環境 / 困った時。HTML はブラウザで開く（手順を見せる時は HTML を読む） |
| `recipes/hearing.md` | おまかせ6問・詳細20問・用途別追加 |
| `recipes/materials.md` | SNS・記事・既存LPからの抽出 |
| `recipes/taste.md` | センスの基準。良いサイト10の共通点と禁止7項目。10案と Build の前に必読 |
| `recipes/proposals.md` | デザイン10案の作り方と提示形式 |
| `recipes/structures.md` / `worlds.md` / `signatures.md` / `ambient-voice-compat.md` | 5軸の辞書。worlds.md は100種・10グループ（機械可読 `worlds.json`。元データは `scripts/worlds_data.py`、`scripts/build-worlds.py` で md / json / 見本帳を再生成） |
| （`../Tako_LP_Lookbook/`） | 世界観見本帳。スキルとは別フォルダで特典として配布（無い人もいる）。100種・10グループを同じ被写体で見比べる。見本であって上限ではない（色替え・混合・custom で無限）。メニュー 3、10案の提示時に案内 |
| `parts/forms.md` | CTA 自動設置と4方式 |
| `parts/prompts-handoff.md` | 画像なし完成 → プロンプト書き出し → 差し替え |
| `parts/motion.js` | 共通モーション関数 |
| `scripts/` | setup（「セットアップ」で全部入れる）/ publish（Cloudflare Pages に公開）/ doctor / gen-images / convert / formprobe / qa / shot / copyify・apply-copy・watch-copy（台本.md ⇄ index.html） |
| `parts/sig-tear.md` / `parts/sig-stamp.md` | 紙を破く / スタンプ の実装（HTML・CSS・JS を貼るだけ） |
| （examples/） | 開発者の手元にだけある完成例3サイト。配布版には無く、公開URLで見る |
| `history.json` / `config.json` | 直近レシピ / 設定 |
