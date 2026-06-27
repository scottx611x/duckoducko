#!/bin/bash
# Build the Android APK + a web bundle and attach both to a GitHub release on
# the public releases-only repo (scottx611x/duckoducko-web).
# Usage: tools/release.sh v0.10-beta     (gh must be authed as scottx611x)
set -euo pipefail
cd "$(dirname "$0")/.."
TAG="${1:?usage: tools/release.sh vX.Y-beta}"
mkdir -p build
godot --headless --path . --export-debug "Android" build/duckoducko.apk
godot --headless --path . --export-release "Web" docs/index.html
rm -f build/duckoducko-web.zip
(cd docs && zip -qr ../build/duckoducko-web.zip . -x ".nojekyll")
gh release create "$TAG" build/duckoducko.apk build/duckoducko-web.zip \
    --repo scottx611x/duckoducko-web --title "DUCKODUCKO $TAG" \
    --notes "🦆 PLAY IN BROWSER: https://duckoducko.scott-ouellette.com — Android: install the APK (allow 'unknown apps'). Web: unzip and serve with \`python3 -m http.server\`." \
    2>/dev/null \
    || gh release upload "$TAG" build/duckoducko.apk build/duckoducko-web.zip \
        --clobber --repo scottx611x/duckoducko-web
echo "https://github.com/scottx611x/duckoducko-web/releases/tag/$TAG"

# --- deploy the web build to the LIVE GitHub Pages site (scottx611x/duckoducko-web, main:/docs) ---
# Pages serves a static snapshot, so each release re-syncs docs/ into the repo and pushes.
echo "deploying web build to Pages..."
WORK="$(mktemp -d)"
gh repo clone scottx611x/duckoducko-web "$WORK/web" -- -q --depth 1
rm -rf "$WORK/web/docs"; mkdir -p "$WORK/web/docs"
cp docs/index.* "$WORK/web/docs/"
rm -f "$WORK/web/docs"/*.import          # editor import metadata isn't needed to serve
touch "$WORK/web/docs/.nojekyll"         # stop Jekyll from eating engine files
echo "duckoducko.scott-ouellette.com" > "$WORK/web/docs/CNAME"  # keep the Pages custom domain across releases
git -C "$WORK/web" add -A docs
if git -C "$WORK/web" diff --cached --quiet; then
    echo "Pages: no web changes to deploy"
else
    git -C "$WORK/web" -c user.name="scottx611x" -c user.email="scottx611x@gmail.com" \
        commit -q -m "Deploy DUCKODUCKO web build ($TAG) for GitHub Pages"
    git -C "$WORK/web" push -q origin HEAD:main
    echo "Pages updated -> https://duckoducko.scott-ouellette.com"
fi
rm -rf "$WORK"
echo "PLAY: https://duckoducko.scott-ouellette.com"
