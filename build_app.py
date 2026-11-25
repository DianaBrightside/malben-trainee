"""Build the installable Malben Trainee web app from malben-trainee.html.

Run:  python3 build_app.py
Then drag the "app" folder onto https://app.netlify.com/drop (or your site's Deploys page).
"""
import json, os, re, shutil, subprocess, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "malben-trainee.html")
LOGO = os.path.join(HERE, "Malben_logo.svg")
OUT = os.path.join(HERE, "app")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
GREEN, BEIGE = "#005357", "#E3DABB"

page = open(SRC, encoding="utf-8").read()
split = page.index('<header class="bar">')
head_part, body_part = page[:split], page[split:]
version = time.strftime("%Y%m%d%H%M%S")

index = f"""<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{BEIGE}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0d2224" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Malben">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="robots" content="noindex, nofollow">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; -webkit-text-size-adjust: 100%; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
{head_part.strip()}
</head>
<body>
{body_part.strip()}
<script>
if ("serviceWorker" in navigator) {{
  addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {{}}));
}}
</script>
</body>
</html>
"""

manifest = {
    "name": "Malben Trainee",
    "short_name": "Malben",
    "description": "מדריך למתלמדים / Trainee guide",
    "lang": "he",
    "dir": "rtl",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "background_color": BEIGE,
    "theme_color": BEIGE,
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}

# Offline: app files are cached on install; fonts are cached the first time they load.
sw = f"""const CACHE = "malben-{version}";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];
self.addEventListener("install", e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
}});
self.addEventListener("activate", e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
}});
self.addEventListener("fetch", e => {{
  const req = e.request;
  if (req.method !== "GET") return;
  // Pages: try the network first so updates show up, fall back to the saved copy offline.
  if (req.mode === "navigate") {{
    e.respondWith(fetch(req).then(r => {{ const copy = r.clone(); caches.open(CACHE).then(c => c.put("./", copy)); return r; }})
      .catch(() => caches.match("./")));
    return;
  }}
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {{
    if (r.ok || r.type === "opaque") {{ const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }}
    return r;
  }})));
}});
"""

netlify = """[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow"
[[headers]]
  for = "/sw.js"
  [headers.values]
    Cache-Control = "no-cache"
"""

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
for name, text in [("index.html", index), ("manifest.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2)),
                   ("sw.js", sw), ("netlify.toml", netlify), ("robots.txt", "User-agent: *\nDisallow: /\n")]:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)

# Icons: green wordmark on beige, drawn by headless Chrome.
logo = open(LOGO, encoding="utf-8").read()
def icon(size, width_ratio, out):
    html = f"""<html><body style="margin:0;width:{size}px;height:{size}px;background:{BEIGE};display:flex;align-items:center;justify-content:center">
    <div style="width:{int(size*width_ratio)}px">{logo.replace('<svg ', '<svg style="width:100%;height:auto;display:block" ', 1)}</div></body></html>"""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={size},{size}",
                    f"--screenshot={os.path.join(OUT, out)}", "file://" + f.name],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.unlink(f.name)

icon(512, 0.80, "icon-512.png")
icon(192, 0.80, "icon-192.png")
icon(180, 0.80, "apple-touch-icon.png")
icon(512, 0.62, "icon-maskable-512.png")  # smaller so Android's round crop doesn't cut the logo

print("Built", OUT)
for n in sorted(os.listdir(OUT)):
    print("  ", n, os.path.getsize(os.path.join(OUT, n)), "bytes")
