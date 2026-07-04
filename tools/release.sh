#!/bin/bash
# Build the Android APK + a web bundle, attach both to a GitHub release on the
# (now public) source repo scottx611x/duckoducko, and deploy the web build to
# GitHub Pages via the gh-pages branch (keeps main source-only; custom domain).
# Usage: tools/release.sh vX.Y.Z     (gh must be authed as scottx611x)
set -euo pipefail
cd "$(dirname "$0")/.."
TAG="${1:?usage: tools/release.sh vX.Y.Z}"
REPO="scottx611x/duckoducko"
mkdir -p build
# stamp the tag into the menu footer so the site always shows what it's running
sed -i '' "s/^const GAME_VERSION := \"[^\"]*\"/const GAME_VERSION := \"${TAG#v}\"/" Main.gd
godot --headless --path . --export-debug "Android" build/duckoducko.apk
godot --headless --path . --export-release "Web" docs/index.html
rm -f build/duckoducko-web.zip
(cd docs && zip -qr ../build/duckoducko-web.zip . -x ".nojekyll")
# GitHub release (APK + web zip)
gh release create "$TAG" build/duckoducko.apk build/duckoducko-web.zip \
    --repo "$REPO" --title "DUCKODUCKO $TAG" \
    --notes "🦆 PLAY IN BROWSER: https://duckoducko.scott-ouellette.com — Android: install the APK (allow 'unknown apps'). Web: unzip and serve with \`python3 -m http.server\`." \
    2>/dev/null \
    || gh release upload "$TAG" build/duckoducko.apk build/duckoducko-web.zip --clobber --repo "$REPO"
echo "release: https://github.com/$REPO/releases/tag/$TAG"
# --- deploy the web build to Pages (gh-pages branch, force-pushed; main stays source-only) ---
echo "deploying web build to Pages..."
WORK="$(mktemp -d)"
cp docs/index.* "$WORK/"
rm -f "$WORK"/*.import                                   # editor import metadata not needed to serve
touch "$WORK/.nojekyll"                                  # stop Jekyll from eating engine files
echo "duckoducko.scott-ouellette.com" > "$WORK/CNAME"    # keep the Pages custom domain
python3 tools/web_meta.py "$WORK"                        # social link-preview meta + installable PWA manifest
git -C "$WORK" init -q
git -C "$WORK" checkout -q -b gh-pages
git -C "$WORK" add -A
git -C "$WORK" -c user.name="scottx611x" -c user.email="scottx611x@gmail.com" commit -q -m "Deploy DUCKODUCKO web build ($TAG)"
git -C "$WORK" push -qf git@github.com:scottx611x/duckoducko.git gh-pages
rm -rf "$WORK"
echo "PLAY: https://duckoducko.scott-ouellette.com"
