# brief.md テンプレート

用途を1つ選んでコピーし、`brief.md` として保存する。`#` 以降はメモなので消してよい。
必須は `use` `name` `goal` `link` `facts` `audience` の6つ。それ以外は空でよい（スキルが決める）。

## 全用途共通で使える項目

```yaml
images: auto          # auto / codex / chatgpt / later / ./images/ / none
                      #   later = 画像なしで完成させ、prompts.md を出す（Codex が無い人の既定）
icon: ./icon.jpg      # 本人写真・ロゴ。無ければ 10案の「アイコン」列で選ぶ（生成エンブレム or なし）
face_ok: true         # 本人の顔写真を使ってよいか
avoid: [エンブレム, 縦書き, 丸っこい]   # 嫌いな見た目。10案の生成時に除外される
direction: []          # 方向性グループ（最大2）: dark light cute retro nature business genre minimal cool gira。空なら 1-f で聞く
numbers_ok: [3ステップ, 24時間, 7日間]  # 実績ではない数字表現。QA の数字チェックで許可する
sources: [https://www.threads.com/@xxx, https://note.com/xxx/n/xxxx]  # 貼ると口調・実績・リンクを抽出する
mode: quick           # quick（おまかせ） / detail（詳細ヒアリング）
```

---

## 登録の受け皿（cta）— 全用途共通

| cta | 使う時 | 追加で書くもの |
| --- | --- | --- |
| `auto`（既定） | 迷ったらこれ。`link:` に貼った URL や `form_embed:` のコードから自動判定して設置する | `link:` か `form_embed:` |
| `line` | LINE 公式アカウントに登録させる | `link:` に友だち追加URL、任意で `line_qr: ./line-qr.png`、`keyword: 特典` |
| `embed` | UTAGE / MyASP / ConvertKit 等のフォームを使う | `form_embed:` にサービスの埋め込みコードをそのまま |
| `gform` | 配信ツールを持っていない | Google フォームの埋め込み iframe を `form_embed:` に。任意で `gift_link:`（フォームの確認メッセージに書く） |
| `link` | 登録ページへ飛ばすだけ（既定） | `link:` |

## A. オプトイン（メール・LINE登録を1つ取る）

```yaml
use: optin
subject: product            # 講座・特典そのものが主役なら product、あなた自身なら person
name: まめ家計簿 7日間メール講座
goal: 無料メール講座に登録してもらう
cta: auto                   # auto / line / embed / gform / link。auto は link の中身から自動判定
link: https://lin.ee/xxxxx  # LINE の友だち追加 / UTAGE などの登録ページ / Google フォーム のどれでも
line_qr: ./line-qr.png      # 任意。PC 表示用
keyword: 家計簿             # 任意。登録後に送ってもらう言葉
facts:
  - 1日1通、7日間
  - 登録者にPDF3点
audience: 家計簿が3日で止まる人。20〜40代、共働き
voice: やさしい・友達口調      # 空なら audience から決める
world: auto                   # worlds.md の id / auto（direction から選ぶ）/ custom
images: auto                  # auto / codex / chatgpt / ./images/ / none
hero_video: auto              # auto / yes / no。HyperFrames がある時だけ KV から10秒ループ動画を作る
icon:                         # person の時は必須
avoid: []                     # 使いたくない演出や色
lang: ja
```

## B. セールスレター（1商品を売り切る）

```yaml
use: letter
subject: product
name: 商品名
goal: 購入ページへ進んでもらう
link: https://example.com/buy
facts:
  - 価格 ○○円
  - 販売実績（本人申告の数字だけ）
  - 返金保証の条件
audience:
voice:
world: auto
images: none                  # レターは画像なしが標準。欲しければ auto
icon:
avoid: []
lang: ja
price: 9,800円                # 価格は必ずここに
guarantee: 30日返金           # 保証があれば
deadline: 2026-10-31          # 期限があれば
```

## C. 簡易ホームページ（何屋か3秒で分かる）

```yaml
use: home
subject: service
name: 屋号
goal: 問い合わせフォームへ
link: https://example.com/contact
facts:
  - 創業年
  - 対応エリア
  - 代表的なメニューと価格
audience:
voice:
world: auto
images: auto
icon:
sns: [https://instagram.com/xxx]
avoid: []
lang: ja
```

## D. 自己紹介（人を覚えてもらう）

```yaml
use: profile
subject: person
name: 名前 / 肩書き
goal: Threads をフォローしてもらう
link: https://www.threads.com/@xxx
facts:
  - 本人が公開している実績だけ
audience:
voice: 本人のSNS URL を貼れば口調を抽出する
world: auto
images: auto                  # 顔は生成しない。象徴物・後ろ姿・小物のみ
icon: ./icon.jpg              # 必須
timeline:                     # 年表があれば（無ければ省略）
  - 2018: 会社員のまま副業開始
  - 2022: 独立
avoid: []
lang: ja
```

## E. ポートフォリオ入口（作品へ送り込む）

```yaml
use: portfolio
subject: person
name:
goal: 作品一覧を見てもらう
link: https://example.com/works
facts: []
audience: 依頼を検討している人
works:                        # 代表作3〜6件。画像は ./works/ に入れる
  - title: 作品A
    year: 2025
    note: 一言
audience:
world: auto
images: ./works/
icon: ./icon.jpg
lang: ja
```

## F. リンクまとめ（SNSプロフに貼る1画面）

`links:` に**URLがあるものだけ**書く。空の行は作らない（死んだリンクを納品しないため）。`primary: true` を付けた1つが金のボタンになる。

```yaml
use: links
subject: person
name:
goal: 一番押したいリンクへ進んでもらう
links:
  - label: LINE公式
    url: https://lin.ee/xxxxx
    note: 無料特典を配布中
    primary: true          # 1つだけ。金の厚みボタンになる
  - label: note
    url: https://note.com/xxx
    note: 販売中のコンテンツ
  - label: X
    url: https://x.com/xxx
    note: 毎日の発信
  - label: Instagram
    url: https://instagram.com/xxx
    note: 日々の記録
facts: []                  # 実績を出すなら本人申告のまま
audience:
world: auto
images: auto               # 1画面なので 2〜3枚（背景・アイコン代わりの象徴）
icon: ./icon.jpg           # 無ければ World の色でエンブレムを生成する
lang: ja
```
