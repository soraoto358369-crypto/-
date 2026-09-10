# 世界観（World）— 100種 + custom

World は「色トークン」「書体2〜3」「質感」「画像プロンプトの接頭辞」「必須装備」「禁止装備」「使える演出」「章番号の例（ARM 01 / 第一幕 など）」のセット。**画風もここに属する。** 見本帳 `lookbook/index.html` に全種の代表画面がある。機械可読版は `recipes/worlds.json`（このファイルと同じ内容。`scripts/build-worlds.py` が両方を生成する。**手で直す時は `scripts/worlds_data.py` を直して再生成**）。

## 全 World 共通の禁止（`recipes/taste.md`）

- 写実の象徴物（紋章・メダル・王冠・金塊・宝石）を生成しない。名前の由来（たこ・鷹 など）を紋章にしない。
- 1つの素材（金グラデ等）を文字・ボタン・枠・粒に全部塗らない。強い色は「1か所」。
- 明るい World で `cinematic photorealistic` を使わない。イラスト・切り抜き・抽象にする。
- 英字の箔付け語（PREMIUM / LUXURY / 8 FIGURES 等）を置かない。

## 選び方

1. brief の「見た目の希望」を下の表で**グループ**に落とす（複数可）
2. そのグループの中から、用途（uses）と読者に合う World を**5種類以上**選んで10案に散らす（同じ World は最大2案）
3. 希望が「おまかせ」なら: 女性寄り → cute+nature / 男性寄り → dark+retro / ビジネス → business+light を混ぜる
4. 10案の「世界観」列にはここの id をそのまま書く。ユーザーが見本帳で見比べられる

| 希望 | グループ | 代表 |
| --- | --- | --- |
| ダーク / 壮大 / 映画っぽく / 静かに重い | dark（ダーク・壮大） | wafu-dark, midnight-navy, deep-ocean, cinema-black |
| 上品 / 信頼 / ミニマル / クラフト | light（明るい・上品） | paper-white, ivory-serif, letterpress, newspaper |
| かわいい / ポップ / 元気 | cute（かわいい・ポップ） | pastel-pop-dark, pastel-pop, candy-shop, macaron |
| レトロ / 昭和 / 80s / ゲーム | retro（レトロ） | retro-future, showa-kissa, pixel-8bit, riso-poster |
| 和風 / 自然 / やさしい / 季節 | nature（和・自然） | watercolor, sumi-ink, forest-moss, ocean-blue |
| ビジネス / 医療 / テック / 数字で信頼 | business（ビジネス・テック） | trust-navy, fintech-emerald, data-dashboard, clinic-clean |
| ホラー / SF / ゲーム / アニメ・作品の公式サイト | genre（ジャンル（ホラー・SF・ゲーム）） | horror-west, horror-jp, sf-space, game-rpg, game-esports, anime-kinetic |
| ミニマル / 余白 / 文字だけ | minimal（ミニマル） | mono-minimal, minimal-black, minimal-type, gallery-white |
| かっこいい / クール / 硬派 / 速い | cool（かっこいい・クール） | paper-black, neon-tokyo, concrete, carbon-red |
| 商材屋 / ギラギラ / 黒金 / セール | gira（商材屋（ギラギラ）） | abyss-gold, gold-rush, red-alert, money-green |

## 一覧（id → 名前 / 方向性 / 向く用途）

| No. | id | 名前 | 方向性 | 向く用途 |
| --- | --- | --- | --- | --- |
| 1 | wafu-dark | 和風ダーク | 和風・壮大 | 作品公式サイト / イベント / 和の商材 |
| 2 | midnight-navy | 深夜の紺 | かっこいい・落ち着き | 自己紹介 / コーチ・カウンセラー / 夜の商材 |
| 3 | deep-ocean | 深海の青 | ダーク・壮大・静か | 壮大な講座 / 海・旅 / 静かな商材 |
| 4 | volcanic | 溶岩 | ダーク・熱い | 熱い商材 / スポーツ / 挑戦系 |
| 5 | storm | 嵐 | ダーク・緊張 | 覚悟系の商材 / 作品 / 告知 |
| 6 | cinema-black | 映画の予告 | ダーク・壮大・白黒 | 作品告知 / イベント / ローンチ |
| 7 | aurora | オーロラ | ダーク・壮大・幻想 | 旅・北欧 / 壮大な講座 / 幻想系の作品 |
| 8 | eclipse | 日蝕 | ダーク・壮大・儀式 | ローンチ / 作品 / 一度きりのイベント |
| 9 | paper-white | 紙・エディトリアル | 上品・信頼 | 簡易HP（士業・医療）/ 自己紹介 |
| 10 | ivory-serif | 象牙のセリフ | 上品・高級 | 高単価サービス / サロン / ブライダル |
| 11 | linen-sage | 麻とセージ | 自然派・やさしい | ヨガ・食・暮らし / 教室 / 簡易HP |
| 12 | porcelain-blue | 白磁と藍 | 上品・和洋 | 工芸 / 器・食 / 旅館 |
| 13 | letterpress | 活版印刷 | 上品・クラフト | 文具・紙もの / 書籍・出版 / 招待 |
| 14 | newspaper | 新聞 | かっこいい・報道 | 号外的セールスレター / ニュース系発信 |
| 15 | botanical | 植物図鑑 | 上品・クラシック・自然 | 植物・ハーブ / 教室 / 上品な自然系 |
| 16 | marble | 大理石 | 上品・高級・白 | ジュエリー / サロン / 高単価サービス |
| 17 | kraft | クラフト紙 | 上品・素朴・手仕事 | パン・食品 / 手仕事 / ギフト |
| 18 | pastel-pop | 白地パステル | かわいい・明るい | オプトイン / 教室・サロン |
| 19 | pastel-pop-dark | 黒地パステルクレイ | かわいい・でも大人っぽく | オプトイン / リンクまとめ / 講座 |
| 20 | candy-shop | キャンディショップ | かわいい・ビビッド | 雑貨・コスメ / 若年層 / イベント |
| 21 | sakura | 桜 | かわいい・和・春 | 春の企画 / 教室 / 和菓子 |
| 22 | kawaii-sticker | シール風 | かわいい・元気 | 子ども向け / イベント / 楽しい商材 |
| 23 | macaron | マカロン | かわいい・上品 | パティスリー / ギフト / 女性向けサロン |
| 24 | picnic-gingham | ピクニック | かわいい・素朴 | カフェ・食 / 手作り / 週末イベント |
| 25 | pop-art | ポップアート | ポップ・コミック | イベント / エンタメ / 若年層 |
| 26 | cream-soda | クリームソーダ | かわいい・レトロ喫茶 | 喫茶・スイーツ / レトロ雑貨 |
| 27 | shojo-manga | 少女漫画 | かわいい・キラキラ | 少女向け / 恋愛系 / 推し活 |
| 28 | yumekawa | ゆめかわ | かわいい・夢 | 雑貨・コスメ / 若年層 / 癒やし系 |
| 29 | retro-future | レトロフューチャー | レトロ・ポップ | 商品LP / イベント / カフェ |
| 30 | showa-kissa | 昭和喫茶 | レトロ・和 | 喫茶・食 / 純喫茶的な商材 |
| 31 | vapor-80s | ヴェイパーウェーブ | レトロ・80年代 | 音楽・アート / 若年層 / イベント |
| 32 | y2k-chrome | Y2K クローム | レトロ・未来 | ファッション / 音楽 / 若年層 |
| 33 | riso-poster | リソグラフ | レトロ・印刷 | デザイン・ZINE / イベント / 若年層 |
| 34 | vintage-map | 古地図 | レトロ・旅 | 旅・ツアー / 冒険系の講座 / 読み物 |
| 35 | film-camera | フィルム写真 | レトロ・ノスタルジー | 写真家 / 旅 / 思い出系の商材 |
| 36 | showa-pop | 昭和ポップ | レトロ・60年代 | 雑貨・喫茶 / 昭和イベント / レトロ商材 |
| 37 | art-deco | アールデコ | レトロ・華麗 | ホテル・バー / ブライダル / 華やかなイベント |
| 38 | watercolor | 水彩・手描き | やさしい・手づくり | 教室・ハンドメイド / 絵本・エッセイ |
| 39 | sumi-ink | 墨一色 | 和・静謐 | 書・茶・禅 / 和の教室 |
| 40 | indigo-aizome | 藍染 | 和・落ち着き | 染め・織り / 民芸 / 旅館 |
| 41 | forest-moss | 森と苔 | 自然・深緑 | アウトドア / 自然体験 / 環境系 |
| 42 | ocean-blue | 海の青 | 自然・爽快 | マリン・旅 / 夏イベント / 爽やかな商材 |
| 43 | autumn-kinmokusei | 金木犀 | 自然・秋 | 季節企画 / 食・お茶 / 読み物 |
| 44 | snow-country | 雪国 | 自然・冬 | 冬の企画 / 温泉・宿 / 静かな商材 |
| 45 | desert | 砂漠 | 自然・乾いた・広い | 旅・冒険 / 乾いた世界観の作品 / ミニマル寄りの商材 |
| 46 | tea-garden | 茶畑 | 和・自然・朝 | お茶・食 / 産地・農園 / 和の教室 |
| 47 | hinoki | 檜と湯 | 和・癒やし | 温泉・宿 / 癒やし系 / 木の商材 |
| 48 | trust-navy | 信頼の紺 | ビジネス・信頼 | 士業・コンサル / BtoB / 採用 |
| 49 | fintech-emerald | エメラルドの金融 | ビジネス・堅実 | 金融・投資 / 高単価コンサル |
| 50 | blueprint | 青図面 | テック・設計 | 建築・製造 / 設計・エンジニア / 講座 |
| 51 | data-dashboard | ダッシュボード | テック・数値 | SaaS / データ・AI / BtoB |
| 52 | clinic-clean | クリニックの白 | 医療・安心 | 医療・歯科 / 整体 / 健康商材 |
| 53 | startup-blue | スタートアップ | ビジネス・勢い | SaaS・スタートアップ / 採用 / サービスLP |
| 54 | consult-charcoal | 炭のコンサル | ビジネス・重厚 | コンサル・士業 / BtoB / 高単価 |
| 55 | eco-green | サステナ | ビジネス・環境 | 環境・食 / 社会貢献 / 自然派ブランド |
| 56 | horror-west | 洋画ホラー | 怖い・映画っぽく | 作品公式サイト / イベント / ハロウィン |
| 57 | pixel-8bit | ドット絵 | ゲーム・レトロ | ゲーム / ガジェット / 楽しい商材 |
| 58 | horror-jp | Jホラー | 怖い・和・湿った | ホラー作品 / 怪談イベント / 夏の企画 |
| 59 | horror-gothic | ゴシックホラー | 怖い・耽美 | 小説・ゲーム作品 / ゴス系ブランド / イベント |
| 60 | horror-vhs | 見つかった映像 | 怖い・記録映像 | ホラー作品 / ARG・謎解き / 配信企画 |
| 61 | sf-space | 宇宙SF | SF・壮大 | SF作品 / 宇宙・科学 / 壮大な講座 |
| 62 | sf-lab | 白いSF | SF・クリーン・冷たい | テック製品 / 研究・医療AI / ミニマルなSF |
| 63 | sf-mecha | メカ・格納庫 | SF・重厚・警告 | ゲーム・ロボ作品 / ガジェット / 製造 |
| 64 | game-rpg | ファンタジーRPG | ゲーム・冒険 | ゲーム作品 / コミュニティ / 冒険系の講座 |
| 65 | game-fps | バトル・FPS | ゲーム・緊張 | ゲーム・配信 / 大会 / 熱い商材 |
| 66 | game-esports | eスポーツ | ゲーム・競技・派手 | 大会・チーム / 配信者 / ガジェット |
| 67 | anime-kinetic | アニメ・ポスター | エンタメ・熱量・斜め | アニメ・漫画作品 / イベント / 熱い告知 |
| 68 | post-apoc | 荒廃した世界 | SF・荒野・錆 | サバイバル系作品 / ゲーム / 硬派な商材 |
| 69 | steampunk | スチームパンク | SF・真鍮・歯車 | ゲーム・小説作品 / クラフト / 異世界系 |
| 70 | kaiju | 特撮 | ジャンル・巨大・熱い | 特撮・映画作品 / イベント / 熱い告知 |
| 71 | obsidian-mint | 黒曜石とミント | かっこいい・クリーン | SaaS・ツール / アプリ / 簡易HP |
| 72 | mono-minimal | 白黒ミニマル | ミニマル・上品 | ポートフォリオ / 建築・デザイン |
| 73 | gallery-white | 美術館の白 | ミニマル・アート | ポートフォリオ / 作家・写真家 / 展示 |
| 74 | morning-fog | 霧の朝 | 静か・淡い | カウンセラー / 朝活 / 読み物 |
| 75 | swiss-grid | スイス・グリッド | かっこいい・国際様式 | デザイン・制作 / 講座 / イベント |
| 76 | minimal-black | 黒ミニマル | ミニマル・黒 | ポートフォリオ / ブランド / 高単価 |
| 77 | minimal-warm | 生成りミニマル | ミニマル・温かい | 暮らし・工芸 / サロン / 自己紹介 |
| 78 | minimal-type | 文字だけ | ミニマル・タイポ | 文字主役の告知 / デザイン / 講座 |
| 79 | notebook-grid | 方眼ノート | ミニマル・道具 | ノート術・学習 / 講座 / 文具 |
| 80 | pale-air | 淡い空 | ミニマル・軽い | 軽やかなサービス / 子育て / 空気感の商材 |
| 81 | paper-black | 黒紙の写真集 | かっこいい・静か | 自己紹介 / ポートフォリオ / 写真家・作家 |
| 82 | neon-tokyo | ネオン | かっこいい・テック | ゲーム・配信者 / ガジェット / コミュニティ |
| 83 | charcoal-brass | 炭と真鍮 | かっこいい・職人 | 職人・工房 / 革・木・コーヒー / 簡易HP |
| 84 | noir-film | 白黒映画 | かっこいい・クラシック | 作家・俳優 / イベント / 作品 |
| 85 | cyber-grid | 端末の緑 | テック・ハッカー | AI・プログラミング講座 / ツール / コミュニティ |
| 86 | concrete | コンクリート | クール・硬派 | 建築・不動産 / 男性向け / 硬派な商材 |
| 87 | carbon-red | カーボン×赤 | クール・速い | 車・スポーツ / ガジェット / 速さ系 |
| 88 | street-mono | ストリート | クール・若い | アパレル / 音楽 / 若年層 |
| 89 | mode-black | モード | クール・雑誌・白黒 | アパレル・美容 / モデル / 雑誌的ブランド |
| 90 | military | ミリタリー | クール・硬派・実用 | アウトドア・ギア / 硬派なブランド / 男性向け |
| 91 | glass-blue | ガラスと青 | クール・テック・透明 | アプリ・ツール / テック製品 / AI系 |
| 92 | abyss-gold | 深海クリムゾン | ギラギラ・情報商材っぽく | セールスレター / オプトイン（煽り） |
| 93 | brutal | ブルータリズム | ギラギラ・尖った・明るい | 号外的セールスレター / イベント / 若年層 |
| 94 | gold-rush | 黒金 | ギラギラ・王道 | セールスレター / 高額商材 / ローンチ |
| 95 | red-alert | 赤ベタ | ギラギラ・セール | セール / 期間限定 / キャンペーン |
| 96 | money-green | 札束グリーン | ギラギラ・稼ぐ | 副業・投資系 / 収益化 / 高額商材 |
| 97 | flash-yellow | 黄×黒 | ギラギラ・警告 | 激安・大量 / 号外 / イベント |
| 98 | royal-purple | 紫×金 | ギラギラ・高級 | 高額コンサル / 会員制 / 占い・スピリチュアル |
| 99 | neon-sale | ネオンセール | ギラギラ・派手・夜 | セール / ナイトイベント / 若年層向け商材 |
| 100 | platinum | プラチナ | ギラギラ・高級・銀 | 会員制 / 高額商材 / 上位プラン |

---


# ダーク・壮大

## No.1 wafu-dark — 和風ダーク（和風・壮大）
```css
:root{--bg:#06070b;--bg2:#0d0f15;--card:#151821;--ink:#efe9dc;--body:#b8b2a4;--muted:#7a756b;--line:rgba(239,233,220,.12);--accent:#c0392b;--accent-2:#c9a227}
```
- 書体: Cormorant Garamond（英字・数字）/ Shippori Mincho B1（見出し）/ Zen Kaku Gothic New（本文・キャプション）
- 質感: 墨のにじみ + 火の粉
- 画像接頭辞: `dark Japanese fantasy, ukiyo-e influence meets cinematic film still, ink wash, fog, paper lantern light, muted vermilion and gold on black`
- 必須装備: 縦書き見出し / 漢数字 / 朱の割印バッジ
- 禁止: 丸ゴシック / パステル
- 使える演出: lightning / ink-splat / letters-fall（雷撃 / 墨 / 文字落下）
- 章番号の例: 壱 弐 参 / 第一幕
- KV の被写体例: `a samurai silhouette under a torii gate in fog, paper lanterns, falling embers`
- 向く用途: 作品公式サイト / イベント / 和の商材

## No.2 midnight-navy — 深夜の紺（かっこいい・落ち着き）
```css
:root{--bg:#0b1426;--bg2:#101b33;--card:#16233f;--ink:#eef1f7;--body:#b8c0d4;--muted:#7784a0;--line:rgba(238,241,247,.12);--accent:#f2c14e;--accent-2:#f2c14e}
```
- 書体: Cormorant Garamond（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 星の粒
- 画像接頭辞: `editorial photograph at midnight, deep navy blue tones, one warm desk lamp, soft film grain, calm and quiet`
- 必須装備: 星の粒 / 細い金線 / 大きな余白
- 禁止: ネオン / 太ゴシック
- 使える演出: spotlight / letters-fall / none（スポットライト / 文字落下 / なし（静止で勝つ））
- 章番号の例: Chapter 1 / 23:00
- KV の被写体例: `a person reading a letter under a desk lamp in a dark navy room, a window full of stars`
- 向く用途: 自己紹介 / コーチ・カウンセラー / 夜の商材

## No.3 deep-ocean — 深海の青（ダーク・壮大・静か）
```css
:root{--bg:#03111c;--bg2:#061a29;--card:#0a2236;--ink:#e6f3fa;--body:#a9c3d1;--muted:#6c8595;--line:rgba(230,243,250,.12);--accent:#2fc4e0;--accent-2:#8fe3ff}
```
- 書体: Cormorant Garamond（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 水面からの光の筋 + 粒
- 画像接頭辞: `deep underwater cinematic photograph, dark teal blue, light rays from the surface, floating particles, vast and quiet`
- 必須装備: 光の筋 / 青緑1色 / 深度の表記
- 禁止: 暖色の金 / 丸ゴシック
- 使える演出: spotlight / ripple / letters-fall（スポットライト / 波紋 / 文字落下）
- 章番号の例: DEPTH -200m
- KV の被写体例: `a diver silhouette far below the surface with light rays coming down`
- 向く用途: 壮大な講座 / 海・旅 / 静かな商材

## No.4 volcanic — 溶岩（ダーク・熱い）
```css
:root{--bg:#0c0806;--bg2:#150c08;--card:#1e110b;--ink:#f6ebe2;--body:#c9b3a4;--muted:#85705f;--line:rgba(246,235,226,.12);--accent:#ff5a1f;--accent-2:#ffb347}
```
- 書体: Oswald（英字・数字）/ Noto Sans JP（見出し）/ BIZ UDPGothic（本文・キャプション）
- 質感: 火の粉 + 熱のゆらぎ
- 画像接頭辞: `cinematic photograph of glowing lava cracks on black volcanic rock, orange heat glow, embers, dark`
- 必須装備: 火の粉 / 橙1色 / 温度・段階の表記
- 禁止: パステル / セリフ
- 使える演出: lightning / flare / letters-fall（雷撃 / 信号弾 / 文字落下）
- 章番号の例: PHASE 01 / 1,200℃
- KV の被写体例: `a lone figure standing on black volcanic rock facing a glowing lava river`
- 向く用途: 熱い商材 / スポーツ / 挑戦系

## No.5 storm — 嵐（ダーク・緊張）
```css
:root{--bg:#0b0e12;--bg2:#12161c;--card:#191e26;--ink:#e9edf2;--body:#aeb6c2;--muted:#6f7886;--line:rgba(233,237,242,.12);--accent:#9ecbff;--accent-2:#ffe066}
```
- 書体: Bebas Neue（英字・数字）/ Noto Sans JP（見出し）/ Noto Serif JP（本文・キャプション）
- 質感: 雨 + 雷の一瞬の白
- 画像接頭辞: `dramatic storm photograph, dark grey clouds, a single lightning bolt, rain, high contrast, cinematic wide`
- 必須装備: 雨 / 雷の一瞬の白 / 警報風の表記
- 禁止: パステル / 丸角
- 使える演出: lightning / flare / letters-fall（雷撃 / 信号弾 / 文字落下）
- 章番号の例: WARNING 01 / 風速 30m
- KV の被写体例: `a person with an umbrella on an empty road under a lightning-lit storm sky`
- 向く用途: 覚悟系の商材 / 作品 / 告知

## No.6 cinema-black — 映画の予告（ダーク・壮大・白黒）
```css
:root{--bg:#000;--bg2:#0a0a0a;--card:#111;--ink:#fff;--body:#cfcfcf;--muted:#8a8a8a;--line:rgba(255,255,255,.14);--accent:#fff;--accent-2:#c9c9c9}
```
- 書体: Bebas Neue（英字・数字）/ Noto Sans JP（見出し）/ Cormorant Garamond（本文・キャプション）
- 質感: レターボックスの黒帯 + グレイン
- 画像接頭辞: `black and white cinematic trailer still, widescreen letterbox, high contrast, film grain, dramatic`
- 必須装備: 黒帯（上下） / 白黒のみ / 公開日の表記
- 禁止: 色 / 丸角
- 使える演出: letters-fall / spotlight / glitch-title（文字落下 / スポットライト / グリッチ）
- 章番号の例: COMING SOON / 2026.09
- KV の被写体例: `a man walking away down a rainy street at night, widescreen`
- 向く用途: 作品告知 / イベント / ローンチ

## No.7 aurora — オーロラ（ダーク・壮大・幻想）
```css
:root{--bg:#050a14;--bg2:#091120;--card:#0e182c;--ink:#eaf2ff;--body:#b4c4dc;--muted:#6f7f9a;--line:rgba(234,242,255,.12);--accent:#5ef0b0;--accent-2:#b388ff}
```
- 書体: Cormorant Garamond（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: オーロラの帯 + 星
- 画像接頭辞: `aurora borealis over a snowy field at night, green and violet light curtains, stars, wide, quiet`
- 必須装備: 緑と紫の光の帯 / 星の粒 / 静かな余白
- 禁止: 赤 / 丸ゴシック
- 使える演出: spotlight / ripple / letters-fall（スポットライト / 波紋 / 文字落下）
- 章番号の例: NIGHT 01 / 68°N
- KV の被写体例: `a person standing in a snowy field watching green aurora curtains`
- 向く用途: 旅・北欧 / 壮大な講座 / 幻想系の作品

## No.8 eclipse — 日蝕（ダーク・壮大・儀式）
```css
:root{--bg:#000;--bg2:#070707;--card:#0f0f0f;--ink:#f5f2ea;--body:#c4c0b4;--muted:#7e7b72;--line:rgba(245,242,234,.12);--accent:#f2d58a;--accent-2:#f5f2ea}
```
- 書体: Cinzel（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: コロナの輪 + グレイン
- 画像接頭辞: `total solar eclipse, black sun with a thin white-gold corona ring, dark desert, cinematic, awe`
- 必須装備: 輪は1つ / 白金の細線 / 時刻の表記
- 禁止: パステル / 丸角
- 使える演出: spotlight / letters-fall / flare（スポットライト / 文字落下 / 信号弾）
- 章番号の例: TOTALITY 02:14
- KV の被写体例: `a crowd silhouette watching a total solar eclipse in a dark desert`
- 向く用途: ローンチ / 作品 / 一度きりのイベント


# 明るい・上品

## No.9 paper-white — 紙・エディトリアル（上品・信頼）
```css
:root{--bg:#f7f6f2;--bg2:#efede7;--card:#fff;--ink:#1c1b18;--body:#3f3d38;--muted:#8a8780;--line:#d9d6ce;--accent:#1f3a5f;--accent-2:#1f3a5f}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 紙の繊維
- 画像接頭辞: `editorial film photograph, natural window light, muted tones, Kodak Portra grain, quiet composition, lots of negative space, bright airy`
- 必須装備: 罫線 / ドロップキャップ / 大余白
- 禁止: 黒背景 / グロー / グレイン
- 使える演出: tear / none（紙を破く / なし（静止で勝つ））
- 章番号の例: p. 02 / Vol. 01
- KV の被写体例: `a bright white studio with a single wooden chair and a tall window, morning light`
- 向く用途: 簡易HP（士業・医療）/ 自己紹介

## No.10 ivory-serif — 象牙のセリフ（上品・高級）
```css
:root{--bg:#f4efe6;--bg2:#ede6d8;--card:#fff;--ink:#221c14;--body:#4a4238;--muted:#8f867a;--line:#d8d0c2;--accent:#8a6d3b;--accent-2:#8a6d3b}
```
- 書体: Cormorant Garamond（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし（余白）
- 画像接頭辞: `luxury still life on ivory linen, soft diffused daylight, champagne gold accents, editorial, refined`
- 必須装備: 細いセリフの大見出し / 小さな金の飾り罫 / イタリック
- 禁止: 太ゴシック / 原色
- 使える演出: none / tear（なし（静止で勝つ） / 紙を破く）
- 章番号の例: I / II / III
- KV の被写体例: `a woman in an ivory silk dress seen from behind in a bright salon, champagne gold details`
- 向く用途: 高単価サービス / サロン / ブライダル

## No.11 linen-sage — 麻とセージ（自然派・やさしい）
```css
:root{--bg:#f3f1ea;--bg2:#e9e6dc;--card:#fff;--ink:#2f3a30;--body:#4f5a4f;--muted:#8b948b;--line:#d6d9cf;--accent:#6f8f6a;--accent-2:#6f8f6a}
```
- 書体: Fraunces（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 麻の織り
- 画像接頭辞: `natural lifestyle photography, sage green and linen tones, soft daylight, plants and ceramics, calm`
- 必須装備: 麻の質感 / 丸みのある見出し / 葉の色1つ
- 禁止: 黒背景 / ネオン
- 使える演出: ripple / none / stamp（波紋 / なし（静止で勝つ） / スタンプ）
- 章番号の例: Step 01
- KV の被写体例: `a yoga mat on a linen floor next to a potted plant, morning daylight`
- 向く用途: ヨガ・食・暮らし / 教室 / 簡易HP

## No.12 porcelain-blue — 白磁と藍（上品・和洋）
```css
:root{--bg:#f8f8f6;--bg2:#eef1f3;--card:#fff;--ink:#1b2a44;--body:#3d4a63;--muted:#8590a3;--line:#d7dde5;--accent:#1f4e8c;--accent-2:#1f4e8c}
```
- 書体: Cormorant Garamond（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 陶器の釉薬
- 画像接頭辞: `white porcelain and indigo blue still life, soft north light, ceramic glaze texture, refined and calm`
- 必須装備: 藍の細線 / 白磁のような余白 / 縦書きの小見出し
- 禁止: 原色 / グレイン
- 使える演出: ripple / tear / none（波紋 / 紙を破く / なし（静止で勝つ））
- 章番号の例: 一 / 二 / 三
- KV の被写体例: `a white porcelain bowl with indigo pattern on a wooden table, north light`
- 向く用途: 工芸 / 器・食 / 旅館

## No.13 letterpress — 活版印刷（上品・クラフト）
```css
:root{--bg:#f5efe3;--bg2:#ece4d4;--card:#fff9ee;--ink:#2b241c;--body:#4e453a;--muted:#8c8273;--line:#d9d0bf;--accent:#a63d2f;--accent-2:#a63d2f}
```
- 書体: Libre Baskerville（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 活版の凹み・インクのかすれ
- 画像接頭辞: `letterpress printed card on thick cream cotton paper, deep impression, single red ink, macro`
- 必須装備: かすれた文字 / 罫線と飾り罫 / 番号スタンプ
- 禁止: グロー / ネオン
- 使える演出: stamp / tear / none（スタンプ / 紙を破く / なし（静止で勝つ））
- 章番号の例: № 1 / 1st Edition
- KV の被写体例: `a stack of letterpress printed cards with a red wax seal on cream paper`
- 向く用途: 文具・紙もの / 書籍・出版 / 招待

## No.14 newspaper — 新聞（かっこいい・報道）
```css
:root{--bg:#f6f4ef;--bg2:#ebe8e1;--card:#fff;--ink:#111;--body:#333;--muted:#777;--line:#111;--accent:#c8102e;--accent-2:#c8102e}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 新聞のインク
- 画像接頭辞: `vintage newspaper front page on a desk, black ink on off-white newsprint, one red headline, halftone photo`
- 必須装備: 段組 / 太い横罫線 / 赤は見出し1つ
- 禁止: 丸角 / パステル
- 使える演出: stamp / letters-fall（スタンプ / 文字落下）
- 章番号の例: 第1面 / 号外
- KV の被写体例: `a folded vintage newspaper on a cafe table with a cup of coffee, one red headline block`
- 向く用途: 号外的セールスレター / ニュース系発信

## No.15 botanical — 植物図鑑（上品・クラシック・自然）
```css
:root{--bg:#f7f4ea;--bg2:#efeadb;--card:#fff;--ink:#1f2f22;--body:#41503f;--muted:#8a927f;--line:#d8d3c2;--accent:#1f5b3a;--accent-2:#b8402e}
```
- 書体: Libre Baskerville（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 古い図鑑の紙 + 銅版画の線
- 画像接頭辞: `vintage botanical illustration of a fern and leaves on cream paper, copperplate engraving, muted green`
- 必須装備: 銅版画風の線 / 学名のような小さなラベル / 深緑1色
- 禁止: ネオン / 太ゴシック
- 使える演出: tear / none / ripple（紙を破く / なし（静止で勝つ） / 波紋）
- 章番号の例: Fig. 12 / Pl. Ⅲ
- KV の被写体例: `an open vintage botanical book on a wooden table with a pressed fern`
- 向く用途: 植物・ハーブ / 教室 / 上品な自然系

## No.16 marble — 大理石（上品・高級・白）
```css
:root{--bg:#f8f7f5;--bg2:#f0eeeb;--card:#fff;--ink:#1a1a1a;--body:#4a4a4a;--muted:#8f8f8f;--line:#dedbd6;--accent:#1a1a1a;--accent-2:#b89b5e}
```
- 書体: Cormorant Garamond（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 大理石の筋
- 画像接頭辞: `white marble surface with grey veins, a single gold ring and soft shadow, luxury product photography`
- 必須装備: 大理石の筋 / 金は細線1本 / 細いセリフ
- 禁止: ビビッド / 丸角
- 使える演出: none / tear / spotlight（なし（静止で勝つ） / 紙を破く / スポットライト）
- 章番号の例: Ⅰ / Ⅱ
- KV の被写体例: `a woman's hand placing a gold ring on a white marble table`
- 向く用途: ジュエリー / サロン / 高単価サービス

## No.17 kraft — クラフト紙（上品・素朴・手仕事）
```css
:root{--bg:#d9c3a0;--bg2:#cfb68e;--card:#e8d8bb;--ink:#2b2218;--body:#4f4232;--muted:#8a7a63;--line:#bfa987;--accent:#1d1d1d;--accent-2:#b8402e}
```
- 書体: Fraunces（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: クラフト紙の繊維 + スタンプ
- 画像接頭辞: `fresh bread wrapped in brown kraft paper with a black rubber stamp, warm daylight, rustic`
- 必須装備: クラフト紙の面 / 黒のスタンプ / 紐・タグ
- 禁止: ネオン / グラデ
- 使える演出: stamp / tear / none（スタンプ / 紙を破く / なし（静止で勝つ））
- 章番号の例: No. 01 / LOT
- KV の被写体例: `a bakery counter with loaves wrapped in kraft paper and black stamps`
- 向く用途: パン・食品 / 手仕事 / ギフト


# かわいい・ポップ

## No.18 pastel-pop — 白地パステル（かわいい・明るい）
```css
:root{--bg:#fffdf8;--bg2:#fff;--card:#fff;--ink:#3d3552;--body:#5b5470;--muted:#8f89a3;--line:rgba(61,53,82,.1);--accent:#ff7f9f;--accent-2:#5cc9a0}
```
- 書体: Fredoka（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし
- 画像接頭辞: `cute 3D clay render, soft matte materials, pastel mint pink and lemon palette, soft studio lighting, rounded shapes, playful, clean bright background`
- 必須装備: スライドごとの背景色遷移 / 白カード / 丸バッジ
- 禁止: 黒背景 / グレイン
- 使える演出: stamp / card-flip / ripple（スタンプ / カード裏返し / 波紋）
- 章番号の例: 1 / 7、STEP 1
- KV の被写体例: `a cheerful young woman jumping with a notebook, pastel background`
- 向く用途: オプトイン / 教室・サロン

## No.19 pastel-pop-dark — 黒地パステルクレイ（かわいい・でも大人っぽく）
```css
:root{--bg:#15131c;--bg2:#1c1925;--card:#221f2d;--ink:#fff8ee;--body:#cfc9dc;--muted:#8d879f;--line:rgba(255,255,255,.08);--accent:#ff6f91;--accent-2:#4fd1a3}
```
- 書体: Fredoka（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし
- 画像接頭辞: `cute 3D clay render, soft matte materials, pastel mint pink and lemon objects on a dark charcoal background, soft studio lighting, rounded shapes, playful`
- 必須装備: ブロブ形マスクの画像 / 厚み影ボタン / 漂うクレイ玉
- 禁止: グレイン / グリッチ / 明朝
- 使える演出: stamp / card-flip / ripple（スタンプ / カード裏返し / 波紋）
- 章番号の例: 1 / 7、DAY 1
- KV の被写体例: `a small clay character hugging a coin jar, pastel objects floating around`
- 向く用途: オプトイン / リンクまとめ / 講座

## No.20 candy-shop — キャンディショップ（かわいい・ビビッド）
```css
:root{--bg:#fff5fa;--bg2:#ffe9f3;--card:#fff;--ink:#3b1f3a;--body:#5c3d5a;--muted:#9a7f98;--line:#f3d3e3;--accent:#ff3d8a;--accent-2:#3dd6ff}
```
- 書体: Fredoka（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: ドット
- 画像接頭辞: `candy shop product photography, vivid pink and cyan, glossy plastic, playful, bright`
- 必須装備: ビビッド2色 / ドット背景 / 丸いバッジ
- 禁止: 黒 / セリフ
- 使える演出: ripple / stamp / card-flip（波紋 / スタンプ / カード裏返し）
- 章番号の例: No.1 / 2 / 3
- KV の被写体例: `glossy pink and cyan candies spilling out of a glass jar`
- 向く用途: 雑貨・コスメ / 若年層 / イベント

## No.21 sakura — 桜（かわいい・和・春）
```css
:root{--bg:#fff8f9;--bg2:#fdeef2;--card:#fff;--ink:#3a2b30;--body:#5e4a52;--muted:#9b878e;--line:#f1dbe1;--accent:#e8879e;--accent-2:#7fb58a}
```
- 書体: Zen Maru Gothic（英字・数字）/ Klee One（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 花びらの散り
- 画像接頭辞: `cherry blossom season, soft pink petals, pale spring light, gentle bokeh, Japanese spring`
- 必須装備: 花びらの粒 / 淡い桃色1つ / 手描き風の罫線
- 禁止: 黒 / ネオン
- 使える演出: ripple / stamp / tear（波紋 / スタンプ / 紙を破く）
- 章番号の例: 春 / 一 / 二
- KV の被写体例: `a girl in a white blouse under blooming cherry trees, petals falling`
- 向く用途: 春の企画 / 教室 / 和菓子

## No.22 kawaii-sticker — シール風（かわいい・元気）
```css
:root{--bg:#fff;--bg2:#fff7e0;--card:#fff;--ink:#1c1c1c;--body:#333;--muted:#777;--line:#1c1c1c;--accent:#ffcc00;--accent-2:#ff5a5f}
```
- 書体: Fredoka（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 太い黒縁
- 画像接頭辞: `sticker sheet illustration, thick black outlines, flat bright colors, die-cut white border, playful`
- 必須装備: 太い黒縁 / 白フチ / 傾けた配置
- 禁止: セリフ / グレイン
- 使える演出: stamp / card-flip / letters-fall（スタンプ / カード裏返し / 文字落下）
- 章番号の例: 01! / 02!
- KV の被写体例: `a cute cat character waving, thick outlines, die-cut white border`
- 向く用途: 子ども向け / イベント / 楽しい商材

## No.23 macaron — マカロン（かわいい・上品）
```css
:root{--bg:#fffbf7;--bg2:#f9f1ea;--card:#fff;--ink:#4a3a3a;--body:#6b5a5a;--muted:#a29090;--line:#eadcd6;--accent:#e7a0b6;--accent-2:#a8c9c0}
```
- 書体: Cormorant Garamond（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし
- 画像接頭辞: `macaron tower on a pastel table, milky pink mint and lavender, soft studio light, patisserie photography`
- 必須装備: ミルキーな3色 / 細いセリフ英字 / 丸角カード
- 禁止: 黒 / 太い縁
- 使える演出: ripple / none / card-flip（波紋 / なし（静止で勝つ） / カード裏返し）
- 章番号の例: No. 01
- KV の被写体例: `a tower of pastel macarons on a marble table next to a small gift box`
- 向く用途: パティスリー / ギフト / 女性向けサロン

## No.24 picnic-gingham — ピクニック（かわいい・素朴）
```css
:root{--bg:#fffdf7;--bg2:#fff3f3;--card:#fff;--ink:#3b2c2c;--body:#5c4a4a;--muted:#9a8888;--line:#ead9d9;--accent:#d94b4b;--accent-2:#4c8b4c}
```
- 書体: Fraunces（英字・数字）/ Zen Maru Gothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 赤白のギンガムチェック
- 画像接頭辞: `picnic on a red and white gingham cloth, sunlight, homemade food, warm and cozy`
- 必須装備: ギンガムの帯 / 手書き風見出し / 丸いシール
- 禁止: 黒 / ネオン
- 使える演出: stamp / ripple / none（スタンプ / 波紋 / なし（静止で勝つ））
- 章番号の例: Menu 01
- KV の被写体例: `a picnic basket, bread and lemonade on a red gingham cloth in sunlight`
- 向く用途: カフェ・食 / 手作り / 週末イベント

## No.25 pop-art — ポップアート（ポップ・コミック）
```css
:root{--bg:#fff;--bg2:#fff2b3;--card:#fff;--ink:#111;--body:#222;--muted:#666;--line:#111;--accent:#ff2e63;--accent-2:#1e90ff}
```
- 書体: Bangers（英字・数字）/ M PLUS 1p（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: ハーフトーンドット
- 画像接頭辞: `pop art comic style illustration, halftone dots, bold black outlines, primary colors, speech bubble`
- 必須装備: ハーフトーン / 吹き出し / 太い黒縁の見出し
- 禁止: セリフ / 淡色
- 使える演出: stamp / letters-fall / card-flip（スタンプ / 文字落下 / カード裏返し）
- 章番号の例: #01 / POW!
- KV の被写体例: `a woman's face with a big speech bubble, halftone dots, comic style`
- 向く用途: イベント / エンタメ / 若年層

## No.26 cream-soda — クリームソーダ（かわいい・レトロ喫茶）
```css
:root{--bg:#f3fbf6;--bg2:#e6f6ea;--card:#fff;--ink:#1f3a2e;--body:#3f5a4d;--muted:#8aa596;--line:#cfe3d6;--accent:#2ec27e;--accent-2:#ff5a5f}
```
- 書体: Righteous（英字・数字）/ Kosugi Maru（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 泡の粒
- 画像接頭辞: `cream soda in a tall glass at a retro Japanese cafe, emerald green and cherry red, soft window light`
- 必須装備: 泡の粒 / エメラルド1色 / 丸い赤のさくらんぼ
- 禁止: 黒 / 太ゴシック
- 使える演出: ripple / card-flip / stamp（波紋 / カード裏返し / スタンプ）
- 章番号の例: No.1 / 2
- KV の被写体例: `a tall cream soda with a cherry on a retro cafe counter, window light`
- 向く用途: 喫茶・スイーツ / レトロ雑貨

## No.27 shojo-manga — 少女漫画（かわいい・キラキラ）
```css
:root{--bg:#fff;--bg2:#fff3f7;--card:#fff;--ink:#3a2a34;--body:#5e4c57;--muted:#9c8a95;--line:#f1d8e2;--accent:#ff7fb0;--accent-2:#7fd3ff}
```
- 書体: Zen Maru Gothic（英字・数字）/ Klee One（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: スクリーントーン + キラキラ
- 画像接頭辞: `shojo manga style illustration, sparkling eyes, screentone dots, flowers and sparkles, pastel pink`
- 必須装備: スクリーントーン / キラキラの粒 / 吹き出し風の見出し
- 禁止: 黒背景 / セリフ
- 使える演出: stamp / card-flip / ripple（スタンプ / カード裏返し / 波紋）
- 章番号の例: 第1話 / ♡
- KV の被写体例: `a girl with sparkling eyes holding a letter, shojo manga style, pastel`
- 向く用途: 少女向け / 恋愛系 / 推し活

## No.28 yumekawa — ゆめかわ（かわいい・夢）
```css
:root{--bg:#f6f0ff;--bg2:#ece3ff;--card:#fff;--ink:#4a3a6b;--body:#6d5e8c;--muted:#a396bf;--line:#e2d6f5;--accent:#c48bff;--accent-2:#8fe3d9}
```
- 書体: Fredoka（英字・数字）/ M PLUS Rounded 1c（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 雲 + 星の粒
- 画像接頭辞: `dreamy pastel clouds and a soft rainbow over a lavender sky, sparkles, cute, airy`
- 必須装備: 雲の形 / ラベンダー×ミント / 星の粒
- 禁止: 黒 / 太ゴシック
- 使える演出: ripple / card-flip / stamp（波紋 / カード裏返し / スタンプ）
- 章番号の例: 1 / 7 ☆
- KV の被写体例: `a pastel unicorn plush on a cloud-shaped cushion, lavender room`
- 向く用途: 雑貨・コスメ / 若年層 / 癒やし系


# レトロ

## No.29 retro-future — レトロフューチャー（レトロ・ポップ）
```css
:root{--bg:#f3e9d2;--bg2:#e9dcc0;--card:#fff8ea;--ink:#2b1d14;--body:#4a3a2e;--muted:#8a7a6a;--line:rgba(43,29,20,.18);--accent:#e0662f;--accent-2:#3f7d6a}
```
- 書体: Righteous（英字・数字）/ Kosugi Maru（見出し）/ Zen Kaku Gothic Antique（本文・キャプション）
- 質感: 放射線 + グレイン
- 画像接頭辞: `1970s sci-fi poster art, airbrush illustration, warm cream orange and brown palette, grain, retro futurism`
- 必須装備: 放射線 / ストライプ帯 / 太陽のバッジ
- 禁止: ネオン / 黒背景
- 使える演出: card-flip / ripple / stamp（カード裏返し / 波紋 / スタンプ）
- 章番号の例: PHASE 1、No.01
- KV の被写体例: `a rounded retro rocket flying over a desert city`
- 向く用途: 商品LP / イベント / カフェ

## No.30 showa-kissa — 昭和喫茶（レトロ・和）
```css
:root{--bg:#f4ecdc;--bg2:#eadfc8;--card:#fff8e8;--ink:#2c2017;--body:#4b3d30;--muted:#8c7d6b;--line:#d9cbb4;--accent:#7a4b2a;--accent-2:#2f5d4a}
```
- 書体: Zen Old Mincho（英字・数字）/ Kosugi Maru（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 木目 + 色あせ
- 画像接頭辞: `showa era Japanese cafe interior, dark wood, deep green velvet, cream walls, warm tungsten light, film photo`
- 必須装備: 木目 / 深緑1色 / 縦書きのメニュー
- 禁止: ネオン / パステル
- 使える演出: stamp / tear / none（スタンプ / 紙を破く / なし（静止で勝つ））
- 章番号の例: 其の一 / 品書き
- KV の被写体例: `a cup of coffee and a slice of pudding on a dark wood table, green velvet seat behind`
- 向く用途: 喫茶・食 / 純喫茶的な商材

## No.31 vapor-80s — ヴェイパーウェーブ（レトロ・80年代）
```css
:root{--bg:#1a0b2e;--bg2:#2a1245;--card:#341a56;--ink:#ffe6fb;--body:#e9b8ff;--muted:#a87fcf;--line:rgba(255,230,251,.14);--accent:#ff71ce;--accent-2:#01cdfe}
```
- 書体: Orbitron（英字・数字）/ M PLUS 1p（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: グリッドの地平線
- 画像接頭辞: `80s vaporwave aesthetic, sunset gradient of pink and purple, neon grid horizon, retro computer, palm silhouettes`
- 必須装備: グリッドの地平線 / ピンク×シアン / 日本語の飾り文字
- 禁止: セリフ / 紙の質感
- 使える演出: glitch-title / neon-power / ripple（グリッチ / ネオン点灯 / 波紋）
- 章番号の例: 1 9 8 4
- KV の被写体例: `a chrome statue bust between palm trees, pink sunset and neon grid horizon`
- 向く用途: 音楽・アート / 若年層 / イベント

## No.32 y2k-chrome — Y2K クローム（レトロ・未来）
```css
:root{--bg:#e9f2ff;--bg2:#dbe8ff;--card:#fff;--ink:#0b1a33;--body:#2a3a5c;--muted:#7a89a8;--line:#c9d6ee;--accent:#3b82f6;--accent-2:#c0c0c0}
```
- 書体: Orbitron（英字・数字）/ M PLUS 1p（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: クロームの反射
- 画像接頭辞: `y2k aesthetic, chrome metallic objects, baby blue and silver, glossy reflections, early 2000s`
- 必須装備: クロームの見出し / 水色1色 / 丸いボタン
- 禁止: 紙の質感 / セリフ
- 使える演出: ripple / card-flip / glitch-title（波紋 / カード裏返し / グリッチ）
- 章番号の例: 2000 / 01
- KV の被写体例: `a chrome flip phone and silver headphones on a baby blue background`
- 向く用途: ファッション / 音楽 / 若年層

## No.33 riso-poster — リソグラフ（レトロ・印刷）
```css
:root{--bg:#fbf7ee;--bg2:#f3ecdc;--card:#fff;--ink:#1c1c1c;--body:#333;--muted:#777;--line:#1c1c1c;--accent:#ff4fa3;--accent-2:#2f6df6}
```
- 書体: Archivo Black（英字・数字）/ BIZ UDPGothic（見出し）/ Space Mono（本文・キャプション）
- 質感: リソのざらつき + 版ズレ
- 画像接頭辞: `risograph print poster, fluorescent pink and blue overprint, grainy texture, misregistration, bold shapes`
- 必須装備: 蛍光2色の重ね / 版ズレ / ざらつき
- 禁止: グラデ / 写実
- 使える演出: stamp / letters-fall / card-flip（スタンプ / 文字落下 / カード裏返し）
- 章番号の例: No.01 / 2色
- KV の被写体例: `a risograph poster of a bicycle in fluorescent pink and blue`
- 向く用途: デザイン・ZINE / イベント / 若年層

## No.34 vintage-map — 古地図（レトロ・旅）
```css
:root{--bg:#efe4cf;--bg2:#e6d8bc;--card:#f8f0de;--ink:#2e2415;--body:#4d3f2a;--muted:#8a7b62;--line:#d4c5a5;--accent:#8b3a2a;--accent-2:#2f5f6b}
```
- 書体: Libre Baskerville（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 羊皮紙
- 画像接頭辞: `antique sepia map with compass rose and hand-drawn coastlines, aged paper texture, warm light`
- 必須装備: 羊皮紙 / 方位記号 / 点線の航路
- 禁止: ネオン / 黒背景
- 使える演出: tear / stamp / none（紙を破く / スタンプ / なし（静止で勝つ））
- 章番号の例: Ⅰ / Ⅱ / Ⅲ
- KV の被写体例: `a brass compass and a rolled antique map on a wooden ship deck`
- 向く用途: 旅・ツアー / 冒険系の講座 / 読み物

## No.35 film-camera — フィルム写真（レトロ・ノスタルジー）
```css
:root{--bg:#f7f1e6;--bg2:#efe6d6;--card:#fff;--ink:#2b2520;--body:#4f463d;--muted:#8c8377;--line:#dccfbc;--accent:#d2691e;--accent-2:#d2691e}
```
- 書体: Fraunces（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: フィルムの粒子 + 光漏れ
- 画像接頭辞: `golden hour film photograph, light leaks, warm orange tones, nostalgic, grainy`
- 必須装備: 光漏れ / 日付の焼き込み / 粒子
- 禁止: ネオン / 黒背景
- 使える演出: tear / ripple / none（紙を破く / 波紋 / なし（静止で勝つ））
- 章番号の例: '26 09 04
- KV の被写体例: `two friends walking on a summer road at golden hour, light leaks`
- 向く用途: 写真家 / 旅 / 思い出系の商材

## No.36 showa-pop — 昭和ポップ（レトロ・60年代）
```css
:root{--bg:#fff3d6;--bg2:#f7e6b8;--card:#fff9e8;--ink:#3b2414;--body:#5c3d2a;--muted:#9a7d63;--line:#e0cba0;--accent:#f26b1d;--accent-2:#2f7a5a}
```
- 書体: Righteous（英字・数字）/ Kosugi Maru（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 花柄 + 太い縁取り
- 画像接頭辞: `1960s Japanese living room with a bold floral pattern, orange telephone, cream and brown, retro pop`
- 必須装備: 花柄の帯 / 橙1色 / 丸い太縁の見出し
- 禁止: ネオン / 黒背景
- 使える演出: card-flip / stamp / ripple（カード裏返し / スタンプ / 波紋）
- 章番号の例: 第1回 / No.1
- KV の被写体例: `a woman in a 1960s dress in a room with bold floral wallpaper, orange tones`
- 向く用途: 雑貨・喫茶 / 昭和イベント / レトロ商材

## No.37 art-deco — アールデコ（レトロ・華麗）
```css
:root{--bg:#0f0e0c;--bg2:#171512;--card:#1f1c17;--ink:#f3ead8;--body:#c9bfa8;--muted:#857c69;--line:rgba(243,234,216,.14);--accent:#d4b46a;--accent-2:#f3ead8}
```
- 書体: Cinzel（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 扇形の幾何模様 + 金の線
- 画像接頭辞: `art deco hotel lobby with gold geometric fan patterns, black and cream, 1920s glamour`
- 必須装備: 扇形の幾何模様 / 金の細線 / 大文字の英字
- 禁止: 丸角 / パステル
- 使える演出: letters-fall / spotlight / card-flip（文字落下 / スポットライト / カード裏返し）
- 章番号の例: No. 1 / 1925
- KV の被写体例: `a couple in evening wear at an art deco hotel bar, gold and black`
- 向く用途: ホテル・バー / ブライダル / 華やかなイベント


# 和・自然

## No.38 watercolor — 水彩・手描き（やさしい・手づくり）
```css
:root{--bg:#fbfaf6;--bg2:#f2efe6;--card:#fff;--ink:#1f2a44;--body:#3d4560;--muted:#8a8f9e;--line:rgba(31,42,68,.14);--accent:#c0392b;--accent-2:#1f5fa8}
```
- 書体: Caveat（英字・数字）/ Klee One（見出し）/ Zen Kurenaido（本文・キャプション）
- 質感: にじみ + 紙
- 画像接頭辞: `watercolor illustration, ink outline, paper texture, soft washes, hand drawn`
- 必須装備: にじみマスク / 手描き矢印 / 紙テクスチャ
- 禁止: 黒背景 / ネオン
- 使える演出: tear / ripple / stamp（紙を破く / 波紋 / スタンプ）
- 章番号の例: 一、二、三
- KV の被写体例: `a watercolor illustration of a small house with a garden and a bicycle`
- 向く用途: 教室・ハンドメイド / 絵本・エッセイ

## No.39 sumi-ink — 墨一色（和・静謐）
```css
:root{--bg:#f6f5f0;--bg2:#eeece5;--card:#fff;--ink:#141414;--body:#333;--muted:#888;--line:#d8d6cf;--accent:#141414;--accent-2:#141414}
```
- 書体: Shippori Mincho B1（英字・数字）/ Zen Old Mincho（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 墨のかすれ
- 画像接頭辞: `sumi-e ink painting, single black ink on white washi paper, brush strokes, minimal`
- 必須装備: 縦書き / 墨のかすれ / 余白
- 禁止: 色 / 丸ゴシック
- 使える演出: tear / letters-fall / none（紙を破く / 文字落下 / なし（静止で勝つ））
- 章番号の例: 一 / 二 / 三
- KV の被写体例: `a sumi-e ink painting of a single crane standing in water`
- 向く用途: 書・茶・禅 / 和の教室

## No.40 indigo-aizome — 藍染（和・落ち着き）
```css
:root{--bg:#0e1f3a;--bg2:#132a4d;--card:#1a355e;--ink:#eef3fa;--body:#b9c6dc;--muted:#7c8ea9;--line:rgba(238,243,250,.12);--accent:#e8dcc0;--accent-2:#e8dcc0}
```
- 書体: Shippori Mincho B1（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 布の織り
- 画像接頭辞: `indigo dyed fabric texture, deep blue with white shibori patterns, natural light, Japanese craft`
- 必須装備: 布の織り / 生成りの文字 / 絞りの模様
- 禁止: ネオン / 原色
- 使える演出: tear / ripple / none（紙を破く / 波紋 / なし（静止で勝つ））
- 章番号の例: 一 / 二
- KV の被写体例: `indigo-dyed fabric hanging to dry in a wooden workshop, sunlight through the door`
- 向く用途: 染め・織り / 民芸 / 旅館

## No.41 forest-moss — 森と苔（自然・深緑）
```css
:root{--bg:#0f1a12;--bg2:#15231a;--card:#1b2d21;--ink:#e9f0e6;--body:#b7c6b6;--muted:#748a77;--line:rgba(233,240,230,.12);--accent:#9ad17a;--accent-2:#9ad17a}
```
- 書体: Fraunces（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 木漏れ日
- 画像接頭辞: `deep forest with moss and soft light rays, dark green tones, misty, nature photography`
- 必須装備: 木漏れ日のグラデ / 緑1色 / 木目の罫線
- 禁止: ネオン / ピンク
- 使える演出: ripple / spotlight / none（波紋 / スポットライト / なし（静止で勝つ））
- 章番号の例: Trail 01
- KV の被写体例: `a hiker standing in a mossy forest with light rays through the trees`
- 向く用途: アウトドア / 自然体験 / 環境系

## No.42 ocean-blue — 海の青（自然・爽快）
```css
:root{--bg:#f4fbff;--bg2:#e6f4fc;--card:#fff;--ink:#0b2a45;--body:#2c4a66;--muted:#7c95ad;--line:#cfe3f0;--accent:#0a84ff;--accent-2:#ffb703}
```
- 書体: Fraunces（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 波の線
- 画像接頭辞: `bright ocean and white sand, clear blue water, summer sunlight, wide and airy`
- 必須装備: 波の線 / 青1色 / 白い大余白
- 禁止: 黒背景 / グレイン
- 使える演出: ripple / none / letters-fall（波紋 / なし（静止で勝つ） / 文字落下）
- 章番号の例: Wave 01
- KV の被写体例: `a surfer walking on white sand toward clear blue water, wide shot`
- 向く用途: マリン・旅 / 夏イベント / 爽やかな商材

## No.43 autumn-kinmokusei — 金木犀（自然・秋）
```css
:root{--bg:#fbf6ee;--bg2:#f5ecdd;--card:#fff;--ink:#3a2a1a;--body:#5c4a36;--muted:#9a8b78;--line:#e3d6c2;--accent:#e07a1f;--accent-2:#6d4c2b}
```
- 書体: Fraunces（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 落ち葉
- 画像接頭辞: `autumn afternoon, orange osmanthus flowers and warm golden light, soft focus, cozy`
- 必須装備: 橙1色 / 落ち葉の粒 / 温かい影
- 禁止: ネオン / 黒背景
- 使える演出: ripple / tear / none（波紋 / 紙を破く / なし（静止で勝つ））
- 章番号の例: 秋 / 一
- KV の被写体例: `a cup of tea by a window with orange osmanthus branches, autumn light`
- 向く用途: 季節企画 / 食・お茶 / 読み物

## No.44 snow-country — 雪国（自然・冬）
```css
:root{--bg:#f7f9fb;--bg2:#eef2f6;--card:#fff;--ink:#1f2933;--body:#3e4c59;--muted:#8a98a8;--line:#d9e1ea;--accent:#c62828;--accent-2:#c62828}
```
- 書体: Shippori Mincho B1（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 雪の粒
- 画像接頭辞: `snow country landscape, white and pale grey, a single red element, quiet winter light`
- 必須装備: 雪の粒 / 赤1点 / 静かな余白
- 禁止: ネオン / パステル
- 使える演出: ripple / none / tear（波紋 / なし（静止で勝つ） / 紙を破く）
- 章番号の例: 冬 / 一
- KV の被写体例: `a red-roofed hut in a wide snowy field, quiet winter light`
- 向く用途: 冬の企画 / 温泉・宿 / 静かな商材

## No.45 desert — 砂漠（自然・乾いた・広い）
```css
:root{--bg:#f3e6d0;--bg2:#ead9bc;--card:#fff8ec;--ink:#3b2a1a;--body:#5f4a33;--muted:#9a8467;--line:#d9c6a6;--accent:#c8642b;--accent-2:#5b8fb9}
```
- 書体: Fraunces（英字・数字）/ Noto Sans JP（見出し）/ Noto Serif JP（本文・キャプション）
- 質感: 砂の粒 + 長い影
- 画像接頭辞: `sand dunes at sunrise with long shadows, warm beige and terracotta, wide and empty`
- 必須装備: 砂色の面 / 長い影 / テラコッタ1色
- 禁止: ネオン / 黒背景
- 使える演出: ripple / none / letters-fall（波紋 / なし（静止で勝つ） / 文字落下）
- 章番号の例: DAY 01 / 42°C
- KV の被写体例: `a lone traveler walking across sand dunes at sunrise`
- 向く用途: 旅・冒険 / 乾いた世界観の作品 / ミニマル寄りの商材

## No.46 tea-garden — 茶畑（和・自然・朝）
```css
:root{--bg:#f4f6ee;--bg2:#e9eedc;--card:#fff;--ink:#1f3322;--body:#3f5240;--muted:#889a86;--line:#d3dcc8;--accent:#2f6b3c;--accent-2:#8a5a2b}
```
- 書体: Shippori Mincho B1（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 茶畑の畝の線 + 朝霧
- 画像接頭辞: `rows of a green tea plantation in morning mist, soft light, Japanese countryside`
- 必須装備: 畝の線 / 深緑1色 / 朝霧のグラデ
- 禁止: ネオン / 黒背景
- 使える演出: ripple / tear / none（波紋 / 紙を破く / なし（静止で勝つ））
- 章番号の例: 一番茶 / 朝五時
- KV の被写体例: `a tea picker in a straw hat among green tea rows in morning mist`
- 向く用途: お茶・食 / 産地・農園 / 和の教室

## No.47 hinoki — 檜と湯（和・癒やし）
```css
:root{--bg:#f6efe4;--bg2:#eee3d2;--card:#fff;--ink:#3a2c20;--body:#5e4b3b;--muted:#9a8672;--line:#dccbb5;--accent:#b07a3c;--accent-2:#e8e2d6}
```
- 書体: Zen Old Mincho（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 木目 + 湯気
- 画像接頭辞: `hinoki wood bath with rising steam and soft window light, Japanese onsen, calm`
- 必須装備: 木目 / 湯気のグラデ / 縦書きの小見出し
- 禁止: ネオン / ビビッド
- 使える演出: ripple / none / tear（波紋 / なし（静止で勝つ） / 紙を破く）
- 章番号の例: 一 / 湯
- KV の被写体例: `a wooden hinoki bath with steam and a view of trees through a window`
- 向く用途: 温泉・宿 / 癒やし系 / 木の商材


# ビジネス・テック

## No.48 trust-navy — 信頼の紺（ビジネス・信頼）
```css
:root{--bg:#fff;--bg2:#f4f6fa;--card:#fff;--ink:#0f2140;--body:#33415c;--muted:#7d8aa3;--line:#d7dde8;--accent:#0f2140;--accent-2:#f2b705}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし
- 画像接頭辞: `corporate photography, navy blue and white, clean office with daylight, confident and calm`
- 必須装備: 紺1色 / 太い見出し / 数字のタイル
- 禁止: グレイン / 装飾
- 使える演出: none / letters-fall（なし（静止で勝つ） / 文字落下）
- 章番号の例: 01 / 02 / 03
- KV の被写体例: `a confident consultant in a navy suit standing in a bright office`
- 向く用途: 士業・コンサル / BtoB / 採用

## No.49 fintech-emerald — エメラルドの金融（ビジネス・堅実）
```css
:root{--bg:#0b1f1a;--bg2:#0f2923;--card:#14332c;--ink:#eaf5f0;--body:#b5cfc4;--muted:#6f9184;--line:rgba(234,245,240,.12);--accent:#2ecc8f;--accent-2:#d4af37}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: なし
- 画像接頭辞: `premium financial product photography, deep emerald green and gold accents, dark, sharp`
- 必須装備: 深緑1色 / 金の細線 / 等幅の数字
- 禁止: パステル / 丸角
- 使える演出: spotlight / none / letters-fall（スポットライト / なし（静止で勝つ） / 文字落下）
- 章番号の例: Q1 / Q2
- KV の被写体例: `a black credit card with a gold edge resting on emerald green stone`
- 向く用途: 金融・投資 / 高単価コンサル

## No.50 blueprint — 青図面（テック・設計）
```css
:root{--bg:#0b3d91;--bg2:#0a3480;--card:#0d47a1;--ink:#eaf2ff;--body:#bcd0f5;--muted:#7fa0d9;--line:rgba(234,242,255,.18);--accent:#fff;--accent-2:#fff}
```
- 書体: Space Mono（英字・数字）/ BIZ UDPGothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 方眼 + 白線
- 画像接頭辞: `architectural blueprint, white technical lines on deep blue paper, grid, measurements`
- 必須装備: 白線の方眼 / 寸法線 / 等幅フォント
- 禁止: セリフ / 丸角
- 使える演出: none / letters-fall / glitch-title（なし（静止で勝つ） / 文字落下 / グリッチ）
- 章番号の例: Fig. 1 / Rev. A
- KV の被写体例: `an architect's hands drafting on blueprint paper with a steel ruler`
- 向く用途: 建築・製造 / 設計・エンジニア / 講座

## No.51 data-dashboard — ダッシュボード（テック・数値）
```css
:root{--bg:#0d1117;--bg2:#111827;--card:#161e2e;--ink:#e6edf3;--body:#aab4c2;--muted:#6b7785;--line:rgba(230,237,243,.12);--accent:#3fb6ff;--accent-2:#ff7a45}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: なし（カードとグラフ）
- 画像接頭辞: `dark analytics dashboard on a monitor, glowing cyan charts and numbers, clean UI photography`
- 必須装備: 数字のタイル / 折れ線のスパークライン / シアン1色
- 禁止: セリフ / 紙の質感
- 使える演出: none / spotlight（なし（静止で勝つ） / スポットライト）
- 章番号の例: KPI 01
- KV の被写体例: `a large monitor showing glowing cyan charts in a dark office`
- 向く用途: SaaS / データ・AI / BtoB

## No.52 clinic-clean — クリニックの白（医療・安心）
```css
:root{--bg:#fff;--bg2:#f3f8fb;--card:#fff;--ink:#1d2b36;--body:#3d4f5e;--muted:#84939f;--line:#dbe6ee;--accent:#2a9d8f;--accent-2:#2a9d8f}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし
- 画像接頭辞: `clean medical clinic interior, white and pale teal, soft daylight, calm and hygienic`
- 必須装備: 白と水色 / 丸みのある見出し / 安心の余白
- 禁止: 黒 / ネオン
- 使える演出: none / ripple（なし（静止で勝つ） / 波紋）
- 章番号の例: Step 1 / 2 / 3
- KV の被写体例: `a smiling doctor in a white coat in a bright clinic hallway`
- 向く用途: 医療・歯科 / 整体 / 健康商材

## No.53 startup-blue — スタートアップ（ビジネス・勢い）
```css
:root{--bg:#fff;--bg2:#f3f6ff;--card:#fff;--ink:#0b1220;--body:#334155;--muted:#7b8798;--line:#dbe3f0;--accent:#2563eb;--accent-2:#0b1220}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし（面と太字）
- 画像接頭辞: `modern coworking office with large windows, bright daylight, clean, people blurred in motion`
- 必須装備: 電気的な青1色 / 極太の見出し / 数字のタイル
- 禁止: グレイン / セリフ
- 使える演出: letters-fall / none / spotlight（文字落下 / なし（静止で勝つ） / スポットライト）
- 章番号の例: 01 / 02 / 03
- KV の被写体例: `a young team at a bright office table with laptops, daylight`
- 向く用途: SaaS・スタートアップ / 採用 / サービスLP

## No.54 consult-charcoal — 炭のコンサル（ビジネス・重厚）
```css
:root{--bg:#1f2937;--bg2:#111827;--card:#273244;--ink:#f3f4f6;--body:#c7cdd6;--muted:#8b93a1;--line:rgba(243,244,246,.12);--accent:#f59e0b;--accent-2:#f3f4f6}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし（面と細線）
- 画像接頭辞: `consultant's desk with a leather notebook and a fountain pen, dark charcoal tones, warm lamp`
- 必須装備: 炭色の面 / 琥珀色1点 / セリフの見出し
- 禁止: パステル / 丸角
- 使える演出: spotlight / none / letters-fall（スポットライト / なし（静止で勝つ） / 文字落下）
- 章番号の例: Case 01
- KV の被写体例: `a consultant in a dark grey suit reviewing papers under a warm lamp`
- 向く用途: コンサル・士業 / BtoB / 高単価

## No.55 eco-green — サステナ（ビジネス・環境）
```css
:root{--bg:#fff;--bg2:#f2f7f0;--card:#fff;--ink:#1c2e22;--body:#3e5245;--muted:#889a8e;--line:#d6e2d8;--accent:#3a9a5b;--accent-2:#c9a97a}
```
- 書体: Fraunces（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: クラフト + 葉
- 画像接頭辞: `a small plant growing from soil in a white pot, bright clean background, fresh green`
- 必須装備: 葉の緑1色 / クラフト色の小物 / 丸みのある見出し
- 禁止: ネオン / 黒背景
- 使える演出: ripple / none / stamp（波紋 / なし（静止で勝つ） / スタンプ）
- 章番号の例: Step 01
- KV の被写体例: `hands holding a small plant seedling in soil, bright daylight`
- 向く用途: 環境・食 / 社会貢献 / 自然派ブランド


# ジャンル（ホラー・SF・ゲーム）

## No.56 horror-west — 洋画ホラー（怖い・映画っぽく）
```css
:root{--bg:#050708;--bg2:#0b1014;--card:#141b21;--ink:#e8e2d3;--body:#a9a394;--muted:#6f6a5f;--line:rgba(232,226,211,.12);--accent:#ff4a1f;--accent-2:#4f9a95}
```
- 書体: Bebas Neue（英字・数字）/ Special Elite（見出し）/ Cormorant Garamond（本文・キャプション）
- 質感: 雨 + グレイン
- 画像接頭辞: `cinematic film still, 35mm anamorphic, photorealistic, muted teal and bone-white palette, heavy fog outside the window, practical lighting, film grain, unsettling`
- 必須装備: 警告帯 / タイプライター文字 / 雨
- 禁止: パステル / 丸ゴシック
- 使える演出: flare / lightning / glitch-title（信号弾 / 雷撃 / グリッチ）
- 章番号の例: ACT I / NIGHT 4 / CLASS I
- KV の被写体例: `an abandoned coastal lighthouse at night in heavy fog, a single window lit`
- 向く用途: 作品公式サイト / イベント / ハロウィン

## No.57 pixel-8bit — ドット絵（ゲーム・レトロ）
```css
:root{--bg:#0f0f1a;--bg2:#161626;--card:#1e1e33;--ink:#f4f4f4;--body:#c9c9d9;--muted:#8a8aa3;--line:rgba(244,244,244,.12);--accent:#ff5555;--accent-2:#ffd23f}
```
- 書体: Press Start 2P（英字・数字）/ DotGothic16（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: ドット
- 画像接頭辞: `8-bit pixel art scene, retro video game style, limited palette, crisp pixels`
- 必須装備: ドットフォント / ドット絵アイコン / ライフゲージ
- 禁止: セリフ / 写実
- 使える演出: glitch-title / stamp / card-flip（グリッチ / スタンプ / カード裏返し）
- 章番号の例: STAGE 1 / 1UP
- KV の被写体例: `a pixel art hero standing on a cliff facing a distant castle`
- 向く用途: ゲーム / ガジェット / 楽しい商材

## No.58 horror-jp — Jホラー（怖い・和・湿った）
```css
:root{--bg:#0a0c0b;--bg2:#10130f;--card:#171b16;--ink:#d9dcd3;--body:#a2a79c;--muted:#6a6f66;--line:rgba(217,220,211,.12);--accent:#b1161b;--accent-2:#7f8c7a}
```
- 書体: Yuji Syuku（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Serif JP（本文・キャプション）
- 質感: ビデオノイズ + 湿った緑がかった白
- 画像接頭辞: `Japanese horror film still, desaturated greenish grey, damp abandoned school corridor, fluorescent flicker, VHS grain, unsettling stillness`
- 必須装備: 縦書きの筆文字 / 色あせた緑白 / 赤1点（血ではなく朱）
- 禁止: パステル / 丸ゴシック / ネオン
- 使える演出: glitch-title / flare / letters-fall（グリッチ / 信号弾 / 文字落下）
- 章番号の例: 一日目 / 午前二時
- KV の被写体例: `a dark abandoned school corridor with one flickering light and a small figure far at the end`
- 向く用途: ホラー作品 / 怪談イベント / 夏の企画

## No.59 horror-gothic — ゴシックホラー（怖い・耽美）
```css
:root{--bg:#0b070d;--bg2:#130b16;--card:#1b1020;--ink:#ece3e6;--body:#b8a9b3;--muted:#7d6f79;--line:rgba(236,227,230,.12);--accent:#8e0f24;--accent-2:#c9a24a}
```
- 書体: Cinzel（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Serif JP（本文・キャプション）
- 質感: 蝋燭の揺れ + ビネット
- 画像接頭辞: `gothic horror painting, candlelit cathedral interior, deep purple black shadows, crimson velvet, tarnished gold, oil painting texture, dramatic chiaroscuro`
- 必須装備: 蝋燭色のビネット / 細いセリフの大見出し / 装飾罫線は1本だけ
- 禁止: 丸角 / ポップな色
- 使える演出: spotlight / letters-fall / tear（スポットライト / 文字落下 / 紙を破く）
- 章番号の例: Ⅰ / Ⅱ / Ⅲ、第一夜
- KV の被写体例: `a candlelit gothic cathedral with a lone figure in a black dress`
- 向く用途: 小説・ゲーム作品 / ゴス系ブランド / イベント

## No.60 horror-vhs — 見つかった映像（怖い・記録映像）
```css
:root{--bg:#050605;--bg2:#0b0d0a;--card:#121510;--ink:#d5dccf;--body:#9aa392;--muted:#606860;--line:rgba(213,220,207,.12);--accent:#ff2d2d;--accent-2:#7dff8a}
```
- 書体: VT323（英字・数字）/ DotGothic16（見出し）/ BIZ UDPGothic（本文・キャプション）
- 質感: 走査線 + トラッキングノイズ + REC
- 画像接頭辞: `found footage night vision still, green tinted camcorder view, heavy VHS noise and tracking lines, dark forest, flashlight beam, blurry motion`
- 必須装備: REC と日時の焼き込み / トラッキングノイズ / ナイトビジョンの緑
- 禁止: セリフ / 上品な余白
- 使える演出: glitch-title / flare / none（グリッチ / 信号弾 / なし（静止で勝つ））
- 章番号の例: TAPE 01 / 23:58:04
- KV の被写体例: `night vision view of a dark forest path with a flashlight beam`
- 向く用途: ホラー作品 / ARG・謎解き / 配信企画

## No.61 sf-space — 宇宙SF（SF・壮大）
```css
:root{--bg:#04060e;--bg2:#080c1a;--card:#0e1426;--ink:#e8eeff;--body:#aeb9d8;--muted:#6c7799;--line:rgba(232,238,255,.12);--accent:#6ea8ff;--accent-2:#ffb547}
```
- 書体: Exo 2（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: 星の粒 + 薄い HUD グリッド
- 画像接頭辞: `cinematic space photograph, vast starfield, distant planet with thin ring, cold blue light, one warm orange engine glow, wide anamorphic, awe`
- 必須装備: 星の粒 / 細い HUD 線 / 距離・座標の表記
- 禁止: 紙の質感 / 暖色の金
- 使える演出: spotlight / letters-fall / glitch-title（スポットライト / 文字落下 / グリッチ）
- 章番号の例: SOL 01 / 0.42 AU
- KV の被写体例: `an astronaut floating in front of a vast ringed planet`
- 向く用途: SF作品 / 宇宙・科学 / 壮大な講座

## No.62 sf-lab — 白いSF（SF・クリーン・冷たい）
```css
:root{--bg:#f4f7fa;--bg2:#e9eef4;--card:#fff;--ink:#0e1a2b;--body:#34455c;--muted:#8593a8;--line:#d3dce6;--accent:#e8262a;--accent-2:#3b7dd8}
```
- 書体: Michroma（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし（白い面と細線）
- 画像接頭辞: `clean white science fiction interior, curved white corridor, soft even lighting, one red indicator light, minimal, wide`
- 必須装備: 白い面と細線 / 赤のインジケーター1つ / 等間隔の英数字ラベル
- 禁止: グレイン / 装飾
- 使える演出: none / letters-fall / spotlight（なし（静止で勝つ） / 文字落下 / スポットライト）
- 章番号の例: UNIT 01 / SEC.04
- KV の被写体例: `a curved white corridor with a single red indicator light`
- 向く用途: テック製品 / 研究・医療AI / ミニマルなSF

## No.63 sf-mecha — メカ・格納庫（SF・重厚・警告）
```css
:root{--bg:#0d0e10;--bg2:#141517;--card:#1b1c1f;--ink:#eceae4;--body:#b3b0a8;--muted:#75726b;--line:rgba(236,234,228,.12);--accent:#ff7a00;--accent-2:#ffd400}
```
- 書体: Teko（英字・数字）/ M PLUS 1p（見出し）/ BIZ UDPGothic（本文・キャプション）
- 質感: 黄黒ストライプ + 金属パネル
- 画像接頭辞: `cinematic hangar interior with a giant mech silhouette, orange warning lights, yellow-black hazard stripes, steel panels, steam, dramatic scale`
- 必須装備: 黄黒ストライプ / 警告オレンジ / 型番のラベル（TYPE-01）
- 禁止: パステル / セリフ
- 使える演出: lightning / glitch-title / letters-fall（雷撃 / グリッチ / 文字落下）
- 章番号の例: TYPE-01 / UNIT 02
- KV の被写体例: `a giant mech being repaired in a hangar, tiny engineers below`
- 向く用途: ゲーム・ロボ作品 / ガジェット / 製造

## No.64 game-rpg — ファンタジーRPG（ゲーム・冒険）
```css
:root{--bg:#0f1410;--bg2:#161d17;--card:#1e271f;--ink:#efe6cf;--body:#c2b89f;--muted:#857d6a;--line:rgba(239,230,207,.14);--accent:#d6a640;--accent-2:#4f8fd6}
```
- 書体: Cinzel（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 羊皮紙の縁 + 魔法の粒
- 画像接頭辞: `fantasy RPG concept art, ancient castle on a cliff at dusk, glowing blue magic particles, gold-lit windows, painterly, epic`
- 必須装備: 羊皮紙色の見出し / 金の細い縁1本 / クエスト風の番号
- 禁止: ネオン / 丸ゴシック
- 使える演出: lightning / card-flip / letters-fall（雷撃 / カード裏返し / 文字落下）
- 章番号の例: QUEST 01 / LV.5
- KV の被写体例: `a young adventurer with a sword looking at a distant castle at dusk`
- 向く用途: ゲーム作品 / コミュニティ / 冒険系の講座

## No.65 game-fps — バトル・FPS（ゲーム・緊張）
```css
:root{--bg:#0a0b0a;--bg2:#111311;--card:#181b18;--ink:#e8e6df;--body:#aeaca3;--muted:#6f6e66;--line:rgba(232,230,223,.12);--accent:#ff6a00;--accent-2:#7fa650}
```
- 書体: Black Ops One（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: HUD + 走査線
- 画像接頭辞: `tactical shooter key art, soldier silhouette in smoke, orange flare, olive green and black, dust particles, gritty, cinematic`
- 必須装備: HUD 風の角括弧 / オレンジ1色 / カウントダウン
- 禁止: パステル / セリフ / 丸角
- 使える演出: lightning / glitch-title / flare（雷撃 / グリッチ / 信号弾）
- 章番号の例: MISSION 01 / 03:00
- KV の被写体例: `a soldier silhouette walking through smoke with an orange flare behind`
- 向く用途: ゲーム・配信 / 大会 / 熱い商材

## No.66 game-esports — eスポーツ（ゲーム・競技・派手）
```css
:root{--bg:#08070f;--bg2:#0e0c19;--card:#151226;--ink:#f1efff;--body:#b9b4d8;--muted:#736e94;--line:rgba(241,239,255,.12);--accent:#8b5cf6;--accent-2:#22d3ee}
```
- 書体: Rajdhani（英字・数字）/ M PLUS 1p（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 斜めカット + 光の筋
- 画像接頭辞: `esports arena stage with purple and cyan stage lights, dramatic haze, diagonal light beams, crowd silhouettes, high energy`
- 必須装備: 斜めカットの帯 / 紫×シアン / チーム名のような大文字英字
- 禁止: 紙の質感 / セリフ
- 使える演出: neon-power / glitch-title / lightning（ネオン点灯 / グリッチ / 雷撃）
- 章番号の例: ROUND 01 / VS
- KV の被写体例: `a player at a glowing gaming desk on stage with purple and cyan lights`
- 向く用途: 大会・チーム / 配信者 / ガジェット

## No.67 anime-kinetic — アニメ・ポスター（エンタメ・熱量・斜め）
```css
:root{--bg:#fff;--bg2:#f3f3f3;--card:#fff;--ink:#111;--body:#222;--muted:#777;--line:#111;--accent:#e60012;--accent-2:#111}
```
- 書体: Zen Kaku Gothic New（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 斜めの赤帯 + 集中線
- 画像接頭辞: `anime movie poster style illustration, dramatic low angle of a character against a bright sky, bold red diagonal band, speed lines, high contrast`
- 必須装備: 極太の斜め帯 / 赤1色 / キャッチコピーを縦と横で交差
- 禁止: パステル / 丸角
- 使える演出: letters-fall / stamp / lightning（文字落下 / スタンプ / 雷撃）
- 章番号の例: 第1話 / 予告
- KV の被写体例: `a determined young character in a school uniform against a bright blue sky, low angle`
- 向く用途: アニメ・漫画作品 / イベント / 熱い告知

## No.68 post-apoc — 荒廃した世界（SF・荒野・錆）
```css
:root{--bg:#14110d;--bg2:#1b1712;--card:#231e18;--ink:#e6dcc8;--body:#b5a88e;--muted:#7a7060;--line:rgba(230,220,200,.12);--accent:#d3552b;--accent-2:#8a9a5b}
```
- 書体: Special Elite（英字・数字）/ BIZ UDPGothic（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 砂嵐 + 錆の擦れ
- 画像接頭辞: `post-apocalyptic wasteland, rusted vehicle in sand, dust storm, muted sand and rust palette, lone figure with a backpack, cinematic wide`
- 必須装備: 錆色1つ / タイプライター文字 / 擦れたスタンプ
- 禁止: パステル / グロー
- 使える演出: stamp / tear / glitch-title（スタンプ / 紙を破く / グリッチ）
- 章番号の例: DAY 214 / SECTOR 7
- KV の被写体例: `a lone figure with a backpack walking toward a rusted city in a dust storm`
- 向く用途: サバイバル系作品 / ゲーム / 硬派な商材

## No.69 steampunk — スチームパンク（SF・真鍮・歯車）
```css
:root{--bg:#1a120c;--bg2:#241912;--card:#2e2118;--ink:#f1e4cf;--body:#c4b39a;--muted:#87765f;--line:rgba(241,228,207,.12);--accent:#c8873a;--accent-2:#7aa3a8}
```
- 書体: Libre Baskerville（英字・数字）/ Shippori Mincho B1（見出し）/ Special Elite（本文・キャプション）
- 質感: 真鍮 + 歯車 + 蒸気
- 画像接頭辞: `steampunk brass airship above a Victorian city, gears and steam, copper and dark brown, painterly`
- 必須装備: 歯車のモチーフ / 真鍮色1つ / タイプライター文字
- 禁止: パステル / 丸ゴシック
- 使える演出: card-flip / stamp / letters-fall（カード裏返し / スタンプ / 文字落下）
- 章番号の例: Vol. Ⅰ / 蒸気圧
- KV の被写体例: `a brass airship over a Victorian city with gears and steam`
- 向く用途: ゲーム・小説作品 / クラフト / 異世界系

## No.70 kaiju — 特撮（ジャンル・巨大・熱い）
```css
:root{--bg:#0a0a0a;--bg2:#141414;--card:#1c1c1c;--ink:#f2efe6;--body:#c2bfb4;--muted:#807d74;--line:rgba(242,239,230,.12);--accent:#e5261d;--accent-2:#f2c13d}
```
- 書体: Bebas Neue（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: フィルムの粒子 + 赤い空
- 画像接頭辞: `giant monster silhouette rising behind a city at dusk, red sky, film grain, tokusatsu movie still`
- 必須装備: 赤い空 / 極太の見出し / 警報の帯
- 禁止: パステル / 丸角
- 使える演出: lightning / letters-fall / flare（雷撃 / 文字落下 / 信号弾）
- 章番号の例: 第1報 / 出現
- KV の被写体例: `a giant monster silhouette rising behind a city skyline at dusk, red sky`
- 向く用途: 特撮・映画作品 / イベント / 熱い告知


# ミニマル

## No.71 obsidian-mint — 黒曜石とミント（かっこいい・クリーン）
```css
:root{--bg:#0c0f0e;--bg2:#111615;--card:#171d1b;--ink:#f2fbf7;--body:#b5c9c0;--muted:#728a80;--line:rgba(242,251,247,.12);--accent:#5ee3b0;--accent-2:#5ee3b0}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: なし（面と線だけ）
- 画像接頭辞: `product photography on black glass, single mint green light edge, minimal, sharp shadows, high contrast`
- 必須装備: 1色のミント / 極太見出し / 細い等幅キャプション
- 禁止: グラデ / 装飾罫線
- 使える演出: spotlight / none / letters-fall（スポットライト / なし（静止で勝つ） / 文字落下）
- 章番号の例: 01 — 02
- KV の被写体例: `a sleek smartphone floating above black glass with a single mint light edge`
- 向く用途: SaaS・ツール / アプリ / 簡易HP

## No.72 mono-minimal — 白黒ミニマル（ミニマル・上品）
```css
:root{--bg:#fff;--bg2:#fafafa;--card:#fff;--ink:#000;--body:#222;--muted:#888;--line:#e5e5e5;--accent:#000;--accent-2:#000}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし
- 画像接頭辞: `monochrome photography, hard shadow, minimal composition, high key, black and white`
- 必須装備: 1px罫線 / 極端なサイズ差 / 演出は最小
- 禁止: 差し色2色以上 / グロー / カーソル
- 使える演出: none / letters-fall（なし（静止で勝つ） / 文字落下）
- 章番号の例: 01 — 02
- KV の被写体例: `a single black ceramic vase on a white table, hard shadow`
- 向く用途: ポートフォリオ / 建築・デザイン

## No.73 gallery-white — 美術館の白（ミニマル・アート）
```css
:root{--bg:#fff;--bg2:#f5f5f5;--card:#fff;--ink:#111;--body:#333;--muted:#999;--line:#e8e8e8;--accent:#111;--accent-2:#111}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし
- 画像接頭辞: `art gallery white wall with a single framed photograph, museum lighting, minimal, wide`
- 必須装備: 作品を1点だけ大きく / キャプションは11px / 壁のような余白
- 禁止: 装飾 / グラデ
- 使える演出: none / spotlight（なし（静止で勝つ） / スポットライト）
- 章番号の例: No. 1 — 2026
- KV の被写体例: `a person standing alone in a white gallery looking at one large framed photograph`
- 向く用途: ポートフォリオ / 作家・写真家 / 展示

## No.74 morning-fog — 霧の朝（静か・淡い）
```css
:root{--bg:#f2f3f4;--bg2:#e9ebee;--card:#fff;--ink:#2a2f36;--body:#555c66;--muted:#8f97a3;--line:#dde1e6;--accent:#6b7f99;--accent-2:#6b7f99}
```
- 書体: Cormorant Garamond（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 霧のグラデ
- 画像接頭辞: `foggy morning landscape through the window, pale grey and soft blue tones, soft light, minimal`
- 必須装備: 淡い青灰1色 / ぼかしの背景 / 薄い文字
- 禁止: ビビッド / 太ゴシック
- 使える演出: ripple / none / tear（波紋 / なし（静止で勝つ） / 紙を破く）
- 章番号の例: 05:40 / 06:10
- KV の被写体例: `a person walking alone on a foggy pale grey morning road`
- 向く用途: カウンセラー / 朝活 / 読み物

## No.75 swiss-grid — スイス・グリッド（かっこいい・国際様式）
```css
:root{--bg:#fff;--bg2:#f2f2f2;--card:#fff;--ink:#000;--body:#222;--muted:#777;--line:#000;--accent:#e30613;--accent-2:#e30613}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし（グリッド線）
- 画像接頭辞: `swiss international style poster, bold red black white, strict grid, helvetica-like typography, flat`
- 必須装備: 赤1色 / 太い罫線のグリッド / 左寄せ・左揃え
- 禁止: 中央揃え / 装飾
- 使える演出: letters-fall / none（文字落下 / なし（静止で勝つ））
- 章番号の例: 01 / 02 / 03
- KV の被写体例: `a bold red and black geometric poster pinned on a white wall`
- 向く用途: デザイン・制作 / 講座 / イベント

## No.76 minimal-black — 黒ミニマル（ミニマル・黒）
```css
:root{--bg:#000;--bg2:#0a0a0a;--card:#0a0a0a;--ink:#fff;--body:#bdbdbd;--muted:#777;--line:rgba(255,255,255,.14);--accent:#fff;--accent-2:#fff}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし
- 画像接頭辞: `minimal product photography on pure black, a single object, soft light, lots of empty space`
- 必須装備: 白黒のみ / 1px罫線 / 極端なサイズ差
- 禁止: 差し色 / グロー / 装飾
- 使える演出: none / letters-fall（なし（静止で勝つ） / 文字落下）
- 章番号の例: 01
- KV の被写体例: `a single white chair in a black room lit by one soft light`
- 向く用途: ポートフォリオ / ブランド / 高単価

## No.77 minimal-warm — 生成りミニマル（ミニマル・温かい）
```css
:root{--bg:#f4efe7;--bg2:#ece5da;--card:#fff;--ink:#2a2622;--body:#57504a;--muted:#948b81;--line:#dcd3c6;--accent:#2a2622;--accent-2:#b6543a}
```
- 書体: Fraunces（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 紙
- 画像接頭辞: `warm minimal still life on beige linen, one ceramic object, soft natural light, empty space`
- 必須装備: 生成りの面 / 物は1つ / 小さなセリフ英字
- 禁止: ビビッド / 黒背景
- 使える演出: none / tear / ripple（なし（静止で勝つ） / 紙を破く / 波紋）
- 章番号の例: No. 1
- KV の被写体例: `a ceramic cup on a beige table by a window, soft light`
- 向く用途: 暮らし・工芸 / サロン / 自己紹介

## No.78 minimal-type — 文字だけ（ミニマル・タイポ）
```css
:root{--bg:#fff;--bg2:#f7f7f7;--card:#fff;--ink:#000;--body:#222;--muted:#888;--line:#000;--accent:#000;--accent-2:#ff3b30}
```
- 書体: Inter Tight（英字・数字）/ Zen Kaku Gothic New（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: なし（文字が画像）
- 画像接頭辞: `giant black typography poster on white, a single word, extreme scale, flat`
- 必須装備: 見出し20vw / 画像なし前提 / 赤1点
- 禁止: 写真 / グラデ
- 使える演出: letters-fall / none（文字落下 / なし（静止で勝つ））
- 章番号の例: 01 / 02
- KV の被写体例: `a huge black letter printed on white paper, close up`
- 向く用途: 文字主役の告知 / デザイン / 講座

## No.79 notebook-grid — 方眼ノート（ミニマル・道具）
```css
:root{--bg:#fff;--bg2:#fafafa;--card:#fff;--ink:#1a1a1a;--body:#3a3a3a;--muted:#8a8a8a;--line:#dfe3e8;--accent:#1a1a1a;--accent-2:#2b5cd6}
```
- 書体: Inter（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: 方眼の薄い線
- 画像接頭辞: `a blank grid notebook with a blue pen, top view, white desk, soft light`
- 必須装備: 方眼の線 / 青ペン1色 / 手書き風のメモ
- 禁止: グロー / 黒背景
- 使える演出: none / letters-fall / stamp（なし（静止で勝つ） / 文字落下 / スタンプ）
- 章番号の例: p.1 / □
- KV の被写体例: `a student writing in a grid notebook with a blue pen, top view`
- 向く用途: ノート術・学習 / 講座 / 文具

## No.80 pale-air — 淡い空（ミニマル・軽い）
```css
:root{--bg:#fbfdff;--bg2:#f0f6fc;--card:#fff;--ink:#1c2733;--body:#4a5764;--muted:#8f9aa6;--line:#dbe6f0;--accent:#1c2733;--accent-2:#7fb3e6}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Inter（本文・キャプション）
- 質感: なし（淡い青のグラデ）
- 画像接頭辞: `a single white balloon against a pale blue sky, minimal, airy, soft light`
- 必須装備: 淡い青のグラデ / 細い見出し / 大余白
- 禁止: 黒 / ビビッド
- 使える演出: ripple / none（波紋 / なし（静止で勝つ））
- 章番号の例: 01
- KV の被写体例: `a child holding a white balloon under a pale blue sky`
- 向く用途: 軽やかなサービス / 子育て / 空気感の商材


# かっこいい・クール

## No.81 paper-black — 黒紙の写真集（かっこいい・静か）
```css
:root{--bg:#121110;--bg2:#1a1917;--card:#1f1d1a;--ink:#f1ede4;--body:#b9b3a6;--muted:#7d786e;--line:rgba(241,237,228,.14);--accent:#e9d8a6;--accent-2:#e9d8a6}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 紙の繊維 + 朝の光の帯
- 画像接頭辞: `editorial film photograph, night, single warm lamp light, deep black shadows, muted tones, Kodak Portra grain, quiet composition, lots of negative space`
- 必須装備: マスクからの文字浮上 / ページ番号 / 紙の繊維
- 禁止: カラフルな差し色 / 太ゴシック / 厚み影ボタン
- 使える演出: tear / spotlight / letters-fall（紙を破く / スポットライト / 文字落下）
- 章番号の例: p. 02 / Vol. 01 / Fig. 1
- KV の被写体例: `a woman photographer seen from behind holding a film camera by a window at dawn, quiet room`
- 向く用途: 自己紹介 / ポートフォリオ / 写真家・作家

## No.82 neon-tokyo — ネオン（かっこいい・テック）
```css
:root{--bg:#070a14;--bg2:#0b1020;--card:#111833;--ink:#eef2ff;--body:#b7c0e0;--muted:#6f7aa3;--line:rgba(238,242,255,.12);--accent:#22d3ee;--accent-2:#f0abfc}
```
- 書体: Orbitron（英字・数字）/ M PLUS 1p（見出し）/ DotGothic16（本文・キャプション）
- 質感: 走査線
- 画像接頭辞: `rainy neon city night through the window, cyan and magenta reflections, anamorphic lens flare, cyberpunk photography`
- 必須装備: 走査線 / ネオン管の点滅 / HUD風の角括弧
- 禁止: 明朝 / 暖色の金
- 使える演出: neon-power / glitch-title / spotlight（ネオン点灯 / グリッチ / スポットライト）
- 章番号の例: 01 // 02、SYS.01
- KV の被写体例: `a person in a hooded jacket walking through a rainy neon alley, umbrella reflecting cyan and magenta`
- 向く用途: ゲーム・配信者 / ガジェット / コミュニティ

## No.83 charcoal-brass — 炭と真鍮（かっこいい・職人）
```css
:root{--bg:#1a1a1a;--bg2:#222;--card:#2a2a2a;--ink:#efe9df;--body:#bdb5a8;--muted:#857c70;--line:rgba(239,233,223,.12);--accent:#b8862b;--accent-2:#b8862b}
```
- 書体: Oswald（英字・数字）/ Noto Sans JP（見出し）/ Zen Old Mincho（本文・キャプション）
- 質感: 金属のヘアライン
- 画像接頭辞: `workshop still life, dark charcoal tones with brass and warm tungsten light, macro texture of wood and metal, film grain`
- 必須装備: ヘアライン罫線 / 真鍮色の数字 / 工具のような角ばったUI
- 禁止: 丸角 / パステル
- 使える演出: stamp / letters-fall / spotlight（スタンプ / 文字落下 / スポットライト）
- 章番号の例: No. 01 / LOT 2026
- KV の被写体例: `a craftsman's hands shaping leather on a dark workbench with brass tools`
- 向く用途: 職人・工房 / 革・木・コーヒー / 簡易HP

## No.84 noir-film — 白黒映画（かっこいい・クラシック）
```css
:root{--bg:#0a0a0a;--bg2:#141414;--card:#1c1c1c;--ink:#f4f4f4;--body:#c8c8c8;--muted:#8a8a8a;--line:rgba(244,244,244,.14);--accent:#f4f4f4;--accent-2:#f4f4f4}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Special Elite（本文・キャプション）
- 質感: フィルムの傷 + グレイン
- 画像接頭辞: `black and white film noir still, hard venetian blind shadows, cigarette smoke, 1950s, grain`
- 必須装備: 白黒のみ / 字幕風キャプション / フィルムの傷
- 禁止: 色 / 丸角
- 使える演出: spotlight / tear / glitch-title（スポットライト / 紙を破く / グリッチ）
- 章番号の例: REEL 1 / SCENE 4
- KV の被写体例: `a woman in a 1950s trench coat under a streetlight, venetian blind shadows`
- 向く用途: 作家・俳優 / イベント / 作品

## No.85 cyber-grid — 端末の緑（テック・ハッカー）
```css
:root{--bg:#050805;--bg2:#0a100a;--card:#0f160f;--ink:#d7ffd7;--body:#9fd39f;--muted:#5f8f5f;--line:rgba(215,255,215,.12);--accent:#39ff6a;--accent-2:#39ff6a}
```
- 書体: Space Mono（英字・数字）/ BIZ UDPGothic（見出し）/ VT323（本文・キャプション）
- 質感: 走査線 + カーソル点滅
- 画像接頭辞: `close-up of a green phosphor terminal screen reflecting on a desk, dark room, scanlines, retro computing`
- 必須装備: 等幅フォント / カーソル点滅 / > プロンプト表記
- 禁止: セリフ / 丸角 / 写真の多用
- 使える演出: glitch-title / neon-power / none（グリッチ / ネオン点灯 / なし（静止で勝つ））
- 章番号の例: $ step 01
- KV の被写体例: `hands on a mechanical keyboard in a dark room lit only by a green terminal screen`
- 向く用途: AI・プログラミング講座 / ツール / コミュニティ

## No.86 concrete — コンクリート（クール・硬派）
```css
:root{--bg:#2b2d2f;--bg2:#333638;--card:#3b3e41;--ink:#f1f1f0;--body:#c3c5c6;--muted:#8a8d90;--line:rgba(241,241,240,.12);--accent:#f1f1f0;--accent-2:#ff8a00}
```
- 書体: Oswald（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: 打ちっぱなしの質感
- 画像接頭辞: `brutalist concrete architecture photograph, grey textured walls, hard shadow, minimal, overcast`
- 必須装備: 灰の面 / 硬い影 / 安全オレンジ1点
- 禁止: パステル / 丸角
- 使える演出: spotlight / letters-fall / none（スポットライト / 文字落下 / なし（静止で勝つ））
- 章番号の例: BLOCK 01
- KV の被写体例: `a person standing in a concrete stairwell with hard light`
- 向く用途: 建築・不動産 / 男性向け / 硬派な商材

## No.87 carbon-red — カーボン×赤（クール・速い）
```css
:root{--bg:#0e0f11;--bg2:#15171a;--card:#1c1f23;--ink:#f5f5f5;--body:#b9bcc2;--muted:#767a82;--line:rgba(245,245,245,.12);--accent:#e10600;--accent-2:#f5f5f5}
```
- 書体: Teko（英字・数字）/ Noto Sans JP（見出し）/ Rajdhani（本文・キャプション）
- 質感: カーボンの織り + 斜線
- 画像接頭辞: `carbon fiber texture with a single red racing stripe, studio light, sharp, automotive`
- 必須装備: 斜めの赤ライン1本 / カーボンの織り / ラップタイム風の数字
- 禁止: セリフ / 紙の質感
- 使える演出: neon-power / letters-fall / lightning（ネオン点灯 / 文字落下 / 雷撃）
- 章番号の例: LAP 01 / 0.01s
- KV の被写体例: `a sports car in a dark studio with one red light streak`
- 向く用途: 車・スポーツ / ガジェット / 速さ系

## No.88 street-mono — ストリート（クール・若い）
```css
:root{--bg:#f2f2f2;--bg2:#e8e8e8;--card:#fff;--ink:#111;--body:#333;--muted:#777;--line:#111;--accent:#111;--accent-2:#c6ff00}
```
- 書体: Archivo Black（英字・数字）/ M PLUS 1p（見出し）/ Space Mono（本文・キャプション）
- 質感: コピー機のざらつき + テープ
- 画像接頭辞: `street photography, black and white, urban wall with torn posters, one neon yellow-green element, grainy`
- 必須装備: 白黒 + 蛍光1色 / テープで貼った風 / 傾けた見出し
- 禁止: セリフ / パステル
- 使える演出: stamp / letters-fall / glitch-title（スタンプ / 文字落下 / グリッチ）
- 章番号の例: VOL.01 / DROP
- KV の被写体例: `a skater on a city street, black and white, with a neon yellow-green accent`
- 向く用途: アパレル / 音楽 / 若年層

## No.89 mode-black — モード（クール・雑誌・白黒）
```css
:root{--bg:#000;--bg2:#0a0a0a;--card:#111;--ink:#fff;--body:#c8c8c8;--muted:#808080;--line:rgba(255,255,255,.16);--accent:#fff;--accent-2:#c8c8c8}
```
- 書体: Playfair Display（英字・数字）/ Noto Serif JP（見出し）/ Inter（本文・キャプション）
- 質感: なし（写真1枚と文字）
- 画像接頭辞: `fashion editorial photograph, black and white, a model against a black backdrop, high contrast, magazine`
- 必須装備: 写真1枚を大きく / 細いセリフの巨大見出し / 白黒のみ
- 禁止: 色 / 丸角
- 使える演出: letters-fall / spotlight / none（文字落下 / スポットライト / なし（静止で勝つ））
- 章番号の例: ISSUE 01 / FW
- KV の被写体例: `a fashion model in a black coat on a black backdrop, black and white`
- 向く用途: アパレル・美容 / モデル / 雑誌的ブランド

## No.90 military — ミリタリー（クール・硬派・実用）
```css
:root{--bg:#3b4a2f;--bg2:#334128;--card:#44553a;--ink:#f0ecdc;--body:#c8c4b0;--muted:#8f8c78;--line:rgba(240,236,220,.14);--accent:#f0ecdc;--accent-2:#d9a441}
```
- 書体: Black Ops One（英字・数字）/ BIZ UDPGothic（見出し）/ Space Mono（本文・キャプション）
- 質感: ステンシル + 帆布の織り
- 画像接頭辞: `canvas military backpack on an olive green background, stencil lettering style, hard light`
- 必須装備: ステンシル風の英字 / オリーブ1色 / 帆布の質感
- 禁止: パステル / セリフ
- 使える演出: stamp / letters-fall / none（スタンプ / 文字落下 / なし（静止で勝つ））
- 章番号の例: UNIT 01 / SPEC
- KV の被写体例: `a hiker with a canvas backpack on a ridge, olive and sand tones`
- 向く用途: アウトドア・ギア / 硬派なブランド / 男性向け

## No.91 glass-blue — ガラスと青（クール・テック・透明）
```css
:root{--bg:#070b16;--bg2:#0c1224;--card:#121a30;--ink:#eaf1ff;--body:#b3c1e0;--muted:#6f7ea3;--line:rgba(234,241,255,.14);--accent:#38bdf8;--accent-2:#eaf1ff}
```
- 書体: Inter Tight（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: すりガラスの面 + 青い光
- 画像接頭辞: `frosted glass panels lit by cool blue light in a dark room, reflections, clean, futuristic`
- 必須装備: すりガラスの面（backdrop-blur） / 青い光1つ / 細い等幅ラベル
- 禁止: 紙の質感 / 暖色
- 使える演出: spotlight / neon-power / none（スポットライト / ネオン点灯 / なし（静止で勝つ））
- 章番号の例: v1.0 / 01
- KV の被写体例: `a person behind a frosted glass panel lit by blue light`
- 向く用途: アプリ・ツール / テック製品 / AI系


# 商材屋（ギラギラ）

## No.92 abyss-gold — 深海クリムゾン（ギラギラ・情報商材っぽく）
```css
:root{--bg:#000;--bg2:#070707;--card:#111;--ink:#fff;--body:#d6d6d6;--muted:#8b8b8b;--line:rgba(255,255,255,.1);--accent:#d10a1e;--accent-2:#e5c158}
```
- 書体: Bebas Neue（英字・数字）/ Noto Sans JP（見出し）/ Shippori Mincho B1（本文・キャプション）
- 質感: グレイン
- 画像接頭辞: `cinematic photorealistic film still, pure black background, crimson red and metallic gold accent lighting only, volumetric light, subtle film grain, anamorphic`
- 必須装備: 金は数字1か所か線1本 / 赤帯 / ローダー
- 禁止: パステル / 丸ゴシック / 金の象徴物 / 金を全部に塗る
- 使える演出: ink-splat / spotlight / lightning / letters-fall（墨 / スポットライト / 雷撃 / 文字落下）
- 章番号の例: ARM 01 / 深度 -8,000m
- KV の被写体例: `a lone man in a black coat standing at the edge of a rooftop at night facing a vast dark ocean, a thin line of red light on the horizon`
- 向く用途: セールスレター / オプトイン（煽り）

## No.93 brutal — ブルータリズム（ギラギラ・尖った・明るい）
```css
:root{--bg:#fff;--bg2:#f4f4f4;--card:#fff;--ink:#000;--body:#111;--muted:#666;--line:#000;--accent:#ffe600;--accent-2:#ff3b30}
```
- 書体: Archivo Black（英字・数字）/ BIZ UDPGothic（見出し）/ Space Mono（本文・キャプション）
- 質感: なし（4pxの黒罫線）
- 画像接頭辞: `flat graphic illustration, high contrast, risograph texture, two-color print, bold shapes, yellow and black`
- 必須装備: 4pxの黒罫線 / ズレたグリッド / 黄色の塗り
- 禁止: グラデ / 角丸 / 影 / 明朝
- 使える演出: stamp / letters-fall / card-flip（スタンプ / 文字落下 / カード裏返し）
- 章番号の例: №1、[01]
- KV の被写体例: `a black megaphone on a bright yellow background`
- 向く用途: 号外的セールスレター / イベント / 若年層

## No.94 gold-rush — 黒金（ギラギラ・王道）
```css
:root{--bg:#000;--bg2:#0b0a07;--card:#14120b;--ink:#fff;--body:#d9d2bd;--muted:#8f8770;--line:rgba(229,193,88,.25);--accent:#e5c158;--accent-2:#d10a1e}
```
- 書体: Bebas Neue（英字・数字）/ Noto Sans JP（見出し）/ Shippori Mincho B1（本文・キャプション）
- 質感: 金の粒 + 光の筋
- 画像接頭辞: `luxurious black and gold cinematic still, golden light rays and particles on black, dramatic`
- 必須装備: 金は見出し1つとボタンまで / 赤の帯 / 光の筋
- 禁止: パステル / 丸ゴシック / 金の象徴物
- 使える演出: spotlight / letters-fall / ink-splat（スポットライト / 文字落下 / 墨）
- 章番号の例: 第1章 / ¥
- KV の被写体例: `golden light rays and floating gold particles over a dark city skyline`
- 向く用途: セールスレター / 高額商材 / ローンチ

## No.95 red-alert — 赤ベタ（ギラギラ・セール）
```css
:root{--bg:#d10a1e;--bg2:#b8081a;--card:#a10716;--ink:#fff;--body:#ffe3e6;--muted:#f4a3ab;--line:rgba(255,255,255,.3);--accent:#ffe600;--accent-2:#111}
```
- 書体: Archivo Black（英字・数字）/ Noto Sans JP（見出し）/ BIZ UDPGothic（本文・キャプション）
- 質感: 斜めストライプ
- 画像接頭辞: `bold red poster background with a single black object, flat, high contrast, sale advertisement style`
- 必須装備: 全面の赤 / 黄色の見出し / 残り数・期限の表記
- 禁止: セリフ / グラデ
- 使える演出: stamp / letters-fall / lightning（スタンプ / 文字落下 / 雷撃）
- 章番号の例: 本日限り / 残り
- KV の被写体例: `a black megaphone and yellow burst shapes on a bright red background`
- 向く用途: セール / 期間限定 / キャンペーン

## No.96 money-green — 札束グリーン（ギラギラ・稼ぐ）
```css
:root{--bg:#061a12;--bg2:#0a2419;--card:#0f2f20;--ink:#eafff3;--body:#b5d8c4;--muted:#6f9682;--line:rgba(234,255,243,.12);--accent:#2ecc71;--accent-2:#e5c158}
```
- 書体: Bebas Neue（英字・数字）/ Noto Sans JP（見出し）/ Space Mono（本文・キャプション）
- 質感: 紙幣の細線パターン
- 画像接頭辞: `dark green cinematic still with gold coins and green light, wealth mood, dramatic spotlight`
- 必須装備: 深緑の面 / 等幅の数字 / 金は数字1か所
- 禁止: パステル / 丸ゴシック
- 使える演出: spotlight / letters-fall / neon-power（スポットライト / 文字落下 / ネオン点灯）
- 章番号の例: ¥ / 第1章
- KV の被写体例: `stacks of gold coins on a dark green table under a spotlight`
- 向く用途: 副業・投資系 / 収益化 / 高額商材

## No.97 flash-yellow — 黄×黒（ギラギラ・警告）
```css
:root{--bg:#ffe600;--bg2:#f5dc00;--card:#fff;--ink:#000;--body:#111;--muted:#6b6400;--line:#000;--accent:#000;--accent-2:#d10a1e}
```
- 書体: Bebas Neue（英字・数字）/ Zen Kaku Gothic New（見出し）/ BIZ UDPGothic（本文・キャプション）
- 質感: 黄黒の斜線 + 集中線
- 画像接頭辞: `bright yellow background with bold black shapes and a warning stripe, flat graphic, loud`
- 必須装備: 全面の黄 / 黒の極太見出し / 警告の斜線
- 禁止: セリフ / 淡色
- 使える演出: stamp / lightning / letters-fall（スタンプ / 雷撃 / 文字落下）
- 章番号の例: 激 / 01
- KV の被写体例: `a black lightning bolt shape on a bright yellow wall with hazard stripes`
- 向く用途: 激安・大量 / 号外 / イベント

## No.98 royal-purple — 紫×金（ギラギラ・高級）
```css
:root{--bg:#12061f;--bg2:#1b0b2c;--card:#24123a;--ink:#f7efff;--body:#cdb9e0;--muted:#8a72a3;--line:rgba(247,239,255,.12);--accent:#e5c158;--accent-2:#c084fc}
```
- 書体: Cinzel（英字・数字）/ Shippori Mincho B1（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: ベルベット + 金の粒
- 画像接頭辞: `royal purple velvet with gold light particles, luxurious, dramatic spotlight, cinematic`
- 必須装備: 紫の面 / 金は見出し1つ / VIP・招待の語彙
- 禁止: パステル / 丸ゴシック / 金の象徴物
- 使える演出: spotlight / letters-fall / card-flip（スポットライト / 文字落下 / カード裏返し）
- 章番号の例: Ⅰ / VIP
- KV の被写体例: `a golden key resting on purple velvet under a spotlight`
- 向く用途: 高額コンサル / 会員制 / 占い・スピリチュアル

## No.99 neon-sale — ネオンセール（ギラギラ・派手・夜）
```css
:root{--bg:#0a0510;--bg2:#120a1c;--card:#1a1026;--ink:#fff0fa;--body:#e6b8dc;--muted:#9a7a95;--line:rgba(255,240,250,.14);--accent:#ff2d95;--accent-2:#ffe600}
```
- 書体: Bangers（英字・数字）/ M PLUS 1p（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: ネオン管の光 + レンガ
- 画像接頭辞: `hot pink and yellow neon tubes glowing on a black brick wall at night, vivid, loud`
- 必須装備: ネオンの光 / ピンク×黄 / 太い英字
- 禁止: セリフ / 紙の質感
- 使える演出: neon-power / stamp / lightning（ネオン点灯 / スタンプ / 雷撃）
- 章番号の例: SALE / 24H
- KV の被写体例: `a crowd under hot pink and yellow neon lights on a night street`
- 向く用途: セール / ナイトイベント / 若年層向け商材

## No.100 platinum — プラチナ（ギラギラ・高級・銀）
```css
:root{--bg:#050506;--bg2:#0c0c0e;--card:#131316;--ink:#f7f7f9;--body:#c9c9cf;--muted:#83838b;--line:rgba(247,247,249,.14);--accent:#e6e6ee;--accent-2:#b9b9c6}
```
- 書体: Cinzel（英字・数字）/ Noto Serif JP（見出し）/ Noto Sans JP（本文・キャプション）
- 質感: 銀の光の筋 + 黒ベルベット
- 画像接頭辞: `silver light streaks and sparkles on black velvet, luxurious, cinematic, cool tones`
- 必須装備: 銀の光1つ / 黒の面 / 細いセリフの大文字
- 禁止: パステル / 丸ゴシック / 宝石の象徴物
- 使える演出: spotlight / letters-fall / card-flip（スポットライト / 文字落下 / カード裏返し）
- 章番号の例: Ⅰ / MEMBER
- KV の被写体例: `a silver key on black velvet with light streaks`
- 向く用途: 会員制 / 高額商材 / 上位プラン

---

## custom — ヒアリングで独自 World を作る

`world: custom` の時は次の6問を**1つのメッセージで**聞く。

1. 好きなサイト・ブランド・雑誌を3つ（URLでも名前でも）
2. 嫌いな見た目（例: ギラギラ、丸っこい、写真が多い）
3. 読者に持ってほしい気分を一言（例: 安心、ワクワク、緊張）
4. 色を3つ（無ければ「おまかせ」）
5. 文字の印象: やわらかい / 硬い / 手書き / 機械的
6. 参考画像があれば添付

答えから次を作り `worlds/custom-<name>.md` に保存する: トークン CSS（上と同じ変数名で）/ 書体2〜3（Google Fonts にあるもの）/ 画像接頭辞（画風・光・質感・色を英語で1行）/ 必須装備3つ / 禁止3つ / 使える演出2〜3。作った World を1段落で説明してから生成に進む。以後は通常の World として指定できる。一番近い既存 World を「ベース」として名指しすると速い（例: ベース = linen-sage、色だけ藍に）。
