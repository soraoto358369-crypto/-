# -*- coding: utf-8 -*-
"""worlds_data.py — 世界観100種の定義。build-worlds.py がここから worlds.json / worlds.md / ../Tako_LP_Lookbook/index.html / prompts.json を生成する
各要素: id, name, tag(方向性), group, colors{bg,bg2,card,ink,body,muted,line,accent,accent2}, fonts[en,jp,sub], texture,
        prefix(画像プロンプト接頭辞), must[], forbid[], sigs[], count(数え方), uses, hero{cap,h,em,btn}
"""
W = []
def w(id, name, tag, group, colors, fonts, texture, prefix, must, forbid, sigs, count, uses, cap, h, em, btn):
    W.append(dict(id=id, name=name, tag=tag, group=group, colors=colors, fonts=fonts, texture=texture, prefix=prefix,
                  must=must, forbid=forbid, sigs=sigs, count=count, uses=uses, hero=dict(cap=cap, h=h, em=em, btn=btn)))
C = lambda bg, bg2, card, ink, body, muted, line, accent, accent2="": dict(bg=bg, bg2=bg2, card=card, ink=ink, body=body, muted=muted, line=line, accent=accent, accent2=accent2 or accent)

# ============ A. ダーク・壮大（10） ============
w("abyss-gold","深海クリムゾン","ギラギラ・情報商材っぽく","gira",
  C("#000","#070707","#111","#fff","#d6d6d6","#8b8b8b","rgba(255,255,255,.1)","#d10a1e","#e5c158"),
  ["Bebas Neue","Noto Sans JP","Shippori Mincho B1"],"グレイン",
  "cinematic photorealistic film still, pure black background, crimson red and metallic gold accent lighting only, volumetric light, subtle film grain, anamorphic",
  ["金は数字1か所か線1本","赤帯","ローダー"],["パステル","丸ゴシック","金の象徴物","金を全部に塗る"],["ink-splat","spotlight","lightning","letters-fall"],"ARM 01 / 深度 -8,000m","セールスレター / オプトイン（煽り）",
  "ARM 01 — SURFACE","深海から、","8桁へ。","今すぐ受け取る")
w("paper-black","黒紙の写真集","かっこいい・静か","cool",
  C("#121110","#1a1917","#1f1d1a","#f1ede4","#b9b3a6","#7d786e","rgba(241,237,228,.14)","#e9d8a6"),
  ["Playfair Display","Noto Serif JP","Noto Sans JP"],"紙の繊維 + 朝の光の帯",
  "editorial film photograph, night, single warm lamp light, deep black shadows, muted tones, Kodak Portra grain, quiet composition, lots of negative space",
  ["マスクからの文字浮上","ページ番号","紙の繊維"],["カラフルな差し色","太ゴシック","厚み影ボタン"],["tear","spotlight","letters-fall"],"p. 02 / Vol. 01 / Fig. 1","自己紹介 / ポートフォリオ / 写真家・作家",
  "p. 02 — About","Rin ","Takase","READ")
w("wafu-dark","和風ダーク","和風・壮大","dark",
  C("#06070b","#0d0f15","#151821","#efe9dc","#b8b2a4","#7a756b","rgba(239,233,220,.12)","#c0392b","#c9a227"),
  ["Cormorant Garamond","Shippori Mincho B1","Zen Kaku Gothic New"],"墨のにじみ + 火の粉",
  "dark Japanese fantasy, ukiyo-e influence meets cinematic film still, ink wash, fog, paper lantern light, muted vermilion and gold on black",
  ["縦書き見出し","漢数字","朱の割印バッジ"],["丸ゴシック","パステル"],["lightning","ink-splat","letters-fall"],"壱 弐 参 / 第一幕","作品公式サイト / イベント / 和の商材",
  "Act I","壱 ","去りし神々","事前登録")
w("neon-tokyo","ネオン","かっこいい・テック","cool",
  C("#070a14","#0b1020","#111833","#eef2ff","#b7c0e0","#6f7aa3","rgba(238,242,255,.12)","#22d3ee","#f0abfc"),
  ["Orbitron","M PLUS 1p","DotGothic16"],"走査線",
  "rainy neon city night through the window, cyan and magenta reflections, anamorphic lens flare, cyberpunk photography",
  ["走査線","ネオン管の点滅","HUD風の角括弧"],["明朝","暖色の金"],["neon-power","glitch-title","spotlight"],"01 // 02、SYS.01","ゲーム・配信者 / ガジェット / コミュニティ",
  "SYS.01 // ONLINE","夜を、","アップデート。","[ ENTER ]")
w("horror-west","洋画ホラー","怖い・映画っぽく","genre",
  C("#050708","#0b1014","#141b21","#e8e2d3","#a9a394","#6f6a5f","rgba(232,226,211,.12)","#ff4a1f","#4f9a95"),
  ["Bebas Neue","Special Elite","Cormorant Garamond"],"雨 + グレイン",
  "cinematic film still, 35mm anamorphic, photorealistic, muted teal and bone-white palette, heavy fog outside the window, practical lighting, film grain, unsettling",
  ["警告帯","タイプライター文字","雨"],["パステル","丸ゴシック"],["flare","lightning","glitch-title"],"ACT I / NIGHT 4 / CLASS I","作品公式サイト / イベント / ハロウィン",
  "ACT I — NIGHT 4","HOLLOW ","tide","SIGN THE LEDGER")
w("midnight-navy","深夜の紺","かっこいい・落ち着き","dark",
  C("#0b1426","#101b33","#16233f","#eef1f7","#b8c0d4","#7784a0","rgba(238,241,247,.12)","#f2c14e"),
  ["Cormorant Garamond","Noto Serif JP","Noto Sans JP"],"星の粒",
  "editorial photograph at midnight, deep navy blue tones, one warm desk lamp, soft film grain, calm and quiet",
  ["星の粒","細い金線","大きな余白"],["ネオン","太ゴシック"],["spotlight","letters-fall","none"],"Chapter 1 / 23:00","自己紹介 / コーチ・カウンセラー / 夜の商材",
  "Chapter 1","眠れない夜に、","読む手紙。","はじめる")
w("charcoal-brass","炭と真鍮","かっこいい・職人","cool",
  C("#1a1a1a","#222","#2a2a2a","#efe9df","#bdb5a8","#857c70","rgba(239,233,223,.12)","#b8862b"),
  ["Oswald","Noto Sans JP","Zen Old Mincho"],"金属のヘアライン",
  "workshop still life, dark charcoal tones with brass and warm tungsten light, macro texture of wood and metal, film grain",
  ["ヘアライン罫線","真鍮色の数字","工具のような角ばったUI"],["丸角","パステル"],["stamp","letters-fall","spotlight"],"No. 01 / LOT 2026","職人・工房 / 革・木・コーヒー / 簡易HP",
  "LOT 2026","手で、","作る。","注文する")
w("obsidian-mint","黒曜石とミント","かっこいい・クリーン","minimal",
  C("#0c0f0e","#111615","#171d1b","#f2fbf7","#b5c9c0","#728a80","rgba(242,251,247,.12)","#5ee3b0"),
  ["Inter Tight","Noto Sans JP","Space Mono"],"なし（面と線だけ）",
  "product photography on black glass, single mint green light edge, minimal, sharp shadows, high contrast",
  ["1色のミント","極太見出し","細い等幅キャプション"],["グラデ","装飾罫線"],["spotlight","none","letters-fall"],"01 — 02","SaaS・ツール / アプリ / 簡易HP",
  "01 — PRODUCT","速い。","それだけ。","試す")
w("noir-film","白黒映画","かっこいい・クラシック","cool",
  C("#0a0a0a","#141414","#1c1c1c","#f4f4f4","#c8c8c8","#8a8a8a","rgba(244,244,244,.14)","#f4f4f4"),
  ["Playfair Display","Noto Serif JP","Special Elite"],"フィルムの傷 + グレイン",
  "black and white film noir still, hard venetian blind shadows, cigarette smoke, 1950s, grain",
  ["白黒のみ","字幕風キャプション","フィルムの傷"],["色","丸角"],["spotlight","tear","glitch-title"],"REEL 1 / SCENE 4","作家・俳優 / イベント / 作品",
  "REEL 1 — SCENE 4","彼女は、","二度と戻らない。","予告を見る")
w("cyber-grid","端末の緑","テック・ハッカー","cool",
  C("#050805","#0a100a","#0f160f","#d7ffd7","#9fd39f","#5f8f5f","rgba(215,255,215,.12)","#39ff6a"),
  ["Space Mono","BIZ UDPGothic","VT323"],"走査線 + カーソル点滅",
  "close-up of a green phosphor terminal screen reflecting on a desk, dark room, scanlines, retro computing",
  ["等幅フォント","カーソル点滅","> プロンプト表記"],["セリフ","丸角","写真の多用"],["glitch-title","neon-power","none"],"$ step 01","AI・プログラミング講座 / ツール / コミュニティ",
  "$ run","echo ","'hello, world'","> execute")

# ============ B. 明るい・上品（10） ============
w("paper-white","紙・エディトリアル","上品・信頼","light",
  C("#f7f6f2","#efede7","#fff","#1c1b18","#3f3d38","#8a8780","#d9d6ce","#1f3a5f"),
  ["Playfair Display","Noto Serif JP","Noto Sans JP"],"紙の繊維",
  "editorial film photograph, natural window light, muted tones, Kodak Portra grain, quiet composition, lots of negative space, bright airy",
  ["罫線","ドロップキャップ","大余白"],["黒背景","グロー","グレイン"],["tear","none"],"p. 02 / Vol. 01","簡易HP（士業・医療）/ 自己紹介",
  "PHOTOGRAPHER, KAMAKURA","朝の光だけを、","撮る人。","CONTACT")
w("mono-minimal","白黒ミニマル","ミニマル・上品","minimal",
  C("#fff","#fafafa","#fff","#000","#222","#888","#e5e5e5","#000"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし",
  "monochrome photography, hard shadow, minimal composition, high key, black and white",
  ["1px罫線","極端なサイズ差","演出は最小"],["差し色2色以上","グロー","カーソル"],["none","letters-fall"],"01 — 02","ポートフォリオ / 建築・デザイン",
  "01 — 02","LESS.","","MORE")
w("ivory-serif","象牙のセリフ","上品・高級","light",
  C("#f4efe6","#ede6d8","#fff","#221c14","#4a4238","#8f867a","#d8d0c2","#8a6d3b"),
  ["Cormorant Garamond","Shippori Mincho B1","Noto Sans JP"],"なし（余白）",
  "luxury still life on ivory linen, soft diffused daylight, champagne gold accents, editorial, refined",
  ["細いセリフの大見出し","小さな金の飾り罫","イタリック"],["太ゴシック","原色"],["none","tear"],"I / II / III","高単価サービス / サロン / ブライダル",
  "Maison","静けさを、","身にまとう。","予約する")
w("linen-sage","麻とセージ","自然派・やさしい","light",
  C("#f3f1ea","#e9e6dc","#fff","#2f3a30","#4f5a4f","#8b948b","#d6d9cf","#6f8f6a"),
  ["Fraunces","Zen Kaku Gothic New","Noto Sans JP"],"麻の織り",
  "natural lifestyle photography, sage green and linen tones, soft daylight, plants and ceramics, calm",
  ["麻の質感","丸みのある見出し","葉の色1つ"],["黒背景","ネオン"],["ripple","none","stamp"],"Step 01","ヨガ・食・暮らし / 教室 / 簡易HP",
  "MORNING","深呼吸から、","はじめる。","体験する")
w("porcelain-blue","白磁と藍","上品・和洋","light",
  C("#f8f8f6","#eef1f3","#fff","#1b2a44","#3d4a63","#8590a3","#d7dde5","#1f4e8c"),
  ["Cormorant Garamond","Noto Serif JP","Noto Sans JP"],"陶器の釉薬",
  "white porcelain and indigo blue still life, soft north light, ceramic glaze texture, refined and calm",
  ["藍の細線","白磁のような余白","縦書きの小見出し"],["原色","グレイン"],["ripple","tear","none"],"一 / 二 / 三","工芸 / 器・食 / 旅館",
  "器","白と藍だけで、","足りる。","品を見る")
w("gallery-white","美術館の白","ミニマル・アート","minimal",
  C("#fff","#f5f5f5","#fff","#111","#333","#999","#e8e8e8","#111"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし",
  "art gallery white wall with a single framed photograph, museum lighting, minimal, wide",
  ["作品を1点だけ大きく","キャプションは11px","壁のような余白"],["装飾","グラデ"],["none","spotlight"],"No. 1 — 2026","ポートフォリオ / 作家・写真家 / 展示",
  "No. 1 — 2026","見る人が、","完成させる。","作品一覧")
w("morning-fog","霧の朝","静か・淡い","minimal",
  C("#f2f3f4","#e9ebee","#fff","#2a2f36","#555c66","#8f97a3","#dde1e6","#6b7f99"),
  ["Cormorant Garamond","Noto Serif JP","Noto Sans JP"],"霧のグラデ",
  "foggy morning landscape through the window, pale grey and soft blue tones, soft light, minimal",
  ["淡い青灰1色","ぼかしの背景","薄い文字"],["ビビッド","太ゴシック"],["ripple","none","tear"],"05:40 / 06:10","カウンセラー / 朝活 / 読み物",
  "05:40","まだ誰も、","起きていない。","読む")
w("swiss-grid","スイス・グリッド","かっこいい・国際様式","minimal",
  C("#fff","#f2f2f2","#fff","#000","#222","#777","#000","#e30613"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし（グリッド線）",
  "swiss international style poster, bold red black white, strict grid, helvetica-like typography, flat",
  ["赤1色","太い罫線のグリッド","左寄せ・左揃え"],["中央揃え","装飾"],["letters-fall","none"],"01 / 02 / 03","デザイン・制作 / 講座 / イベント",
  "01","Grid.","","ENTER")
w("letterpress","活版印刷","上品・クラフト","light",
  C("#f5efe3","#ece4d4","#fff9ee","#2b241c","#4e453a","#8c8273","#d9d0bf","#a63d2f"),
  ["Libre Baskerville","Shippori Mincho B1","Noto Sans JP"],"活版の凹み・インクのかすれ",
  "letterpress printed card on thick cream cotton paper, deep impression, single red ink, macro",
  ["かすれた文字","罫線と飾り罫","番号スタンプ"],["グロー","ネオン"],["stamp","tear","none"],"№ 1 / 1st Edition","文具・紙もの / 書籍・出版 / 招待",
  "1st Edition","一枚の紙が、","招待状になる。","申し込む")
w("newspaper","新聞","かっこいい・報道","light",
  C("#f6f4ef","#ebe8e1","#fff","#111","#333","#777","#111","#c8102e"),
  ["Playfair Display","Noto Serif JP","Noto Sans JP"],"新聞のインク",
  "vintage newspaper front page on a desk, black ink on off-white newsprint, one red headline, halftone photo",
  ["段組","太い横罫線","赤は見出し1つ"],["丸角","パステル"],["stamp","letters-fall"],"第1面 / 号外","号外的セールスレター / ニュース系発信",
  "号外","本日、","発売。","読む")

# ============ C. かわいい・ポップ（10） ============
w("pastel-pop","白地パステル","かわいい・明るい","cute",
  C("#fffdf8","#fff","#fff","#3d3552","#5b5470","#8f89a3","rgba(61,53,82,.1)","#ff7f9f","#5cc9a0"),
  ["Fredoka","Zen Maru Gothic","Noto Sans JP"],"なし",
  "cute 3D clay render, soft matte materials, pastel mint pink and lemon palette, soft studio lighting, rounded shapes, playful, clean bright background",
  ["スライドごとの背景色遷移","白カード","丸バッジ"],["黒背景","グレイン"],["stamp","card-flip","ripple"],"1 / 7、STEP 1","オプトイン / 教室・サロン",
  "MORNING ROUTINE","朝の10分で、","ぜんぶ整う。","はじめる")
w("pastel-pop-dark","黒地パステルクレイ","かわいい・でも大人っぽく","cute",
  C("#15131c","#1c1925","#221f2d","#fff8ee","#cfc9dc","#8d879f","rgba(255,255,255,.08)","#ff6f91","#4fd1a3"),
  ["Fredoka","Zen Maru Gothic","Noto Sans JP"],"なし",
  "cute 3D clay render, soft matte materials, pastel mint pink and lemon objects on a dark charcoal background, soft studio lighting, rounded shapes, playful",
  ["ブロブ形マスクの画像","厚み影ボタン","漂うクレイ玉"],["グレイン","グリッチ","明朝"],["stamp","card-flip","ripple"],"1 / 7、DAY 1","オプトイン / リンクまとめ / 講座",
  "7 DAYS FREE LESSON","がんばらない、","7日で習慣に。","無料で受け取る")
w("candy-shop","キャンディショップ","かわいい・ビビッド","cute",
  C("#fff5fa","#ffe9f3","#fff","#3b1f3a","#5c3d5a","#9a7f98","#f3d3e3","#ff3d8a","#3dd6ff"),
  ["Fredoka","Zen Maru Gothic","Noto Sans JP"],"ドット",
  "candy shop product photography, vivid pink and cyan, glossy plastic, playful, bright",
  ["ビビッド2色","ドット背景","丸いバッジ"],["黒","セリフ"],["ripple","stamp","card-flip"],"No.1 / 2 / 3","雑貨・コスメ / 若年層 / イベント",
  "NEW FLAVOR","甘さ、","限界突破。","買う")
w("sakura","桜","かわいい・和・春","cute",
  C("#fff8f9","#fdeef2","#fff","#3a2b30","#5e4a52","#9b878e","#f1dbe1","#e8879e","#7fb58a"),
  ["Zen Maru Gothic","Klee One","Noto Sans JP"],"花びらの散り",
  "cherry blossom season, soft pink petals, pale spring light, gentle bokeh, Japanese spring",
  ["花びらの粒","淡い桃色1つ","手描き風の罫線"],["黒","ネオン"],["ripple","stamp","tear"],"春 / 一 / 二","春の企画 / 教室 / 和菓子",
  "SPRING","春だけの、","おしらせ。","見る")
w("kawaii-sticker","シール風","かわいい・元気","cute",
  C("#fff","#fff7e0","#fff","#1c1c1c","#333","#777","#1c1c1c","#ffcc00","#ff5a5f"),
  ["Fredoka","Zen Maru Gothic","Noto Sans JP"],"太い黒縁",
  "sticker sheet illustration, thick black outlines, flat bright colors, die-cut white border, playful",
  ["太い黒縁","白フチ","傾けた配置"],["セリフ","グレイン"],["stamp","card-flip","letters-fall"],"01! / 02!","子ども向け / イベント / 楽しい商材",
  "NEW!","貼るだけで、","かわいい。","もらう")
w("macaron","マカロン","かわいい・上品","cute",
  C("#fffbf7","#f9f1ea","#fff","#4a3a3a","#6b5a5a","#a29090","#eadcd6","#e7a0b6","#a8c9c0"),
  ["Cormorant Garamond","Zen Maru Gothic","Noto Sans JP"],"なし",
  "macaron tower on a pastel table, milky pink mint and lavender, soft studio light, patisserie photography",
  ["ミルキーな3色","細いセリフ英字","丸角カード"],["黒","太い縁"],["ripple","none","card-flip"],"No. 01","パティスリー / ギフト / 女性向けサロン",
  "Pâtisserie","ひとくちの、","ごほうび。","予約する")
w("brutal","ブルータリズム","ギラギラ・尖った・明るい","gira",
  C("#fff","#f4f4f4","#fff","#000","#111","#666","#000","#ffe600","#ff3b30"),
  ["Archivo Black","BIZ UDPGothic","Space Mono"],"なし（4pxの黒罫線）",
  "flat graphic illustration, high contrast, risograph texture, two-color print, bold shapes, yellow and black",
  ["4pxの黒罫線","ズレたグリッド","黄色の塗り"],["グラデ","角丸","影","明朝"],["stamp","letters-fall","card-flip"],"№1、[01]","号外的セールスレター / イベント / 若年層",
  "№1 — EXTRA","デザイナー、","不要。","READ MORE")
w("picnic-gingham","ピクニック","かわいい・素朴","cute",
  C("#fffdf7","#fff3f3","#fff","#3b2c2c","#5c4a4a","#9a8888","#ead9d9","#d94b4b","#4c8b4c"),
  ["Fraunces","Zen Maru Gothic","Noto Sans JP"],"赤白のギンガムチェック",
  "picnic on a red and white gingham cloth, sunlight, homemade food, warm and cozy",
  ["ギンガムの帯","手書き風見出し","丸いシール"],["黒","ネオン"],["stamp","ripple","none"],"Menu 01","カフェ・食 / 手作り / 週末イベント",
  "PICNIC","週末は、","外で食べよう。","メニューを見る")
w("pop-art","ポップアート","ポップ・コミック","cute",
  C("#fff","#fff2b3","#fff","#111","#222","#666","#111","#ff2e63","#1e90ff"),
  ["Bangers","M PLUS 1p","Noto Sans JP"],"ハーフトーンドット",
  "pop art comic style illustration, halftone dots, bold black outlines, primary colors, speech bubble",
  ["ハーフトーン","吹き出し","太い黒縁の見出し"],["セリフ","淡色"],["stamp","letters-fall","card-flip"],"#01 / POW!","イベント / エンタメ / 若年層",
  "POW!","ドカンと、","一撃。","見る")
w("cream-soda","クリームソーダ","かわいい・レトロ喫茶","cute",
  C("#f3fbf6","#e6f6ea","#fff","#1f3a2e","#3f5a4d","#8aa596","#cfe3d6","#2ec27e","#ff5a5f"),
  ["Righteous","Kosugi Maru","Noto Sans JP"],"泡の粒",
  "cream soda in a tall glass at a retro Japanese cafe, emerald green and cherry red, soft window light",
  ["泡の粒","エメラルド1色","丸い赤のさくらんぼ"],["黒","太ゴシック"],["ripple","card-flip","stamp"],"No.1 / 2","喫茶・スイーツ / レトロ雑貨",
  "CREAM SODA","泡が消える前に。","","注文する")

# ============ D. レトロ（8） ============
w("retro-future","レトロフューチャー","レトロ・ポップ","retro",
  C("#f3e9d2","#e9dcc0","#fff8ea","#2b1d14","#4a3a2e","#8a7a6a","rgba(43,29,20,.18)","#e0662f","#3f7d6a"),
  ["Righteous","Kosugi Maru","Zen Kaku Gothic Antique"],"放射線 + グレイン",
  "1970s sci-fi poster art, airbrush illustration, warm cream orange and brown palette, grain, retro futurism",
  ["放射線","ストライプ帯","太陽のバッジ"],["ネオン","黒背景"],["card-flip","ripple","stamp"],"PHASE 1、No.01","商品LP / イベント / カフェ",
  "PHASE 1","未来は、","丸かった。","GO")
w("showa-kissa","昭和喫茶","レトロ・和","retro",
  C("#f4ecdc","#eadfc8","#fff8e8","#2c2017","#4b3d30","#8c7d6b","#d9cbb4","#7a4b2a","#2f5d4a"),
  ["Zen Old Mincho","Kosugi Maru","Noto Sans JP"],"木目 + 色あせ",
  "showa era Japanese cafe interior, dark wood, deep green velvet, cream walls, warm tungsten light, film photo",
  ["木目","深緑1色","縦書きのメニュー"],["ネオン","パステル"],["stamp","tear","none"],"其の一 / 品書き","喫茶・食 / 純喫茶的な商材",
  "品書き","珈琲は、","濃いめで。","品書きを見る")
w("vapor-80s","ヴェイパーウェーブ","レトロ・80年代","retro",
  C("#1a0b2e","#2a1245","#341a56","#ffe6fb","#e9b8ff","#a87fcf","rgba(255,230,251,.14)","#ff71ce","#01cdfe"),
  ["Orbitron","M PLUS 1p","Noto Sans JP"],"グリッドの地平線",
  "80s vaporwave aesthetic, sunset gradient of pink and purple, neon grid horizon, retro computer, palm silhouettes",
  ["グリッドの地平線","ピンク×シアン","日本語の飾り文字"],["セリフ","紙の質感"],["glitch-title","neon-power","ripple"],"1 9 8 4","音楽・アート / 若年層 / イベント",
  "1 9 8 4","夕日は、","ピンクだった。","再生")
w("y2k-chrome","Y2K クローム","レトロ・未来","retro",
  C("#e9f2ff","#dbe8ff","#fff","#0b1a33","#2a3a5c","#7a89a8","#c9d6ee","#3b82f6","#c0c0c0"),
  ["Orbitron","M PLUS 1p","Noto Sans JP"],"クロームの反射",
  "y2k aesthetic, chrome metallic objects, baby blue and silver, glossy reflections, early 2000s",
  ["クロームの見出し","水色1色","丸いボタン"],["紙の質感","セリフ"],["ripple","card-flip","glitch-title"],"2000 / 01","ファッション / 音楽 / 若年層",
  "2000","未来は、","もう来た。","OPEN")
w("pixel-8bit","ドット絵","ゲーム・レトロ","genre",
  C("#0f0f1a","#161626","#1e1e33","#f4f4f4","#c9c9d9","#8a8aa3","rgba(244,244,244,.12)","#ff5555","#ffd23f"),
  ["Press Start 2P","DotGothic16","Noto Sans JP"],"ドット",
  "8-bit pixel art scene, retro video game style, limited palette, crisp pixels",
  ["ドットフォント","ドット絵アイコン","ライフゲージ"],["セリフ","写実"],["glitch-title","stamp","card-flip"],"STAGE 1 / 1UP","ゲーム / ガジェット / 楽しい商材",
  "STAGE 1","PRESS ","START","▶ CONTINUE")
w("riso-poster","リソグラフ","レトロ・印刷","retro",
  C("#fbf7ee","#f3ecdc","#fff","#1c1c1c","#333","#777","#1c1c1c","#ff4fa3","#2f6df6"),
  ["Archivo Black","BIZ UDPGothic","Space Mono"],"リソのざらつき + 版ズレ",
  "risograph print poster, fluorescent pink and blue overprint, grainy texture, misregistration, bold shapes",
  ["蛍光2色の重ね","版ズレ","ざらつき"],["グラデ","写実"],["stamp","letters-fall","card-flip"],"No.01 / 2色","デザイン・ZINE / イベント / 若年層",
  "2色刷り","ズレてるのが、","正解。","申し込む")
w("vintage-map","古地図","レトロ・旅","retro",
  C("#efe4cf","#e6d8bc","#f8f0de","#2e2415","#4d3f2a","#8a7b62","#d4c5a5","#8b3a2a","#2f5f6b"),
  ["Libre Baskerville","Shippori Mincho B1","Noto Sans JP"],"羊皮紙",
  "antique sepia map with compass rose and hand-drawn coastlines, aged paper texture, warm light",
  ["羊皮紙","方位記号","点線の航路"],["ネオン","黒背景"],["tear","stamp","none"],"Ⅰ / Ⅱ / Ⅲ","旅・ツアー / 冒険系の講座 / 読み物",
  "Ⅰ","地図の外へ。","","出発する")
w("film-camera","フィルム写真","レトロ・ノスタルジー","retro",
  C("#f7f1e6","#efe6d6","#fff","#2b2520","#4f463d","#8c8377","#dccfbc","#d2691e"),
  ["Fraunces","Noto Serif JP","Noto Sans JP"],"フィルムの粒子 + 光漏れ",
  "golden hour film photograph, light leaks, warm orange tones, nostalgic, grainy",
  ["光漏れ","日付の焼き込み","粒子"],["ネオン","黒背景"],["tear","ripple","none"],"'26 09 04","写真家 / 旅 / 思い出系の商材",
  "'26 09 04","撮った日の、","光のまま。","見る")

# ============ E. 和・自然（7） ============
w("watercolor","水彩・手描き","やさしい・手づくり","nature",
  C("#fbfaf6","#f2efe6","#fff","#1f2a44","#3d4560","#8a8f9e","rgba(31,42,68,.14)","#c0392b","#1f5fa8"),
  ["Caveat","Klee One","Zen Kurenaido"],"にじみ + 紙",
  "watercolor illustration, ink outline, paper texture, soft washes, hand drawn",
  ["にじみマスク","手描き矢印","紙テクスチャ"],["黒背景","ネオン"],["tear","ripple","stamp"],"一、二、三","教室・ハンドメイド / 絵本・エッセイ",
  "一、はじめに","にじむくらいが、","ちょうどいい。","よむ →")
w("sumi-ink","墨一色","和・静謐","nature",
  C("#f6f5f0","#eeece5","#fff","#141414","#333","#888","#d8d6cf","#141414"),
  ["Shippori Mincho B1","Zen Old Mincho","Noto Sans JP"],"墨のかすれ",
  "sumi-e ink painting, single black ink on white washi paper, brush strokes, minimal",
  ["縦書き","墨のかすれ","余白"],["色","丸ゴシック"],["tear","letters-fall","none"],"一 / 二 / 三","書・茶・禅 / 和の教室",
  "一","余白に、","書く。","読む")
w("indigo-aizome","藍染","和・落ち着き","nature",
  C("#0e1f3a","#132a4d","#1a355e","#eef3fa","#b9c6dc","#7c8ea9","rgba(238,243,250,.12)","#e8dcc0"),
  ["Shippori Mincho B1","Noto Serif JP","Noto Sans JP"],"布の織り",
  "indigo dyed fabric texture, deep blue with white shibori patterns, natural light, Japanese craft",
  ["布の織り","生成りの文字","絞りの模様"],["ネオン","原色"],["tear","ripple","none"],"一 / 二","染め・織り / 民芸 / 旅館",
  "藍","深く、","染まる。","工房を見る")
w("forest-moss","森と苔","自然・深緑","nature",
  C("#0f1a12","#15231a","#1b2d21","#e9f0e6","#b7c6b6","#748a77","rgba(233,240,230,.12)","#9ad17a"),
  ["Fraunces","Zen Kaku Gothic New","Noto Sans JP"],"木漏れ日",
  "deep forest with moss and soft light rays, dark green tones, misty, nature photography",
  ["木漏れ日のグラデ","緑1色","木目の罫線"],["ネオン","ピンク"],["ripple","spotlight","none"],"Trail 01","アウトドア / 自然体験 / 環境系",
  "TRAIL 01","森の音を、","聞きに行く。","予約する")
w("ocean-blue","海の青","自然・爽快","nature",
  C("#f4fbff","#e6f4fc","#fff","#0b2a45","#2c4a66","#7c95ad","#cfe3f0","#0a84ff","#ffb703"),
  ["Fraunces","Zen Kaku Gothic New","Noto Sans JP"],"波の線",
  "bright ocean and white sand, clear blue water, summer sunlight, wide and airy",
  ["波の線","青1色","白い大余白"],["黒背景","グレイン"],["ripple","none","letters-fall"],"Wave 01","マリン・旅 / 夏イベント / 爽やかな商材",
  "SUMMER","青が、","足りない。","行く")
w("autumn-kinmokusei","金木犀","自然・秋","nature",
  C("#fbf6ee","#f5ecdd","#fff","#3a2a1a","#5c4a36","#9a8b78","#e3d6c2","#e07a1f","#6d4c2b"),
  ["Fraunces","Noto Serif JP","Noto Sans JP"],"落ち葉",
  "autumn afternoon, orange osmanthus flowers and warm golden light, soft focus, cozy",
  ["橙1色","落ち葉の粒","温かい影"],["ネオン","黒背景"],["ripple","tear","none"],"秋 / 一","季節企画 / 食・お茶 / 読み物",
  "AUTUMN","香りで、","思い出す。","読む")
w("snow-country","雪国","自然・冬","nature",
  C("#f7f9fb","#eef2f6","#fff","#1f2933","#3e4c59","#8a98a8","#d9e1ea","#c62828"),
  ["Shippori Mincho B1","Noto Serif JP","Noto Sans JP"],"雪の粒",
  "snow country landscape, white and pale grey, a single red element, quiet winter light",
  ["雪の粒","赤1点","静かな余白"],["ネオン","パステル"],["ripple","none","tear"],"冬 / 一","冬の企画 / 温泉・宿 / 静かな商材",
  "WINTER","白の中の、","赤ひとつ。","予約する")

# ============ F. ビジネス・テック（5） ============
w("trust-navy","信頼の紺","ビジネス・信頼","business",
  C("#fff","#f4f6fa","#fff","#0f2140","#33415c","#7d8aa3","#d7dde8","#0f2140","#f2b705"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし",
  "corporate photography, navy blue and white, clean office with daylight, confident and calm",
  ["紺1色","太い見出し","数字のタイル"],["グレイン","装飾"],["none","letters-fall"],"01 / 02 / 03","士業・コンサル / BtoB / 採用",
  "SERVICE","数字で、","約束する。","相談する")
w("fintech-emerald","エメラルドの金融","ビジネス・堅実","business",
  C("#0b1f1a","#0f2923","#14332c","#eaf5f0","#b5cfc4","#6f9184","rgba(234,245,240,.12)","#2ecc8f","#d4af37"),
  ["Inter Tight","Noto Sans JP","Space Mono"],"なし",
  "premium financial product photography, deep emerald green and gold accents, dark, sharp",
  ["深緑1色","金の細線","等幅の数字"],["パステル","丸角"],["spotlight","none","letters-fall"],"Q1 / Q2","金融・投資 / 高単価コンサル",
  "Q1 — REPORT","増やすより、","減らさない。","資料を見る")
w("blueprint","青図面","テック・設計","business",
  C("#0b3d91","#0a3480","#0d47a1","#eaf2ff","#bcd0f5","#7fa0d9","rgba(234,242,255,.18)","#fff"),
  ["Space Mono","BIZ UDPGothic","Noto Sans JP"],"方眼 + 白線",
  "architectural blueprint, white technical lines on deep blue paper, grid, measurements",
  ["白線の方眼","寸法線","等幅フォント"],["セリフ","丸角"],["none","letters-fall","glitch-title"],"Fig. 1 / Rev. A","建築・製造 / 設計・エンジニア / 講座",
  "Fig. 1 — Rev. A","設計図から、","はじめる。","図面を見る")
w("data-dashboard","ダッシュボード","テック・数値","business",
  C("#0d1117","#111827","#161e2e","#e6edf3","#aab4c2","#6b7785","rgba(230,237,243,.12)","#3fb6ff","#ff7a45"),
  ["Inter Tight","Noto Sans JP","Space Mono"],"なし（カードとグラフ）",
  "dark analytics dashboard on a monitor, glowing cyan charts and numbers, clean UI photography",
  ["数字のタイル","折れ線のスパークライン","シアン1色"],["セリフ","紙の質感"],["none","spotlight"],"KPI 01","SaaS / データ・AI / BtoB",
  "KPI","見える数字だけ、","信じる。","デモを見る")
w("clinic-clean","クリニックの白","医療・安心","business",
  C("#fff","#f3f8fb","#fff","#1d2b36","#3d4f5e","#84939f","#dbe6ee","#2a9d8f"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし",
  "clean medical clinic interior, white and pale teal, soft daylight, calm and hygienic",
  ["白と水色","丸みのある見出し","安心の余白"],["黒","ネオン"],["none","ripple"],"Step 1 / 2 / 3","医療・歯科 / 整体 / 健康商材",
  "STEP 1","まず、","話を聞く。","予約する")


# ============ G. ジャンル（ホラー・SF・ゲーム）（11 + 既存2） ============
w("horror-jp","Jホラー","怖い・和・湿った","genre",
  C("#0a0c0b","#10130f","#171b16","#d9dcd3","#a2a79c","#6a6f66","rgba(217,220,211,.12)","#b1161b","#7f8c7a"),
  ["Yuji Syuku","Shippori Mincho B1","Noto Serif JP"],"ビデオノイズ + 湿った緑がかった白",
  "Japanese horror film still, desaturated greenish grey, damp abandoned school corridor, fluorescent flicker, VHS grain, unsettling stillness",
  ["縦書きの筆文字","色あせた緑白","赤1点（血ではなく朱）"],["パステル","丸ゴシック","ネオン"],["glitch-title","flare","letters-fall"],"一日目 / 午前二時","ホラー作品 / 怪談イベント / 夏の企画",
  "午前二時","振り向いては、","いけない。","扉を開ける")
w("horror-gothic","ゴシックホラー","怖い・耽美","genre",
  C("#0b070d","#130b16","#1b1020","#ece3e6","#b8a9b3","#7d6f79","rgba(236,227,230,.12)","#8e0f24","#c9a24a"),
  ["Cinzel","Shippori Mincho B1","Noto Serif JP"],"蝋燭の揺れ + ビネット",
  "gothic horror painting, candlelit cathedral interior, deep purple black shadows, crimson velvet, tarnished gold, oil painting texture, dramatic chiaroscuro",
  ["蝋燭色のビネット","細いセリフの大見出し","装飾罫線は1本だけ"],["丸角","ポップな色"],["spotlight","letters-fall","tear"],"Ⅰ / Ⅱ / Ⅲ、第一夜","小説・ゲーム作品 / ゴス系ブランド / イベント",
  "第一夜","招かれざる","客。","門を叩く")
w("horror-vhs","見つかった映像","怖い・記録映像","genre",
  C("#050605","#0b0d0a","#121510","#d5dccf","#9aa392","#606860","rgba(213,220,207,.12)","#ff2d2d","#7dff8a"),
  ["VT323","DotGothic16","BIZ UDPGothic"],"走査線 + トラッキングノイズ + REC",
  "found footage night vision still, green tinted camcorder view, heavy VHS noise and tracking lines, dark forest, flashlight beam, blurry motion",
  ["REC と日時の焼き込み","トラッキングノイズ","ナイトビジョンの緑"],["セリフ","上品な余白"],["glitch-title","flare","none"],"TAPE 01 / 23:58:04","ホラー作品 / ARG・謎解き / 配信企画",
  "REC ● 23:58:04","この映像は、","編集されていない。","再生する")
w("sf-space","宇宙SF","SF・壮大","genre",
  C("#04060e","#080c1a","#0e1426","#e8eeff","#aeb9d8","#6c7799","rgba(232,238,255,.12)","#6ea8ff","#ffb547"),
  ["Exo 2","Noto Sans JP","Space Mono"],"星の粒 + 薄い HUD グリッド",
  "cinematic space photograph, vast starfield, distant planet with thin ring, cold blue light, one warm orange engine glow, wide anamorphic, awe",
  ["星の粒","細い HUD 線","距離・座標の表記"],["紙の質感","暖色の金"],["spotlight","letters-fall","glitch-title"],"SOL 01 / 0.42 AU","SF作品 / 宇宙・科学 / 壮大な講座",
  "SOL 01 — 0.42 AU","地球が、","小さく見える。","出航する")
w("sf-lab","白いSF","SF・クリーン・冷たい","genre",
  C("#f4f7fa","#e9eef4","#fff","#0e1a2b","#34455c","#8593a8","#d3dce6","#e8262a","#3b7dd8"),
  ["Michroma","Noto Sans JP","Inter"],"なし（白い面と細線）",
  "clean white science fiction interior, curved white corridor, soft even lighting, one red indicator light, minimal, wide",
  ["白い面と細線","赤のインジケーター1つ","等間隔の英数字ラベル"],["グレイン","装飾"],["none","letters-fall","spotlight"],"UNIT 01 / SEC.04","テック製品 / 研究・医療AI / ミニマルなSF",
  "UNIT 01 — SEC.04","静かに、","起動する。","開始")
w("sf-mecha","メカ・格納庫","SF・重厚・警告","genre",
  C("#0d0e10","#141517","#1b1c1f","#eceae4","#b3b0a8","#75726b","rgba(236,234,228,.12)","#ff7a00","#ffd400"),
  ["Teko","M PLUS 1p","BIZ UDPGothic"],"黄黒ストライプ + 金属パネル",
  "cinematic hangar interior with a giant mech silhouette, orange warning lights, yellow-black hazard stripes, steel panels, steam, dramatic scale",
  ["黄黒ストライプ","警告オレンジ","型番のラベル（TYPE-01）"],["パステル","セリフ"],["lightning","glitch-title","letters-fall"],"TYPE-01 / UNIT 02","ゲーム・ロボ作品 / ガジェット / 製造",
  "TYPE-01 — HANGAR","起動まで、","あと3秒。","搭乗する")
w("game-rpg","ファンタジーRPG","ゲーム・冒険","genre",
  C("#0f1410","#161d17","#1e271f","#efe6cf","#c2b89f","#857d6a","rgba(239,230,207,.14)","#d6a640","#4f8fd6"),
  ["Cinzel","Shippori Mincho B1","Noto Sans JP"],"羊皮紙の縁 + 魔法の粒",
  "fantasy RPG concept art, ancient castle on a cliff at dusk, glowing blue magic particles, gold-lit windows, painterly, epic",
  ["羊皮紙色の見出し","金の細い縁1本","クエスト風の番号"],["ネオン","丸ゴシック"],["lightning","card-flip","letters-fall"],"QUEST 01 / LV.5","ゲーム作品 / コミュニティ / 冒険系の講座",
  "QUEST 01","はじまりの","村へ。","冒険に出る")
w("game-fps","バトル・FPS","ゲーム・緊張","genre",
  C("#0a0b0a","#111311","#181b18","#e8e6df","#aeaca3","#6f6e66","rgba(232,230,223,.12)","#ff6a00","#7fa650"),
  ["Black Ops One","Noto Sans JP","Space Mono"],"HUD + 走査線",
  "tactical shooter key art, soldier silhouette in smoke, orange flare, olive green and black, dust particles, gritty, cinematic",
  ["HUD 風の角括弧","オレンジ1色","カウントダウン"],["パステル","セリフ","丸角"],["lightning","glitch-title","flare"],"MISSION 01 / 03:00","ゲーム・配信 / 大会 / 熱い商材",
  "MISSION 01","始まる前に、","読め。","参加する")
w("game-esports","eスポーツ","ゲーム・競技・派手","genre",
  C("#08070f","#0e0c19","#151226","#f1efff","#b9b4d8","#736e94","rgba(241,239,255,.12)","#8b5cf6","#22d3ee"),
  ["Rajdhani","M PLUS 1p","Noto Sans JP"],"斜めカット + 光の筋",
  "esports arena stage with purple and cyan stage lights, dramatic haze, diagonal light beams, crowd silhouettes, high energy",
  ["斜めカットの帯","紫×シアン","チーム名のような大文字英字"],["紙の質感","セリフ"],["neon-power","glitch-title","lightning"],"ROUND 01 / VS","大会・チーム / 配信者 / ガジェット",
  "ROUND 01 — VS","勝つ準備は、","できてる。","エントリー")
w("anime-kinetic","アニメ・ポスター","エンタメ・熱量・斜め","genre",
  C("#fff","#f3f3f3","#fff","#111","#222","#777","#111","#e60012","#111"),
  ["Zen Kaku Gothic New","Shippori Mincho B1","Noto Sans JP"],"斜めの赤帯 + 集中線",
  "anime movie poster style illustration, dramatic low angle of a character against a bright sky, bold red diagonal band, speed lines, high contrast",
  ["極太の斜め帯","赤1色","キャッチコピーを縦と横で交差"],["パステル","丸角"],["letters-fall","stamp","lightning"],"第1話 / 予告","アニメ・漫画作品 / イベント / 熱い告知",
  "第1話 予告","全部、","ぶつけろ。","予告を見る")
w("post-apoc","荒廃した世界","SF・荒野・錆","genre",
  C("#14110d","#1b1712","#231e18","#e6dcc8","#b5a88e","#7a7060","rgba(230,220,200,.12)","#d3552b","#8a9a5b"),
  ["Special Elite","BIZ UDPGothic","Noto Sans JP"],"砂嵐 + 錆の擦れ",
  "post-apocalyptic wasteland, rusted vehicle in sand, dust storm, muted sand and rust palette, lone figure with a backpack, cinematic wide",
  ["錆色1つ","タイプライター文字","擦れたスタンプ"],["パステル","グロー"],["stamp","tear","glitch-title"],"DAY 214 / SECTOR 7","サバイバル系作品 / ゲーム / 硬派な商材",
  "DAY 214","残ったのは、","記録だけ。","記録を読む")


# ============ A2. ダーク・壮大（追加4） ============
w("deep-ocean","深海の青","ダーク・壮大・静か","dark",
  C("#03111c","#061a29","#0a2236","#e6f3fa","#a9c3d1","#6c8595","rgba(230,243,250,.12)","#2fc4e0","#8fe3ff"),
  ["Cormorant Garamond","Noto Serif JP","Noto Sans JP"],"水面からの光の筋 + 粒",
  "deep underwater cinematic photograph, dark teal blue, light rays from the surface, floating particles, vast and quiet",
  ["光の筋","青緑1色","深度の表記"],["暖色の金","丸ゴシック"],["spotlight","ripple","letters-fall"],"DEPTH -200m","壮大な講座 / 海・旅 / 静かな商材",
  "DEPTH -200m","光は、","上にある。","潜る")
w("volcanic","溶岩","ダーク・熱い","dark",
  C("#0c0806","#150c08","#1e110b","#f6ebe2","#c9b3a4","#85705f","rgba(246,235,226,.12)","#ff5a1f","#ffb347"),
  ["Oswald","Noto Sans JP","BIZ UDPGothic"],"火の粉 + 熱のゆらぎ",
  "cinematic photograph of glowing lava cracks on black volcanic rock, orange heat glow, embers, dark",
  ["火の粉","橙1色","温度・段階の表記"],["パステル","セリフ"],["lightning","flare","letters-fall"],"PHASE 01 / 1,200℃","熱い商材 / スポーツ / 挑戦系",
  "PHASE 01","燃えるなら、","今。","火をつける")
w("storm","嵐","ダーク・緊張","dark",
  C("#0b0e12","#12161c","#191e26","#e9edf2","#aeb6c2","#6f7886","rgba(233,237,242,.12)","#9ecbff","#ffe066"),
  ["Bebas Neue","Noto Sans JP","Noto Serif JP"],"雨 + 雷の一瞬の白",
  "dramatic storm photograph, dark grey clouds, a single lightning bolt, rain, high contrast, cinematic wide",
  ["雨","雷の一瞬の白","警報風の表記"],["パステル","丸角"],["lightning","flare","letters-fall"],"WARNING 01 / 風速 30m","覚悟系の商材 / 作品 / 告知",
  "WARNING 01","嵐は、","来る。","備える")
w("cinema-black","映画の予告","ダーク・壮大・白黒","dark",
  C("#000","#0a0a0a","#111","#fff","#cfcfcf","#8a8a8a","rgba(255,255,255,.14)","#fff","#c9c9c9"),
  ["Bebas Neue","Noto Sans JP","Cormorant Garamond"],"レターボックスの黒帯 + グレイン",
  "black and white cinematic trailer still, widescreen letterbox, high contrast, film grain, dramatic",
  ["黒帯（上下）","白黒のみ","公開日の表記"],["色","丸角"],["letters-fall","spotlight","glitch-title"],"COMING SOON / 2026.09","作品告知 / イベント / ローンチ",
  "COMING SOON","近日、","公開。","予告を見る")

# ============ H. ミニマル（追加3） ============
w("minimal-black","黒ミニマル","ミニマル・黒","minimal",
  C("#000","#0a0a0a","#0a0a0a","#fff","#bdbdbd","#777","rgba(255,255,255,.14)","#fff","#fff"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし",
  "minimal product photography on pure black, a single object, soft light, lots of empty space",
  ["白黒のみ","1px罫線","極端なサイズ差"],["差し色","グロー","装飾"],["none","letters-fall"],"01","ポートフォリオ / ブランド / 高単価",
  "01","黒と、","白だけ。","見る")
w("minimal-warm","生成りミニマル","ミニマル・温かい","minimal",
  C("#f4efe7","#ece5da","#fff","#2a2622","#57504a","#948b81","#dcd3c6","#2a2622","#b6543a"),
  ["Fraunces","Noto Serif JP","Noto Sans JP"],"紙",
  "warm minimal still life on beige linen, one ceramic object, soft natural light, empty space",
  ["生成りの面","物は1つ","小さなセリフ英字"],["ビビッド","黒背景"],["none","tear","ripple"],"No. 1","暮らし・工芸 / サロン / 自己紹介",
  "No. 1","少ないほど、","豊か。","見る")
w("minimal-type","文字だけ","ミニマル・タイポ","minimal",
  C("#fff","#f7f7f7","#fff","#000","#222","#888","#000","#000","#ff3b30"),
  ["Inter Tight","Zen Kaku Gothic New","Noto Sans JP"],"なし（文字が画像）",
  "giant black typography poster on white, a single word, extreme scale, flat",
  ["見出し20vw","画像なし前提","赤1点"],["写真","グラデ"],["letters-fall","none"],"01 / 02","文字主役の告知 / デザイン / 講座",
  "01","文字だけで、","勝つ。","読む")

# ============ I. かっこいい・クール（追加3） ============
w("concrete","コンクリート","クール・硬派","cool",
  C("#2b2d2f","#333638","#3b3e41","#f1f1f0","#c3c5c6","#8a8d90","rgba(241,241,240,.12)","#f1f1f0","#ff8a00"),
  ["Oswald","Noto Sans JP","Space Mono"],"打ちっぱなしの質感",
  "brutalist concrete architecture photograph, grey textured walls, hard shadow, minimal, overcast",
  ["灰の面","硬い影","安全オレンジ1点"],["パステル","丸角"],["spotlight","letters-fall","none"],"BLOCK 01","建築・不動産 / 男性向け / 硬派な商材",
  "BLOCK 01","削ぎ落として、","残ったもの。","見る")
w("carbon-red","カーボン×赤","クール・速い","cool",
  C("#0e0f11","#15171a","#1c1f23","#f5f5f5","#b9bcc2","#767a82","rgba(245,245,245,.12)","#e10600","#f5f5f5"),
  ["Teko","Noto Sans JP","Rajdhani"],"カーボンの織り + 斜線",
  "carbon fiber texture with a single red racing stripe, studio light, sharp, automotive",
  ["斜めの赤ライン1本","カーボンの織り","ラップタイム風の数字"],["セリフ","紙の質感"],["neon-power","letters-fall","lightning"],"LAP 01 / 0.01s","車・スポーツ / ガジェット / 速さ系",
  "LAP 01","速さは、","正義。","加速する")
w("street-mono","ストリート","クール・若い","cool",
  C("#f2f2f2","#e8e8e8","#fff","#111","#333","#777","#111","#111","#c6ff00"),
  ["Archivo Black","M PLUS 1p","Space Mono"],"コピー機のざらつき + テープ",
  "street photography, black and white, urban wall with torn posters, one neon yellow-green element, grainy",
  ["白黒 + 蛍光1色","テープで貼った風","傾けた見出し"],["セリフ","パステル"],["stamp","letters-fall","glitch-title"],"VOL.01 / DROP","アパレル / 音楽 / 若年層",
  "DROP 01","路上から、","始める。","GET")

# ============ J. 商材屋（ギラギラ）（追加5） ============
w("gold-rush","黒金","ギラギラ・王道","gira",
  C("#000","#0b0a07","#14120b","#fff","#d9d2bd","#8f8770","rgba(229,193,88,.25)","#e5c158","#d10a1e"),
  ["Bebas Neue","Noto Sans JP","Shippori Mincho B1"],"金の粒 + 光の筋",
  "luxurious black and gold cinematic still, golden light rays and particles on black, dramatic",
  ["金は見出し1つとボタンまで","赤の帯","光の筋"],["パステル","丸ゴシック","金の象徴物"],["spotlight","letters-fall","ink-splat"],"第1章 / ¥","セールスレター / 高額商材 / ローンチ",
  "第1章","結果で、","黙らせる。","今すぐ手に入れる")
w("red-alert","赤ベタ","ギラギラ・セール","gira",
  C("#d10a1e","#b8081a","#a10716","#fff","#ffe3e6","#f4a3ab","rgba(255,255,255,.3)","#ffe600","#111"),
  ["Archivo Black","Noto Sans JP","BIZ UDPGothic"],"斜めストライプ",
  "bold red poster background with a single black object, flat, high contrast, sale advertisement style",
  ["全面の赤","黄色の見出し","残り数・期限の表記"],["セリフ","グラデ"],["stamp","letters-fall","lightning"],"本日限り / 残り","セール / 期間限定 / キャンペーン",
  "本日限り","今日を、","逃すな。","参加する")
w("money-green","札束グリーン","ギラギラ・稼ぐ","gira",
  C("#061a12","#0a2419","#0f2f20","#eafff3","#b5d8c4","#6f9682","rgba(234,255,243,.12)","#2ecc71","#e5c158"),
  ["Bebas Neue","Noto Sans JP","Space Mono"],"紙幣の細線パターン",
  "dark green cinematic still with gold coins and green light, wealth mood, dramatic spotlight",
  ["深緑の面","等幅の数字","金は数字1か所"],["パステル","丸ゴシック"],["spotlight","letters-fall","neon-power"],"¥ / 第1章","副業・投資系 / 収益化 / 高額商材",
  "第1章","数字は、","嘘をつかない。","受け取る")
w("flash-yellow","黄×黒","ギラギラ・警告","gira",
  C("#ffe600","#f5dc00","#fff","#000","#111","#6b6400","#000","#000","#d10a1e"),
  ["Bebas Neue","Zen Kaku Gothic New","BIZ UDPGothic"],"黄黒の斜線 + 集中線",
  "bright yellow background with bold black shapes and a warning stripe, flat graphic, loud",
  ["全面の黄","黒の極太見出し","警告の斜線"],["セリフ","淡色"],["stamp","lightning","letters-fall"],"激 / 01","激安・大量 / 号外 / イベント",
  "警告","目を、","逸らすな。","今すぐ見る")
w("royal-purple","紫×金","ギラギラ・高級","gira",
  C("#12061f","#1b0b2c","#24123a","#f7efff","#cdb9e0","#8a72a3","rgba(247,239,255,.12)","#e5c158","#c084fc"),
  ["Cinzel","Shippori Mincho B1","Noto Sans JP"],"ベルベット + 金の粒",
  "royal purple velvet with gold light particles, luxurious, dramatic spotlight, cinematic",
  ["紫の面","金は見出し1つ","VIP・招待の語彙"],["パステル","丸ゴシック","金の象徴物"],["spotlight","letters-fall","card-flip"],"Ⅰ / VIP","高額コンサル / 会員制 / 占い・スピリチュアル",
  "VIP","選ばれた人だけに。","","招待を受ける")


# ============ 100種化の追加（24） ============
# --- dark +2 ---
w("aurora","オーロラ","ダーク・壮大・幻想","dark",
  C("#050a14","#091120","#0e182c","#eaf2ff","#b4c4dc","#6f7f9a","rgba(234,242,255,.12)","#5ef0b0","#b388ff"),
  ["Cormorant Garamond","Noto Serif JP","Noto Sans JP"],"オーロラの帯 + 星",
  "aurora borealis over a snowy field at night, green and violet light curtains, stars, wide, quiet",
  ["緑と紫の光の帯","星の粒","静かな余白"],["赤","丸ゴシック"],["spotlight","ripple","letters-fall"],"NIGHT 01 / 68°N","旅・北欧 / 壮大な講座 / 幻想系の作品",
  "NIGHT 01 — 68°N","空が、","動いた夜。","見に行く")
w("eclipse","日蝕","ダーク・壮大・儀式","dark",
  C("#000","#070707","#0f0f0f","#f5f2ea","#c4c0b4","#7e7b72","rgba(245,242,234,.12)","#f2d58a","#f5f2ea"),
  ["Cinzel","Shippori Mincho B1","Noto Sans JP"],"コロナの輪 + グレイン",
  "total solar eclipse, black sun with a thin white-gold corona ring, dark desert, cinematic, awe",
  ["輪は1つ","白金の細線","時刻の表記"],["パステル","丸角"],["spotlight","letters-fall","flare"],"TOTALITY 02:14","ローンチ / 作品 / 一度きりのイベント",
  "TOTALITY — 02:14","太陽が、","隠れる2分。","立ち会う")
# --- light +3 ---
w("botanical","植物図鑑","上品・クラシック・自然","light",
  C("#f7f4ea","#efeadb","#fff","#1f2f22","#41503f","#8a927f","#d8d3c2","#1f5b3a","#b8402e"),
  ["Libre Baskerville","Noto Serif JP","Noto Sans JP"],"古い図鑑の紙 + 銅版画の線",
  "vintage botanical illustration of a fern and leaves on cream paper, copperplate engraving, muted green",
  ["銅版画風の線","学名のような小さなラベル","深緑1色"],["ネオン","太ゴシック"],["tear","none","ripple"],"Fig. 12 / Pl. Ⅲ","植物・ハーブ / 教室 / 上品な自然系",
  "Pl. Ⅲ — Fig. 12","名前を知ると、","見え方が変わる。","図鑑を開く")
w("marble","大理石","上品・高級・白","light",
  C("#f8f7f5","#f0eeeb","#fff","#1a1a1a","#4a4a4a","#8f8f8f","#dedbd6","#1a1a1a","#b89b5e"),
  ["Cormorant Garamond","Shippori Mincho B1","Noto Sans JP"],"大理石の筋",
  "white marble surface with grey veins, a single gold ring and soft shadow, luxury product photography",
  ["大理石の筋","金は細線1本","細いセリフ"],["ビビッド","丸角"],["none","tear","spotlight"],"Ⅰ / Ⅱ","ジュエリー / サロン / 高単価サービス",
  "Ⅰ","削って、","残す。","予約する")
w("kraft","クラフト紙","上品・素朴・手仕事","light",
  C("#d9c3a0","#cfb68e","#e8d8bb","#2b2218","#4f4232","#8a7a63","#bfa987","#1d1d1d","#b8402e"),
  ["Fraunces","Zen Maru Gothic","Noto Sans JP"],"クラフト紙の繊維 + スタンプ",
  "fresh bread wrapped in brown kraft paper with a black rubber stamp, warm daylight, rustic",
  ["クラフト紙の面","黒のスタンプ","紐・タグ"],["ネオン","グラデ"],["stamp","tear","none"],"No. 01 / LOT","パン・食品 / 手仕事 / ギフト",
  "LOT 01","包むところから、","はじまる。","注文する")
# --- cute +2 ---
w("shojo-manga","少女漫画","かわいい・キラキラ","cute",
  C("#fff","#fff3f7","#fff","#3a2a34","#5e4c57","#9c8a95","#f1d8e2","#ff7fb0","#7fd3ff"),
  ["Zen Maru Gothic","Klee One","Noto Sans JP"],"スクリーントーン + キラキラ",
  "shojo manga style illustration, sparkling eyes, screentone dots, flowers and sparkles, pastel pink",
  ["スクリーントーン","キラキラの粒","吹き出し風の見出し"],["黒背景","セリフ"],["stamp","card-flip","ripple"],"第1話 / ♡","少女向け / 恋愛系 / 推し活",
  "第1話","はじめて、","ときめいた。","つづきを読む")
w("yumekawa","ゆめかわ","かわいい・夢","cute",
  C("#f6f0ff","#ece3ff","#fff","#4a3a6b","#6d5e8c","#a396bf","#e2d6f5","#c48bff","#8fe3d9"),
  ["Fredoka","M PLUS Rounded 1c","Noto Sans JP"],"雲 + 星の粒",
  "dreamy pastel clouds and a soft rainbow over a lavender sky, sparkles, cute, airy",
  ["雲の形","ラベンダー×ミント","星の粒"],["黒","太ゴシック"],["ripple","card-flip","stamp"],"1 / 7 ☆","雑貨・コスメ / 若年層 / 癒やし系",
  "☆ DREAM","ふわふわの、","毎日を。","はじめる")
# --- retro +2 ---
w("showa-pop","昭和ポップ","レトロ・60年代","retro",
  C("#fff3d6","#f7e6b8","#fff9e8","#3b2414","#5c3d2a","#9a7d63","#e0cba0","#f26b1d","#2f7a5a"),
  ["Righteous","Kosugi Maru","Noto Sans JP"],"花柄 + 太い縁取り",
  "1960s Japanese living room with a bold floral pattern, orange telephone, cream and brown, retro pop",
  ["花柄の帯","橙1色","丸い太縁の見出し"],["ネオン","黒背景"],["card-flip","stamp","ripple"],"第1回 / No.1","雑貨・喫茶 / 昭和イベント / レトロ商材",
  "第1回","あの頃の、","色で。","見る")
w("art-deco","アールデコ","レトロ・華麗","retro",
  C("#0f0e0c","#171512","#1f1c17","#f3ead8","#c9bfa8","#857c69","rgba(243,234,216,.14)","#d4b46a","#f3ead8"),
  ["Cinzel","Shippori Mincho B1","Noto Sans JP"],"扇形の幾何模様 + 金の線",
  "art deco hotel lobby with gold geometric fan patterns, black and cream, 1920s glamour",
  ["扇形の幾何模様","金の細線","大文字の英字"],["丸角","パステル"],["letters-fall","spotlight","card-flip"],"No. 1 / 1925","ホテル・バー / ブライダル / 華やかなイベント",
  "1925","夜会は、","続く。","招待を受ける")
# --- nature +3 ---
w("desert","砂漠","自然・乾いた・広い","nature",
  C("#f3e6d0","#ead9bc","#fff8ec","#3b2a1a","#5f4a33","#9a8467","#d9c6a6","#c8642b","#5b8fb9"),
  ["Fraunces","Noto Sans JP","Noto Serif JP"],"砂の粒 + 長い影",
  "sand dunes at sunrise with long shadows, warm beige and terracotta, wide and empty",
  ["砂色の面","長い影","テラコッタ1色"],["ネオン","黒背景"],["ripple","none","letters-fall"],"DAY 01 / 42°C","旅・冒険 / 乾いた世界観の作品 / ミニマル寄りの商材",
  "DAY 01","何もない場所に、","行く。","出発する")
w("tea-garden","茶畑","和・自然・朝","nature",
  C("#f4f6ee","#e9eedc","#fff","#1f3322","#3f5240","#889a86","#d3dcc8","#2f6b3c","#8a5a2b"),
  ["Shippori Mincho B1","Zen Kaku Gothic New","Noto Sans JP"],"茶畑の畝の線 + 朝霧",
  "rows of a green tea plantation in morning mist, soft light, Japanese countryside",
  ["畝の線","深緑1色","朝霧のグラデ"],["ネオン","黒背景"],["ripple","tear","none"],"一番茶 / 朝五時","お茶・食 / 産地・農園 / 和の教室",
  "一番茶","朝五時の、","畑から。","茶を選ぶ")
w("hinoki","檜と湯","和・癒やし","nature",
  C("#f6efe4","#eee3d2","#fff","#3a2c20","#5e4b3b","#9a8672","#dccbb5","#b07a3c","#e8e2d6"),
  ["Zen Old Mincho","Noto Serif JP","Noto Sans JP"],"木目 + 湯気",
  "hinoki wood bath with rising steam and soft window light, Japanese onsen, calm",
  ["木目","湯気のグラデ","縦書きの小見出し"],["ネオン","ビビッド"],["ripple","none","tear"],"一 / 湯","温泉・宿 / 癒やし系 / 木の商材",
  "湯","力を抜く、","場所。","予約する")
# --- business +3 ---
w("startup-blue","スタートアップ","ビジネス・勢い","business",
  C("#fff","#f3f6ff","#fff","#0b1220","#334155","#7b8798","#dbe3f0","#2563eb","#0b1220"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし（面と太字）",
  "modern coworking office with large windows, bright daylight, clean, people blurred in motion",
  ["電気的な青1色","極太の見出し","数字のタイル"],["グレイン","セリフ"],["letters-fall","none","spotlight"],"01 / 02 / 03","SaaS・スタートアップ / 採用 / サービスLP",
  "01","速く、","正しく。","始める")
w("consult-charcoal","炭のコンサル","ビジネス・重厚","business",
  C("#1f2937","#111827","#273244","#f3f4f6","#c7cdd6","#8b93a1","rgba(243,244,246,.12)","#f59e0b","#f3f4f6"),
  ["Playfair Display","Noto Serif JP","Noto Sans JP"],"なし（面と細線）",
  "consultant's desk with a leather notebook and a fountain pen, dark charcoal tones, warm lamp",
  ["炭色の面","琥珀色1点","セリフの見出し"],["パステル","丸角"],["spotlight","none","letters-fall"],"Case 01","コンサル・士業 / BtoB / 高単価",
  "CASE 01","数字の裏に、","理由がある。","相談する")
w("eco-green","サステナ","ビジネス・環境","business",
  C("#fff","#f2f7f0","#fff","#1c2e22","#3e5245","#889a8e","#d6e2d8","#3a9a5b","#c9a97a"),
  ["Fraunces","Zen Kaku Gothic New","Noto Sans JP"],"クラフト + 葉",
  "a small plant growing from soil in a white pot, bright clean background, fresh green",
  ["葉の緑1色","クラフト色の小物","丸みのある見出し"],["ネオン","黒背景"],["ripple","none","stamp"],"Step 01","環境・食 / 社会貢献 / 自然派ブランド",
  "STEP 01","小さく、","続ける。","参加する")
# --- genre +2 ---
w("steampunk","スチームパンク","SF・真鍮・歯車","genre",
  C("#1a120c","#241912","#2e2118","#f1e4cf","#c4b39a","#87765f","rgba(241,228,207,.12)","#c8873a","#7aa3a8"),
  ["Libre Baskerville","Shippori Mincho B1","Special Elite"],"真鍮 + 歯車 + 蒸気",
  "steampunk brass airship above a Victorian city, gears and steam, copper and dark brown, painterly",
  ["歯車のモチーフ","真鍮色1つ","タイプライター文字"],["パステル","丸ゴシック"],["card-flip","stamp","letters-fall"],"Vol. Ⅰ / 蒸気圧","ゲーム・小説作品 / クラフト / 異世界系",
  "Vol. Ⅰ","歯車が、","回り出す。","乗船する")
w("kaiju","特撮","ジャンル・巨大・熱い","genre",
  C("#0a0a0a","#141414","#1c1c1c","#f2efe6","#c2bfb4","#807d74","rgba(242,239,230,.12)","#e5261d","#f2c13d"),
  ["Bebas Neue","Zen Kaku Gothic New","Noto Sans JP"],"フィルムの粒子 + 赤い空",
  "giant monster silhouette rising behind a city at dusk, red sky, film grain, tokusatsu movie still",
  ["赤い空","極太の見出し","警報の帯"],["パステル","丸角"],["lightning","letters-fall","flare"],"第1報 / 出現","特撮・映画作品 / イベント / 熱い告知",
  "第1報","街が、","揺れる。","警報を見る")
# --- minimal +2 ---
w("notebook-grid","方眼ノート","ミニマル・道具","minimal",
  C("#fff","#fafafa","#fff","#1a1a1a","#3a3a3a","#8a8a8a","#dfe3e8","#1a1a1a","#2b5cd6"),
  ["Inter","Noto Sans JP","Space Mono"],"方眼の薄い線",
  "a blank grid notebook with a blue pen, top view, white desk, soft light",
  ["方眼の線","青ペン1色","手書き風のメモ"],["グロー","黒背景"],["none","letters-fall","stamp"],"p.1 / □","ノート術・学習 / 講座 / 文具",
  "p.1","書いて、","考える。","はじめる")
w("pale-air","淡い空","ミニマル・軽い","minimal",
  C("#fbfdff","#f0f6fc","#fff","#1c2733","#4a5764","#8f9aa6","#dbe6f0","#1c2733","#7fb3e6"),
  ["Inter Tight","Noto Sans JP","Inter"],"なし（淡い青のグラデ）",
  "a single white balloon against a pale blue sky, minimal, airy, soft light",
  ["淡い青のグラデ","細い見出し","大余白"],["黒","ビビッド"],["ripple","none"],"01","軽やかなサービス / 子育て / 空気感の商材",
  "01","軽く、","はじめる。","見る")
# --- cool +3 ---
w("mode-black","モード","クール・雑誌・白黒","cool",
  C("#000","#0a0a0a","#111","#fff","#c8c8c8","#808080","rgba(255,255,255,.16)","#fff","#c8c8c8"),
  ["Playfair Display","Noto Serif JP","Inter"],"なし（写真1枚と文字）",
  "fashion editorial photograph, black and white, a model against a black backdrop, high contrast, magazine",
  ["写真1枚を大きく","細いセリフの巨大見出し","白黒のみ"],["色","丸角"],["letters-fall","spotlight","none"],"ISSUE 01 / FW","アパレル・美容 / モデル / 雑誌的ブランド",
  "ISSUE 01 — FW","黒は、","語らない。","コレクションを見る")
w("military","ミリタリー","クール・硬派・実用","cool",
  C("#3b4a2f","#334128","#44553a","#f0ecdc","#c8c4b0","#8f8c78","rgba(240,236,220,.14)","#f0ecdc","#d9a441"),
  ["Black Ops One","BIZ UDPGothic","Space Mono"],"ステンシル + 帆布の織り",
  "canvas military backpack on an olive green background, stencil lettering style, hard light",
  ["ステンシル風の英字","オリーブ1色","帆布の質感"],["パステル","セリフ"],["stamp","letters-fall","none"],"UNIT 01 / SPEC","アウトドア・ギア / 硬派なブランド / 男性向け",
  "UNIT 01","装備は、","少なく強く。","装備を見る")
w("glass-blue","ガラスと青","クール・テック・透明","cool",
  C("#070b16","#0c1224","#121a30","#eaf1ff","#b3c1e0","#6f7ea3","rgba(234,241,255,.14)","#38bdf8","#eaf1ff"),
  ["Inter Tight","Noto Sans JP","Space Mono"],"すりガラスの面 + 青い光",
  "frosted glass panels lit by cool blue light in a dark room, reflections, clean, futuristic",
  ["すりガラスの面（backdrop-blur）","青い光1つ","細い等幅ラベル"],["紙の質感","暖色"],["spotlight","neon-power","none"],"v1.0 / 01","アプリ・ツール / テック製品 / AI系",
  "v1.0","透けて、","見える。","試す")
# --- gira +2 ---
w("neon-sale","ネオンセール","ギラギラ・派手・夜","gira",
  C("#0a0510","#120a1c","#1a1026","#fff0fa","#e6b8dc","#9a7a95","rgba(255,240,250,.14)","#ff2d95","#ffe600"),
  ["Bangers","M PLUS 1p","Noto Sans JP"],"ネオン管の光 + レンガ",
  "hot pink and yellow neon tubes glowing on a black brick wall at night, vivid, loud",
  ["ネオンの光","ピンク×黄","太い英字"],["セリフ","紙の質感"],["neon-power","stamp","lightning"],"SALE / 24H","セール / ナイトイベント / 若年層向け商材",
  "24H ONLY","今夜だけ、","光る。","参加する")
w("platinum","プラチナ","ギラギラ・高級・銀","gira",
  C("#050506","#0c0c0e","#131316","#f7f7f9","#c9c9cf","#83838b","rgba(247,247,249,.14)","#e6e6ee","#b9b9c6"),
  ["Cinzel","Noto Serif JP","Noto Sans JP"],"銀の光の筋 + 黒ベルベット",
  "silver light streaks and sparkles on black velvet, luxurious, cinematic, cool tones",
  ["銀の光1つ","黒の面","細いセリフの大文字"],["パステル","丸ゴシック","宝石の象徴物"],["spotlight","letters-fall","card-flip"],"Ⅰ / MEMBER","会員制 / 高額商材 / 上位プラン",
  "MEMBER","選ばれた席が、","ひとつ。","申し込む")

# 2枚目（KV）: その世界観のLPの1画面目に置く被写体。用途に合わせる
KV = {'abyss-gold': 'a lone man in a black coat standing at the edge of a rooftop at night facing a vast dark ocean, a thin line of red light on the horizon',
 'paper-black': 'a woman photographer seen from behind holding a film camera by a window at dawn, quiet room',
 'wafu-dark': 'a samurai silhouette under a torii gate in fog, paper lanterns, falling embers',
 'neon-tokyo': 'a person in a hooded jacket walking through a rainy neon alley, umbrella reflecting cyan and magenta',
 'horror-west': 'an abandoned coastal lighthouse at night in heavy fog, a single window lit',
 'midnight-navy': 'a person reading a letter under a desk lamp in a dark navy room, a window full of stars',
 'charcoal-brass': "a craftsman's hands shaping leather on a dark workbench with brass tools", 'obsidian-mint': 'a sleek smartphone floating above black glass with a single mint light edge',
 'noir-film': 'a woman in a 1950s trench coat under a streetlight, venetian blind shadows',
 'cyber-grid': 'hands on a mechanical keyboard in a dark room lit only by a green terminal screen',
 'paper-white': 'a bright white studio with a single wooden chair and a tall window, morning light',
 'mono-minimal': 'a single black ceramic vase on a white table, hard shadow',
 'ivory-serif': 'a woman in an ivory silk dress seen from behind in a bright salon, champagne gold details',
 'linen-sage': 'a yoga mat on a linen floor next to a potted plant, morning daylight',
 'porcelain-blue': 'a white porcelain bowl with indigo pattern on a wooden table, north light',
 'gallery-white': 'a person standing alone in a white gallery looking at one large framed photograph',
 'morning-fog': 'a person walking alone on a foggy pale grey morning road',
 'swiss-grid': 'a bold red and black geometric poster pinned on a white wall',
 'letterpress': 'a stack of letterpress printed cards with a red wax seal on cream paper',
 'newspaper': 'a folded vintage newspaper on a cafe table with a cup of coffee, one red headline block',
 'brutal': 'a black megaphone on a bright yellow background',
 'pastel-pop': 'a cheerful young woman jumping with a notebook, pastel background',
 'pastel-pop-dark': 'a small clay character hugging a coin jar, pastel objects floating around',
 'candy-shop': 'glossy pink and cyan candies spilling out of a glass jar',
 'sakura': 'a girl in a white blouse under blooming cherry trees, petals falling',
 'kawaii-sticker': 'a cute cat character waving, thick outlines, die-cut white border',
 'macaron': 'a tower of pastel macarons on a marble table next to a small gift box',
 'picnic-gingham': 'a picnic basket, bread and lemonade on a red gingham cloth in sunlight',
 'pop-art': "a woman's face with a big speech bubble, halftone dots, comic style", 'cream-soda': 'a tall cream soda with a cherry on a retro cafe counter, window light',
 'retro-future': 'a rounded retro rocket flying over a desert city',
 'showa-kissa': 'a cup of coffee and a slice of pudding on a dark wood table, green velvet seat behind',
 'vapor-80s': 'a chrome statue bust between palm trees, pink sunset and neon grid horizon',
 'y2k-chrome': 'a chrome flip phone and silver headphones on a baby blue background',
 'pixel-8bit': 'a pixel art hero standing on a cliff facing a distant castle',
 'riso-poster': 'a risograph poster of a bicycle in fluorescent pink and blue',
 'vintage-map': 'a brass compass and a rolled antique map on a wooden ship deck',
 'film-camera': 'two friends walking on a summer road at golden hour, light leaks',
 'watercolor': 'a watercolor illustration of a small house with a garden and a bicycle',
 'sumi-ink': 'a sumi-e ink painting of a single crane standing in water',
 'indigo-aizome': 'indigo-dyed fabric hanging to dry in a wooden workshop, sunlight through the door',
 'forest-moss': 'a hiker standing in a mossy forest with light rays through the trees',
 'ocean-blue': 'a surfer walking on white sand toward clear blue water, wide shot',
 'autumn-kinmokusei': 'a cup of tea by a window with orange osmanthus branches, autumn light',
 'snow-country': 'a red-roofed hut in a wide snowy field, quiet winter light',
 'trust-navy': 'a confident consultant in a navy suit standing in a bright office',
 'fintech-emerald': 'a black credit card with a gold edge resting on emerald green stone',
 'blueprint': "an architect's hands drafting on blueprint paper with a steel ruler", 'data-dashboard': 'a large monitor showing glowing cyan charts in a dark office',
 'clinic-clean': 'a smiling doctor in a white coat in a bright clinic hallway'}
KV.update({'horror-jp': 'a dark abandoned school corridor with one flickering light and a small figure far at the end', 'horror-gothic': 'a candlelit gothic cathedral with a lone figure in a black dress', 'horror-vhs': 'night vision view of a dark forest path with a flashlight beam', 'sf-space': 'an astronaut floating in front of a vast ringed planet', 'sf-lab': 'a curved white corridor with a single red indicator light', 'sf-mecha': 'a giant mech being repaired in a hangar, tiny engineers below', 'game-rpg': 'a young adventurer with a sword looking at a distant castle at dusk', 'game-fps': 'a soldier silhouette walking through smoke with an orange flare behind', 'game-esports': 'a player at a glowing gaming desk on stage with purple and cyan lights', 'anime-kinetic': 'a determined young character in a school uniform against a bright blue sky, low angle', 'post-apoc': 'a lone figure with a backpack walking toward a rusted city in a dust storm'})
KV.update({'deep-ocean': 'a diver silhouette far below the surface with light rays coming down', 'volcanic': 'a lone figure standing on black volcanic rock facing a glowing lava river', 'storm': 'a person with an umbrella on an empty road under a lightning-lit storm sky', 'cinema-black': 'a man walking away down a rainy street at night, widescreen', 'minimal-black': 'a single white chair in a black room lit by one soft light', 'minimal-warm': 'a ceramic cup on a beige table by a window, soft light', 'minimal-type': 'a huge black letter printed on white paper, close up', 'concrete': 'a person standing in a concrete stairwell with hard light', 'carbon-red': 'a sports car in a dark studio with one red light streak', 'street-mono': 'a skater on a city street, black and white, with a neon yellow-green accent', 'gold-rush': 'golden light rays and floating gold particles over a dark city skyline', 'red-alert': 'a black megaphone and yellow burst shapes on a bright red background', 'money-green': 'stacks of gold coins on a dark green table under a spotlight', 'flash-yellow': 'a black lightning bolt shape on a bright yellow wall with hazard stripes', 'royal-purple': 'a golden key resting on purple velvet under a spotlight'})
KV.update({'aurora': 'a person standing in a snowy field watching green aurora curtains', 'eclipse': 'a crowd silhouette watching a total solar eclipse in a dark desert', 'botanical': 'an open vintage botanical book on a wooden table with a pressed fern', 'marble': "a woman's hand placing a gold ring on a white marble table", 'kraft': 'a bakery counter with loaves wrapped in kraft paper and black stamps', 'shojo-manga': 'a girl with sparkling eyes holding a letter, shojo manga style, pastel', 'yumekawa': 'a pastel unicorn plush on a cloud-shaped cushion, lavender room', 'showa-pop': 'a woman in a 1960s dress in a room with bold floral wallpaper, orange tones', 'art-deco': 'a couple in evening wear at an art deco hotel bar, gold and black', 'desert': 'a lone traveler walking across sand dunes at sunrise', 'tea-garden': 'a tea picker in a straw hat among green tea rows in morning mist', 'hinoki': 'a wooden hinoki bath with steam and a view of trees through a window', 'startup-blue': 'a young team at a bright office table with laptops, daylight', 'consult-charcoal': 'a consultant in a dark grey suit reviewing papers under a warm lamp', 'eco-green': 'hands holding a small plant seedling in soil, bright daylight', 'steampunk': 'a brass airship over a Victorian city with gears and steam', 'kaiju': 'a giant monster silhouette rising behind a city skyline at dusk, red sky', 'notebook-grid': 'a student writing in a grid notebook with a blue pen, top view', 'pale-air': 'a child holding a white balloon under a pale blue sky', 'mode-black': 'a fashion model in a black coat on a black backdrop, black and white', 'military': 'a hiker with a canvas backpack on a ridge, olive and sand tones', 'glass-blue': 'a person behind a frosted glass panel lit by blue light', 'neon-sale': 'a crowd under hot pink and yellow neon lights on a night street', 'platinum': 'a silver key on black velvet with light streaks'})
for _x in W: _x['kv'] = KV[_x['id']]
assert len(W) == 100, len(W)
assert set(KV) == {x['id'] for x in W}
