# Malben Trainee

A bilingual (Hebrew/English) training guide for new staff at Malben's three coffee shops in Givatayim. It covers drink tutorials (shared by all branches), a baking page, and per-branch details (hours, opening routine, and so on).

- **Source:** `malben-trainee.html`, a single self-contained page (HTML + CSS + JS, no build step).
- **Live page:** https://claude.ai/artifact/NqYYTLTZ8xkNiK4gMdktvr (private; the owner shares it from the page's Share menu). Publish changes with the Artifact tool using `malben-trainee.html` as the file path and that URL, so the link stays the same.
- **Brand:** green `#005357` (logo, headings, buttons), beige `#E3DABB` (background). Logo is `Malben_logo.svg`, inlined into the page header with `fill="currentColor"`.

## How the content is organised

All content lives in the data section at the top of the page's `<script>`, above the `APP` banner. Every visible text is `{ en: "...", he: "..." }`. `TODO(en, he)` marks text still to be filled in (shown highlighted in yellow).

- `UI`: interface labels.
- `DRINKS`: drink tutorials. `SHOT` and `STEAM` hold steps shared by several drinks.
- `OVEN`, `BAKING`: the Baking page and the bake table in the opening routine.
- `SEATING`, `CASHIER`, `OPENING_K50`: opening-routine phases. `SEATING` is shared by Katzenelson 50 and 135.
- `BRANCHES`: one entry per branch. Starts from `BRANCH_TEMPLATE()` and overrides what is known.

Keep the locker code and other access codes out of the page.

`app/`, `build_app.py`, `malben-app.zip` and `Install message for trainees.txt` are from an installable-app idea that was dropped. They are not used.

## Checks

Run from the project folder. Both must print `PASS`.

```sh
# 1. The page's script has no syntax errors
sed -n '/<script>/,/<\/script>/p' malben-trainee.html | sed '1d;$d' | node --check - && echo PASS

# 2. The page renders in Chrome (the script runs and draws the drink steps)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --user-data-dir="$(mktemp -d)" --virtual-time-budget=3000 --dump-dom "file://$PWD/malben-trainee.html" 2>/dev/null \
  | grep -q 'class="steps"' && echo PASS || echo FAIL
```

## Sharp edges

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
