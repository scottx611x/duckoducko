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
    --notes "🦆 Android: install the APK (allow 'unknown apps'). Web: unzip and serve with \`python3 -m http.server\`." \
    2>/dev/null \
    || gh release upload "$TAG" build/duckoducko.apk build/duckoducko-web.zip \
        --clobber --repo scottx611x/duckoducko-web
echo "https://github.com/scottx611x/duckoducko-web/releases/tag/$TAG"
