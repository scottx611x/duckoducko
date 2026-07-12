#!/usr/bin/env python3
"""Post-process the Godot web export for the public Pages site.

Godot regenerates index.html on every export, so the social link-preview meta
(Open Graph / Twitter) and the PWA bits are injected here instead of living in
the engine template. Idempotent — safe to run on an already-processed dir.

Usage: web_meta.py <docs_dir>
"""
import json
import os
import sys

URL = "https://duckoducko.scott-ouellette.com"
TITLE = "DUCKODUCKO \U0001F986"  # 🦆
DESC = "A whimsical tap-to-hop duck roguelike — play it right in your browser."
THEME = "#1f7a3d"
MARKER = "<!-- duckoducko-meta -->"

HEAD = f"""{MARKER}
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="{URL}/index.png">
<meta property="og:image:width" content="800">
<meta property="og:image:height" content="600">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{URL}/index.png">
<meta name="theme-color" content="{THEME}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="DUCKODUCKO">
<link rel="manifest" href="manifest.webmanifest">"""

MANIFEST = {
    "name": "DUCKODUCKO",
    "short_name": "DUCKODUCKO",
    "description": "A whimsical tap-to-hop duck roguelike.",
    "start_url": "./",
    "scope": "./",
    "display": "fullscreen",
    "orientation": "any",
    "background_color": "#000000",
    "theme_color": THEME,
    "icons": [
        {"src": "index.icon.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "index.apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
    ],
}


def main(docs):
    with open(os.path.join(docs, "manifest.webmanifest"), "w") as fh:
        json.dump(MANIFEST, fh, indent=2)

    index = os.path.join(docs, "index.html")
    with open(index, encoding="utf-8") as fh:
        html = fh.read()
    if MARKER in html:
        print("web_meta: already present")
        return
    html = html.replace("</head>", "\n" + HEAD + "\n</head>", 1)

    # VERSION THE PCK: a stale-cached index.html can never mismatch its pck again — each
    # release's html names its own pack file (Chrome's PWA cache bit us three times)
    vt = os.path.join(docs, "version.txt")
    pck = os.path.join(docs, "index.pck")
    if os.path.exists(vt) and os.path.exists(pck):
        ver = open(vt).read().strip()
        newpck = "index-v%s.pck" % ver
        os.rename(pck, os.path.join(docs, newpck))
        html = html.replace('"executable":"index"', '"executable":"index","mainPack":"%s"' % newpck)
        html = html.replace('"index.pck"', '"%s"' % newpck)
        print("web_meta: pck versioned -> %s" % newpck)

    with open(index, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("web_meta: injected social meta + PWA manifest")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs")
