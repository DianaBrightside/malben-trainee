# Malben Trainee

A bilingual (Hebrew/English) training guide for new staff at Malben's three coffee shops in Givatayim. It covers drink tutorials (shared by all branches), a baking page, and per-branch details (hours, opening routine, and so on).

- **Source:** `malben-trainee.html`, a single self-contained page (HTML + CSS + JS). Edit only this file.
- **Public site:** https://dianabrightside.github.io/malben-trainee/ served by GitHub Pages from `docs/` on `main` of the public repo `DianaBrightside/malben-trainee`. Anyone with the link can open it, so nothing private goes in the page or the repo.
- **Build:** `python3 build_app.py` turns the source into `docs/` (a full web page plus manifest, icons and an offline service worker, so it can be added to a phone's home screen). It needs Google Chrome installed, which draws the icons. Commit `docs/` together with the source change, then push; the site updates in a minute or two.
- **claude.ai copy:** https://claude.ai/artifact/NqYYTLTZ8xkNiK4gMdktvr (private). Republish it with the Artifact tool using `malben-trainee.html` and that URL so the link stays the same.
- `Install message for trainees.txt`: ready-to-paste WhatsApp message with the link and home-screen install steps.
- **Brand:** green `#005357` (logo, headings, buttons), beige `#E3DABB` (background). Logo is `Malben_logo.svg`, inlined into the page header with `fill="currentColor"`.

## How the content is organised

All content lives in the data section at the top of the page's `<script>`, above the `APP` banner. Every visible text is `{ en: "...", he: "..." }`. `TODO(en, he)` marks text still to be filled in (shown highlighted in yellow).

- `UI`: interface labels.
- `DRINKS`: drink tutorials. `SHOT` and `STEAM` hold steps shared by several drinks.
- `HOW_MANY`, `BAKING`: the Baking page's top cards and the bake table (also shown in the Katzenelson 50 and 135 opening routines).
- `MACHINE`: the coffee machine's button guide, shown as the first entry ("מכונת הקפה") in the Drinks menu. It uses the same `panelHtml` as the ovens; a key can show several icons with `icons: [...]`.
- `OVENS`: one entry per branch oven for the Baking page's "Oven instructions" toggle: settings, a button guide (`PANEL` for Katzenelson 50's Unox, `PANEL_135` for Katzenelson 135's Tecnoeka) and optional how-to steps (`STEPS_135`). Button icons are in `I`.
- `COFFEE`, `SEATING`, `CASHIER`, `OPENING_K50`, `OPENING_K135`, `OPENING_WEIZMAN`: opening routines. `COFFEE`, `SEATING` and `CASHIER` are shared by all three branches. `OPENING_K135` is `OPENING_K50` with its own oven step. Weizman builds its versions from the shared ones and adds its own steps (and swaps `MUSIC` for "outside too").
- `CLOSING`: closing routine, shared by all three branches. Each branch gets it through `forBranch(CLOSING, "k50" | "k135" | "weizman")`: an item with `only: "<branch>"` shows only in that branch, and `add: { <branch>: {en, he} }` adds a point under an item for that branch.
- Routine items are written short: a bold label ending in a colon, then what to do (`<b>תנור:</b> ...`). Longer tasks split into `sub:` points; lists of things go in `groups:` chips.
- `note: true` items are tips or warnings shown in a box without a checkbox.
- Coffee machine steps follow the La Marzocco Linea Classic S (AV) manual: one cup / two cups / spiral buttons; cleaning cycle = spiral + one cup (display CLn); spiral + two cups = OFF. In the routines "ראש" means the portafilter (English: portafilter).
- Each routine item gets a checkbox (`renderPhases`). Ticks are kept in localStorage under `malben.ticks`, keyed by branch, routine, section and item position, and clear on a new day. Reordering items moves existing ticks, which is harmless since they reset daily.
- `BRANCHES`: one entry per branch. Starts from `BRANCH_TEMPLATE()` and overrides what is known.

Keep the locker code and other access codes out of the page.

## Checks

Run from the project folder, after committing. All must print `PASS`.

```sh
# 1. The page's script has no syntax errors
sed -n '/<script>/,/<\/script>/p' malben-trainee.html | sed '1d;$d' | node --check - && echo PASS

# 2. The page renders in Chrome (the script runs and fills the app area with the Drinks view)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --user-data-dir="$(mktemp -d)" --virtual-time-budget=3000 --dump-dom "file://$PWD/malben-trainee.html" 2>/dev/null \
  | grep -q '<main id="app"><div class="drinks">' && echo PASS || echo FAIL

# 3. docs/ is built from the current source (fails if the build changes anything not yet committed)
python3 build_app.py > /dev/null && { [ -z "$(git status --porcelain docs)" ] && echo PASS || echo "FAIL: docs/ out of date"; }
```

## Sharp edges

- **Pasted Hebrew arrives reversed.** Text copied from the user's source document comes in with each word's letters reversed and in odd order (e.g. `הנירטיו` for `ויטרינה`, `ח"ש` for `ש"ח`). Reverse each word and reorder it before using it, keep the meaning as written, and ask the user to check any word you're unsure of.
- **Checking rendered output: grep only for text the script produces.** The page source contains its own templates and CSS, so strings like `class="steps"` or `aria-current="true"` match even when the script fails to run. Look inside `<main id="app">` of the dumped DOM, for a string that only exists after rendering.

## How to work with me

- Commit and push yourself, right after each change that makes sense on its own. Don't wait for me and don't pile changes up. Never force-push.
- Fix the real cause, not the symptom. Figure out why something broke before changing anything. A retry, a try/catch, a special case or a loosened test that just makes the error go away isn't a fix. If the real cause can't be fixed now, tell me.
- Pick the simplest option that's still solid and easy to maintain. Simple never means fragile. Reuse what's already there before adding something new.
- If I correct you, stop and check you understood before carrying on. What I just said beats any plan.
- Don't tell me something works unless you actually ran it.
- Check with me before adding a new library or doing anything public or hard to undo.
- Keep answers short: what happened, plus anything surprising.
- If I need to do something, give me numbered steps.
- When I say "update this for future sessions", write it into the docs, not your memory.
- Keep docs about how things are now. Point at code by name, not line numbers.
