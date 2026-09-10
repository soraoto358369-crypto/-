// shot.js — Playwright で PC / SP のフルページスクショを撮る（ブラウザペインの代わり）
// 使い方: node shot.js <site_dir> [out_dir]
// 前提: npx playwright install chromium 済み。無ければ `npx -y playwright@1.47 install chromium`
// 出力: <out_dir>/pc.png (1280), sp.png (390), hero.png (1280x800 の 1 画面目)
const path = require("path");
const fs = require("fs");
(async () => {
  const site = path.resolve(process.argv[2] || ".");
  const out = path.resolve(process.argv[3] || site + "-src");
  fs.mkdirSync(out, { recursive: true });
  let chromium;
  try { ({ chromium } = require("playwright")); } catch { console.error("playwright がありません: npm i -D playwright && npx playwright install chromium"); process.exit(1); }
  const browser = await chromium.launch();
  const url = "file:///" + path.join(site, "index.html").replace(/\\/g, "/");
  for (const [name, w, h, full] of [["hero", 1280, 800, false], ["pc", 1280, 800, true], ["sp", 390, 844, true]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1, reducedMotion: full ? "reduce" : "no-preference" });
    await page.goto(url, { waitUntil: "networkidle" });
    await page.waitForTimeout(full ? 800 : 4000); // hero はイントロ完了後、full は静止状態
    if (full) { // 遅延表示を全部出す
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
      await page.waitForTimeout(600);
    }
    await page.screenshot({ path: path.join(out, name + ".png"), fullPage: full });
    console.log("saved", name);
    await page.close();
  }
  await browser.close();
})();
