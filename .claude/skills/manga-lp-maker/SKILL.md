---
name: manga-lp-maker
description: Create Japanese manga-style landing pages from user answers and proof assets. Use when the user wants a manga LP, story LP, vertical image-based LP, AI-generated comic landing page, FV manga design, manga sales page, PASBECONA manga scenario, Slippery Slide story structure, follower/fixed CTA footer, or an LP like zoroya Brain/tatekata examples. This skill guides strategy, scenario design, FV reference selection, illustration style selection, image prompt creation, proof sections, HTML assembly, QA, and packaging for Codex and Claude Code workflows.
---

# Manga LP Maker

Build a vertical Japanese manga landing page that reads like a story and converts like a sales page. Keep the user experience simple: the user answers questions, chooses or accepts an illustration style, and provides real proof assets. Do the strategy, scenario, prompts, assembly, QA, and packaging.

## Core Workflow

1. **Intake**: Ask only for missing essentials: business/service, target reader, pain, failed self-help, new option, desired future, proof assets, CTA destination, and preferred illustration style. If the user says "おまかせ", infer and state the assumption.
2. **Strategy Gate**: Before writing image prompts, read `references/scenario-strategy.md` and decide the reader stage, action barrier, proof burden, and story volume preset.
3. **Style Selection Gate (user-facing, before any image work)**: Read `references/style-menu.md` and present the style menu to the user in Japanese: every style as one line (number, name, one-phrase feel, what it fits), the sample sheet path `assets/reference/fv/_イラストテイスト見本_一覧_16種.png` so they can look at real examples, and a clear recommendation of 1-2 styles with a one-sentence reason based on the Sales Temperature Rule (direct-response paid offers → `cinematic-sales-anime`; reassurance-first businesses → soft styles). Then wait for the user's choice. Skip the question only when the user already named a style in their request; if they say 「おまかせ」, apply the Sales Temperature Rule, state which style was chosen and why in one sentence, and continue. Record the chosen style and the reason in `lp-design.md`, then copy that style's Touch Spec from `assets/reference/styles/<NN_stylename>/notes.md` into `lp-design.md`. Do not generate the FV candidate before this gate resolves.
4. **FV Direction**: Read `references/fv-quality.md` and choose 1-3 close reference FVs from `assets/reference/fv/` that match the confirmed style. If the confirmed style is a soft style (gentle-handdrawn, watercolor, pop-cute) on a direct-response paid offer, confirm the sales-punch trade-off with the user in one sentence before proceeding.
5. **FV Prototype Gate**: Generate a single publish-quality first-view candidate before full production whenever image generation is available. Save or place it as `_work/01-fv-candidate.*` or `src/01-fv.png`, show it to the user, and ask if the illustration image, character feel, copy density, and CTA direction are approved. When the user asks for a touch tweak (line weight, saturation, lighting, mood), record it as a `style-adjustments` line in `lp-design.md` using the style's adjustment knobs (`assets/reference/styles/<NN_stylename>/notes.md`) so it persists into every later prompt, then regenerate the FV. Do not generate the remaining LP images until the user approves the FV or requests a revision. If image generation is unavailable, provide the FV prompt and clearly mark the project as waiting for FV approval.
6. **Scenario Design**: Read `references/rhythm-and-slippery-slide.md`. Build a sequence where each block gives a natural reason to continue, not a forced cliffhanger. Use rhythm banners for visual breathing. Assign every image in the `lp-design.md` image list a height role (`band` / `panel` / `breath`) per the Vertical Rhythm rule: banners and chapter cards are landscape `band` images, and tall airy `breath` images are budgeted to 1-2 per LP with a stated reason. Before writing any image prompts, show the user a short scenario summary and the `lp-design.md` sequence for confirmation.
7. **Quality Reference**: For story-heavy Brain/Zoroya-style LPs, read `references/high-quality-zoroya-v3.md` and use `assets/reference/story/zoroya-v3/` as the bar for character consistency, panel rhythm, proof handoff, and browser QA.
8. **Proof Plan**: Read `references/proof-and-compliance.md`. Keep E proof and CTA real, not manga fiction. Use the Real Asset Intake Workflow below before final production.
9. **Prompts**: Produce copy-paste-ready prompts for the approved FV direction, character sheet, product mockup (for digital products), rhythm banners, manga blocks (with punch-line bands on key blocks), proof-support visuals, and CTA assets. Start every prompt with the style's Touch Spec plus all `style-adjustments` recorded in `lp-design.md`, and attach the style's anchor images from `assets/reference/styles/<NN_stylename>/` (when present) as generation references alongside the character sheet. Bake the Ad-Grade Sales Energy Requirements below into the prompts: typography treatment, palette/contrast register, and mockup reuse are prompt-level decisions, not post-processing. Require the character sheet as reference for recurring characters. For manga panels, explicitly forbid panel number badges, small numbered squares, sequence labels like `1/2/3/4`, and artificial page markers unless the user specifically requests numbering. Carry each image's height role into its prompt: `band` prompts must state the landscape aspect and "content fills the frame, no large empty margins"; only `breath` prompts may ask for designed negative space.
10. **Batch Image Production**: After FV approval, create or refine the character sheet from the approved FV direction, then generate the remaining manga/rhythm/offer images in one continuous production pass. Stop only for missing real proof assets, compliance risk, or obvious quality failure. Keep proof slots as real assets or clearly marked placeholders; do not fabricate proof.
11. **Assembly and Image Optimization Gate**: As soon as the ordered image set is available, use `scripts/assemble_manga_lp.py` to create `index.html`, then immediately run `scripts/optimize_lp_images.py --project <project> --max-width 1080 --quality 82`. The optimizer downscales oversized image LP assets, converts local image references to WebP, rewrites `index.html`, adds first-image priority plus lazy loading for later images, and archives originals under `_source_originals/`. Re-run this step whenever images are replaced.
12. **QA**: Run `scripts/audit_scenario.py` before image production and `scripts/audit_fv_quality.py` / browser checks after images exist. Once final images are in place (before optimization is fine), run `scripts/audit_dead_space.py --project <project>` and resolve every flagged image: crop the dead margin, regenerate as a `band`, or record it as an intended `breath` in `qa-report.md`. After optimization, run `scripts/audit_lp_assets.py --project <project> --require-webp --require-lazy` to catch missing, duplicate, unused, non-WebP, or non-lazy final images and YouTube embed hygiene. Then run the mandatory Per-Image Visual Gate Log below — scripts cannot see image content, so script PASS alone never means the Hard Quality Gates passed. Package with `scripts/package_manga_lp.py`.

## Per-Image Visual Gate Log (mandatory before packaging)

Automated scripts only check dimensions, references, and delivery format. Every Hard Quality Gate that concerns image *content* must be verified by actually viewing each final image (Read the image file in Claude Code, or open it in Codex). Record the result as a table in `qa-report.md` with one row per final image in `src/`:

| image | no panel numbers | characters consistent | Japanese text accurate | ad-grade typography/contrast | no unintended dead space | verdict |

The dead-space cell passes when the image has no large featureless area, when a flagged margin was cropped, or when the image is a budgeted `breath` whose reason is recorded in `lp-design.md`/`qa-report.md`.

The "Japanese text accurate" cell also fails when any speech balloon contains script notation instead of bare dialogue: a character name (アカリ等), 「」 quote brackets, or a `名前：` label inside the balloon is a hard fail — the balloon must show only the spoken words (2026-07-14 rule; see Prompt Hygiene in `references/style-menu.md`).

The "characters consistent" cell also fails on broken anatomy: every visible hand must have five fingers with natural joint directions (2026-07-15 rule; see Hand pose planning in `references/style-menu.md`). A broken hand means regenerate, not accept.

In-image media check (2026-07-15 rule, same column): any depicted screen, photo, paper, or poster fails when it contains readable/garbled text or UI rows, when its content ignores the surface's angle or bleeds past the frame/bezel, or when the LP's own characters are re-drawn inside it. Media content must be abstract color blocks and glow (see In-image media abstraction in `references/style-menu.md`).

- Any `fail` cell blocks packaging: regenerate that image, then re-log it.
- This step is how numbered panel badges, drifted faces, garbled text, and washed-out sales images get caught. A qa-report that claims PASS without this table is invalid.

## User-Facing Defaults

- Illustration style is the one design decision the user always gets: present the style menu at the Style Selection Gate (step 3) with a recommendation, and let them choose or say 「おまかせ」. Everything else (image count, panel layouts, palette details) is decided for them.
- Do not ask the user to decide exact image count. Choose a volume preset:
  - `light`: 12-16 images for quick tests or simple offers.
  - `standard`: 20-26 images. Default; closest to the Brain and Tatekata reference LPs.
  - `rich`: 28-36 images for high-ticket, comparison-heavy, or proof-heavy offers.
- Ask the user for real assets only when needed: representative photos, customer voice videos/reviews, ranking screenshots, before/after evidence, product screenshots, credentials, price/offer details, and CTA URL.
- If image generation tools are unavailable, still deliver the strategy, scenario, prompts, asset manifest, and HTML assembly instructions.
- If image generation tools are available and the user asks to create a manga LP, do not stop at documents/prompts. Generate the FV candidate first, get user approval on the visual direction, then continue with batch image production.

## Output Contract

Create or maintain a project folder with:

- `brief.md`: user answers, assumptions, proof assets needed.
- `lp-design.md`: strategy, volume preset, chosen style with Touch Spec and `style-adjustments`, story sequence, image list with a height role (`band`/`panel`/`breath`) per image and the reason for each `breath`.
- `prompts/`: copy-paste prompts for FV, character sheet, banners, manga blocks, proof, CTA.
- `src/`: final ordered LP images, optimized as WebP for delivery.
- `proof/`: real proof assets supplied by the user. Delivery copies may be WebP; originals should be preserved under `_source_originals/` after optimization.
- `index.html`: assembled LP with fixed footer CTA, first image prioritized, and below-the-fold images lazy loaded.
- `qa-report.md`: scenario, FV, legal/compliance, and HTML checks.
- `dist/`: packaged ZIP.
- `_work/01-fv-candidate.*`: optional FV approval draft when it should be kept separate from the final `src/01-fv.*`.
- `_source_originals/`: archived PNG/JPG/WebP originals created by the final optimization step; do not reference these files from `index.html`.

## Real Asset Intake Workflow

- After strategy but before final image generation, create a short `asset-request.md` or `brief.md` section listing only the real assets needed for this LP. Keep it easy for the user to answer by pasting local file paths or URLs.
- Ask for assets by purpose, not by vague file type. Example: "Brain ranking screenshot", "4 strongest review screenshots", "YouTube demo URL", "sample-site screenshots", "CTA URL", "current price/bonus screenshot".
- Accept local Windows paths, relative paths, image files, video URLs, web URLs, PDFs, DOCX, or screenshots. Copy supplied files into `proof/` with stable descriptive names and record original source paths in `brief.md` or `image_manifest.csv`.
- For videos, prefer a public or unlisted YouTube URL. Convert `youtu.be/<id>` or `youtube.com/watch?v=<id>` to `https://www.youtube.com/embed/<id>` in `index.html`. If the user supplies a local video file, place it under `proof/` and use an HTML video element only when that is clearly intended.
- Use manga panels to introduce proof emotionally, then show the real assets immediately after. Do not redraw rankings, testimonials, sample-site screenshots, profile photos, or videos as manga.
- Avoid stacking several generated "proof intro" manga images before the same proof group. Use one emotional bridge, then show the real asset immediately. If ranking, reviews, and video are all supplied, a strong default order is: proof bridge manga -> ranking screenshot -> review screenshots -> video bridge manga -> video embed.
- If a proof asset is missing, continue with scenario/prompts but mark the section as not publish-ready. Do not fabricate proof, review names, rankings, results, or customer quotes.
- Before delivery, verify that all requested proof assets appear in `proof/`, all referenced `src/` files exist, and the CTA/video URLs are correct.


## Ad-Grade Sales Energy Requirements

These requirements exist because a pastel, low-contrast LP with weak typography fails as a sales page even when the story is correct. The bar is `assets/reference/story/zoroya-v3/`, not a storyboard.

- **Headline typography**: main headlines inside final images must use ad-grade treatment: 袋文字 (outlined lettering), metallic/gold gradient or strong two-tone fill, drop shadow or glow, and a clear size jump over secondary text. Flat single-weight text on a light background is not final quality for FV, banners, punch lines, offer, or CTA images.
- **Contrast and palette**: the LP must have at least one deliberate high-contrast register (for example dark navy/night scenes with gold and red accents, as in zoroya-v3). An LP where every image sits in the same soft pastel range has no sales peaks; regenerate the FV, proof-turn, offer, and CTA images with stronger contrast.
- **Product mockup for digital products**: when the offer is a digital product (Brain material, course, template pack), create one 3D-feel product mockup (book/box/package render with the real title) early in production and reuse the same mockup in the FV, the offer section, and near the final CTA. This makes an intangible product feel ownable. Do not skip it, and do not redraw a different-looking package each time.
- **Punch-line band**: story manga blocks that carry a key message must end with a bold one-line conclusion band embedded at the bottom of the image (dark band, large outlined/gold text), e.g. 「見た目はそれなり。でも、何かが足りない。」. The band closes the block's emotion and slides the reader into the next block. Use it on the pain climax, the solution turn, the proof turn, and the fit/offer blocks; do not put a band on every image or it stops working.
- **Offer section anatomy**: the offer image(s) should combine: benefit/bonus cards (icon + short label + one support line), a price plate with strong numeric treatment, real purchase-context cues (e.g. a Brain product card mock with rating and button) and a final laurel/medal CTA band. A single soft illustration with a price written on it is below the bar.

## Image-Only Final Quality Requirements

- The final LP body must be composed from ordered image files in `src/`, matching the reference Brain/Tatekata-style LPs. HTML is only the delivery wrapper and fixed footer CTA; do not replace manga/LP images with HTML/CSS cards, wireframes, or simple vector/PIL placeholders.
- Use high-quality raster generation for final FV, banners, manga blocks, offer images, and CTA-support images. For Codex, prefer the built-in image generation path / ChatGPT Image 2.0 quality when available; otherwise deliver prompts and clearly mark the project as not final.
- Japanese text inside final LP images must be publication-grade and embedded in the final generated image. If Image 2.0 text is inaccurate, regenerate with shorter copy or split the block into another generated image; do not solve final LP text with PIL, HTML/CSS screenshots, rough overlays, or card-like mockups.
- Real proof assets such as Brain screenshots, ranking, reviews, sample-site screenshots, profile photos, and product screenshots must remain real screenshots/photos, not redrawn as manga.
- Never treat simple PIL drawings, rough wireframes, or low-detail generated drafts as final images. They are allowed only as internal storyboards under `_extracted/` or `draft/`.
- Final LP images must not be produced by PIL/HTML/CSS-style substitutes, browser screenshots of designed cards, or simple text overlays. Those may be used only for internal planning. The publishable LP body must be image-generation-first, with rich illustration/composition and sales copy integrated into each image.
- FV must pass the visual bar of the closest `assets/reference/fv/` examples before completion. If `audit_fv_quality.py` warns about low detail, dimensions, or review quality, revise and re-run instead of finishing.
- Do not proceed from FV to full image generation until the user has approved the FV's illustration direction, character feel, copy density, and CTA direction. This approval gate prevents producing 20+ images in the wrong style.
- Before final delivery, visually inspect desktop and mobile renderings and confirm that the LP reads as a polished image-based sales page, not a technical mockup.

## Final Image Optimization

- Do not package a finished image LP with full-size generator PNGs when WebP delivery is possible.
- Crop before optimizing: if `audit_dead_space.py` or visual review found a featureless top/bottom margin on an otherwise good image, crop it (Pillow) before running the optimizer, so the delivery WebP and the archived original stay in sync.
- Once all ordered images and real proof images are in place and `index.html` has been assembled, run `scripts/optimize_lp_images.py --project <project> --max-width 1080 --quality 82`. Do this at the image-complete stage, before browser QA and packaging; rerun it after any image replacement.
- Keep the display width in mind: the default LP wrapper is about 860 CSS pixels wide, so 1080 px source width is the normal delivery ceiling. If proof screenshots contain small Japanese text that becomes hard to read, rerun with `--max-width 1440 --quality 88` only for readability.
- The optimizer should convert every local `<img>` reference in `index.html` from PNG/JPG/WebP to delivery WebP, resize only images wider than the selected ceiling, add `loading="lazy"` to all local images after the first image, add `decoding="async"` to local images, prioritize the first image, and archive the original files under `_source_originals/` instead of leaving unused PNGs in final folders.
- Reopen the page after optimization. Confirm manga text, proof screenshots, and CTA sections still look sharp on desktop and mobile.
- Run `scripts/audit_lp_assets.py --project <project> --require-webp --require-lazy` after optimization. Do not package until it passes.
- Originals correspondence check (2026-07-13 rule): after optimization, verify every `_source_originals/src/<name>.*` is the same picture as its delivery `src/<name>.webp` (same aspect ratio, and a spot-check of content). Archiving a wrong or cross-project file as an "original" is a packaging hard fail — this actually happened (a gym dummy PNG was archived as a beauty clinic's 13-risk-honesty original).

## Hard Quality Gates

Do not finish, package, or call the LP final until these pass:

- **No panel numbering**: manga images must not contain panel-number badges, small boxed `1`, `2`, `3`, `4`, or visible reading-order labels unless the user explicitly requested numbering. If numbering appears, regenerate the image or replace it with an approved image; do not accept it as a final asset.
- **Natural manga reading order**: use vertical stacking, diagonal splits, large-to-small panel flow, balloon placement, and composition to make order clear without numbers. Slightly taller images are preferred over numbered grids.
- **One bridge per proof cluster**: do not create multiple generated intro images that say the same thing before proof. A proof cluster should read as `generated emotional bridge -> real asset(s)` without detours.
- **Real proof adjacency**: ranking screenshots, reviews, sample videos, product screenshots, and before/after assets must appear immediately after the manga block that introduces them. Do not insert unrelated generated sections between the promise and the proof.
- **Exact replacement semantics**: when the user says "replace A with B", update references to B at A's existing position. Do not add B as an extra section unless explicitly requested. Remove superseded images from `src/` and the ZIP.
- **No unused final images**: every final image file in `src/` must be referenced by `index.html`, and every image referenced from `src/` must exist. After optimization, final local image references should be WebP unless the user explicitly needs another format. Remove unused superseded images before packaging.
- **No fake proof slots in publishable output**: if a proof screenshot is missing, mark the LP as not publish-ready instead of drawing a manga substitute that looks like proof.
- **Sales energy present**: for direct-response paid offers, the FV, offer, and CTA images must show ad-grade typography (袋文字/metallic headline), a high-contrast register, the product mockup (digital products), and punch-line bands on key story blocks. A uniformly pastel, flat-typography LP fails this gate even if every scenario check passes.
- **Vertical rhythm (dead-space budget)**: banners, chapter cards, and proof bridges must be landscape `band` images whose content fills the frame; a one-line headline floating in a large featureless area is a fail. Tall airy images are allowed only as budgeted `breath` images (max 1-2 per LP, reason recorded). Every `audit_dead_space.py` flag must be resolved by crop, regeneration, or a recorded `breath` justification before packaging.
- **Per-image visual log completed**: `qa-report.md` must contain the per-image gate table with all rows passing. Script results alone never satisfy the image-content gates.

## Story Manga Character And Panel Requirements

- Standard and rich manga LPs must use fixed recurring characters, usually three roles: protagonist as the reader's mirror, side character as the close person who worries and nudges, and guide as the service/provider mentor who leads to the new option.
- **Character casting (2026-07-15 rule — anti same-face)**: before the character sheet, cast each character from the variable axes in `assets/reference/characters/character-axes.md` (性別・年代・体形・髪型・髪色・眼鏡・特徴・服装) — pick from the 24 archetypes in `assets/reference/characters/_INDEX.md` (catalog sheets A-D show them) or compose a new combination. Never default to the same-face archetype (30代・茶髪ショートボブ・平均体型の女性) unless the brief's target persona is exactly that. Main characters must differ from each other on at least 3 axes (hair style AND hair color always differ). Record every character's axis values in `lp-design.md` and reuse the same concrete words in the character-sheet prompt and every panel prompt.
- Create or define a character sheet before generating recurring manga blocks. It must show the protagonist, side character, and guide with stable appearance, clothing, role labels, and a few expressions. Use it as the reference for every recurring story image.
- **Industry casting shortcut**: `references/character-industry-menu.md` holds 50 industry presets for the 3-role cast (with recommended styles, matching the purchaser-bonus キャラクターカタログ's real sheet examples). Start casting from the matching row, then apply the character-axes re-cast rules above.
- Do not let the protagonist's face, age, hairstyle, clothing logic, or role drift between sections. If a generated panel makes a recurring character look like a different person, regenerate it instead of finishing.
- Use panel-based story manga beyond the opening pain section. Empathy, failed self-help, solution, proof transition, content explanation, fit/narrowing, offer, and final action sections should include 2-panel, 3-panel, 4-panel, or varied manga layouts when emotional movement is needed.
- Keep E proof real: rankings, testimonials, videos, product screenshots, and review screenshots are inserted as real assets. Manga panels may introduce proof emotionally, but must not redraw proof as fiction.
- Vary panel layouts across adjacent blocks: large single panel, 2-panel contrast, 3-panel vertical, 4-panel square, diagonal split, top-large/bottom-small, and speech-balloon-led scenes. Avoid three similar panel grids in a row.
- Prefer speech-balloon-led panel flow over visible numeric labels. If a generated layout needs numbers to be understood, redesign the layout instead of keeping the numbers.

## Implementation Notes

- Keep visible language simple enough for a junior-high reader.
- Use PASBECONA as a hidden strategy structure, not visible section labels.
- Use Slippery Slide as rhythm: every piece should make the next piece feel natural, but strong hooks should appear only 3-5 times in the whole LP.
- Insert rhythm banners between manga sections to prevent visual monotony.
- Use a real HTML footer CTA, not only a button drawn inside an image. Match the final CTA copy and URL.
- Optimize the assembled page for delivery: first visual image should load eagerly with high fetch priority; later local images should use lazy loading.
- For YouTube embeds, add `referrerpolicy="strict-origin-when-cross-origin"`, set a runtime `origin` parameter when served over HTTP(S), and provide a direct YouTube fallback for `file://` preview to avoid local embed error 153.
- For health, beauty, medical, finance, legal, education, or high-risk claims, flag proof requirements and avoid exaggeration.

## Codex And Claude Code

- Codex: use local scripts and browser verification when available.
- Claude Code: use the same files under `.claude/skills/manga-lp-maker`; optional eval workflows can use the user's existing `skill-creator/eval-viewer`.
- Claude Code image generation: Claude Code cannot generate images natively. Either use gpt-image-2 via an `OPENAI_API_KEY` in the project `.env` (write a small one-off generation script when needed), or delegate the image-generation steps to Codex CLI and continue assembly/QA in Claude Code. Output requirements (style, hygiene, QA gates) are identical on both paths.
- Keep both installations identical unless a platform-specific note is truly necessary.

