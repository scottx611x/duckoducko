# DUCKODUCKO 🦆

A whimsical top-down tap-to-hop duck game. See `DESIGN.md` and `WHIMSY.md`.

## M1 prototype (this)

Placeholder shapes only — the goal is to feel whether **steer + hop** is fun before
any art exists. Art style (pixel art) is independent of this code.

### Run it
Godot 4.6 is already installed (via Homebrew, at `/Applications/Godot.app`). Two ways:

**A. Just play it (fastest)** — run the game directly from a terminal:
```
/Applications/Godot.app/Contents/MacOS/Godot --path ~/duck_game
```

**B. Open the editor** (to tinker, see the scene tree, tweak values):
```
/Applications/Godot.app/Contents/MacOS/Godot -e --path ~/duck_game
```
…or just open **Godot.app** from Applications and pick DUCKODUCKO from the project list.
Press **F5** to play, **F8** to stop.

> Validated headless on this machine: project imports clean and runs 120 frames with no
> script/runtime errors. I can't *see* or *play* the window myself, so the "is it fun?"
> verdict is yours.

### Regenerating the art & sound
- Sprites in `art/` come from `tools/gen_sprites.py` (needs Pillow), which drives the
  voxel pipeline in `tools/voxel_duck.py` — one voxel model per species generates every
  2D view **and** the mega-hop 3D slices. Five species: mallard, hen, wood duck,
  bufflehead, pintail.
- SFX in `sfx/` come from `tools/gen_sfx.py` (pure stdlib) — boings, splashes, the sad
  bonk squeak, milestone chimes, one judgmental quack.
- After regenerating either: `godot --headless --path . --import`

### Controls
- **Drag** left/right anywhere on screen → steer the duck across the river.
- **Tap** (a quick touch, no drag) → hop. While airborne you clear water-level logs.
- **MEGA HOP / LASER** buttons (bottom) light up when the LOFT meter fills (collect
  feathers, nail near-misses) → invincible loft with a bird's-eye pull-up, or a
  log-obliterating beam.
- Desktop testing: click-drag to steer, click to hop, **Space** = hop, **M** = mega,
  **L** = laser.

### Progression
- Feathers collected in a run bank to `user://save.cfg` along with your best distance.
- Spend feathers on the duck-select screen to unlock Wood Duck (25), Bufflehead (50),
  Pintail (90). Stats are real: hop/steer values bias lift, hang time, and steering.
- Every 500m the river washes into a new themed stretch (Lazy Pond → Park Picnic →
  Spooky Bog → City Fountain → Aurora Lake).

### Smoke test
`godot --headless --path . -- --smoke` runs the whole loop (menu → unlock → play →
theme change → mega → laser → death/save) and prints SMOKE lines; `-- --dbg` (windowed)
saves screenshots to `/tmp/s_*.png`. Note: both touch the real save file.

### The one question M1 answers
Is hopping over (and steering around) logs *fun* with placeholder squares? If yes, the
game works and everything after is content + art.
