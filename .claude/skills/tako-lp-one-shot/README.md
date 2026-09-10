# Tako_LP_One-Shot — 使い方（購入者向け）

brief.md を1枚書くだけで、Claude Code が公開できる LP フォルダを一撃で作ります。HTML の知識は不要です。

まず `MANUAL.html` をダブルクリックして開いてください（使い方の全体）。公開の手順は `PUBLISH.html`、Netlify にある既存LPを移したい時は `MIGRATE.html`（どちらもブラウザで開く）。導入はアプリのチャットに「セットアップ」と打つだけです（ターミナル不要）。

## 1. 入れる

1. このフォルダごと `~/.claude/skills/tako-lp-one-shot/` に置く（Windows: `C:\Users\<you>\.claude\skills\tako-lp-one-shot\`）。Codex CLI なら `~/.codex/skills/tako-lp-one-shot/`。
2. Python 3 と Pillow を入れる: `pip install pillow`（画像の変換に使います）。
3. 画像を自動生成したい人だけ: Codex CLI を入れて ChatGPT でログイン（`npm i -g @openai/codex` → `codex login`）。ChatGPT の有料プランがあれば追加課金なし。**入れなくても使えます**（下の「画像の4経路」）。

## 2. 書く

`brief.template.md` から用途を1つコピーして `brief.md` に保存。必須は6項目だけ。

```yaml
use: optin
name: まめ家計簿 7日間メール講座
goal: 無料メール講座に登録してもらう
link: https://example.com/register
facts:
  - 1日1通、7日間
audience: 家計簿が3日で止まる人
```

brief.md を書かずに、Claude Code に「LPを作って」と言っても動きます。その場合は6つの質問にまとめて答えるだけです。

## 3. 作る

Claude Code で `スタート` と打つとメニューが出ます（初めての人は `MANUAL.html` を先に）。

```
スタート
```

brief.md がある人は直接:

```
brief.md からLPを作って
```

登録の受け皿（LINE / メール配信ツールの埋め込み / Google フォーム / 登録ページへのリンク）は brief の `cta:` で選びます。詳しくは `parts/forms.md`。

流れ: レシピ決定（1行で表示）→ 文言 → 画像 → 組み立て → 自動検査 → 納品。途中で止まるのは「必須項目が足りない時」と「画像を ChatGPT で手動生成する時」だけです。

## 4. 画像の4経路

| brief の `images:` | どうなるか |
| --- | --- |
| `auto` | Codex があれば自動、無ければ ChatGPT 手動に切替 |
| `codex` | 全自動。1枚約1分 |
| `chatgpt` | `prompts.md` が出るので、ChatGPT の画面に貼って生成し、`images/` に保存して「続けて」 |
| `./images/` | 手持ちの写真を使う |
| `none` | 画像なし。色と文字だけで組む（セールスレターとリンクまとめの標準） |

## 5. 公開する

`PUBLISH.html` に、Cloudflare Pages の登録から公開・更新・フォームの受け皿・独自ドメインまで全部書いてあります。「公開して」と言えばスキルが上げます。最短は:

1. https://dash.cloudflare.com/sign-up でアカウントを作る（無料、カード不要）
2. Workers & Pages → Create → Pages → Upload assets にフォルダ（例: `mame-kakeibo/`）をドラッグ&ドロップ
3. 出てきた URL で公開完了

## 5-b. 環境について

必須は Node.js と Python + Pillow の2つだけ。Codex（画像の自動生成）と HyperFrames（ヒーロー動画）は任意で、「スタート」時のチェックで無ければ案内が出ます。詳細は `SETUP.md`。

## 6. 直したい時

- 文言: `index.html` を Claude Code に「○○の見出しを△△に変えて」
- 画像: `assets/img/` の同名ファイルを差し替え
- 見た目を変えたい: `brief.md` の `world:` を変えて作り直し（`かわいい` / `かっこいい` / `ギラギラ` / `上品` / `custom`）
- 同じ構成でもう1本: `<site>-src/recipe.json` を渡して「このレシピで作って」

## 7. できないこと

決済、フォームの送信処理、複数ページ、会員機能。フォームは見た目だけで、送信ボタンで `link:` に飛びます。登録の受け皿は UTAGE・LINE公式・Notion・Google フォームなどを用意してください。

## 8. 権利

生成画像（ChatGPT / Codex）は商用利用可。GSAP は無償版、Google Fonts はライセンス問題なし。実在の人物・商品の数字は brief に書いたものだけが使われ、それ以外は生成されません。数字の正しさは書いた本人の責任です。
