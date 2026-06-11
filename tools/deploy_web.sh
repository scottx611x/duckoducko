#!/bin/bash
# Rebuild the web export and publish it to the public Pages repo
# (scottx611x/duckoducko-web). The game source repo stays private.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="$PWD"

godot --headless --path . --export-release "Web" docs/index.html

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
git clone -q --depth 1 https://github.com/scottx611x/duckoducko-web.git "$WORK"
cp -r "$SRC/docs/." "$WORK/"
cd "$WORK"
git add -A
if git diff --cached --quiet; then
    echo "no changes to deploy"
else
    git -c user.name=scottx611x -c user.email=scottx611x@gmail.com \
        commit -qm "web build $(date +%Y-%m-%d_%H%M)"
    git push -q origin main
fi
echo "live: https://scottx611x.github.io/duckoducko-web/"
