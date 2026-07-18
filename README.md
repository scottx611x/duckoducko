# DUCKODUCKO 🦆

A whimsical top-down, tap-to-hop duck roguelike built in **Godot 4.6**. You are a duck.
The river goes forever. Steer, hop, snack, and try not to meet a log you weren't ready for.

**▶ PLAY IN BROWSER: https://duckoducko.scott-ouellette.com** (installable as a PWA)

- **Android APK** + web bundle attached to every release: https://github.com/scottx611x/duckoducko/releases
- Saves persist per device (`user://save.cfg` — IndexedDB on web).
- Design docs: `DESIGN.md` (mechanics) · `WHIMSY.md` (the whimsy bible) ·
  `FEEDBACK_TODO.md` (the living playtest tracker — every ask, every root cause, every verdict)

## The game

- **Controls:** drag anywhere to steer (relative — no lurch), tap to hop. **True multitouch:**
  hold a steering drag with one thumb and tap with any other finger to hop instantly.
  Fill the LOFT bar for a **MEGA HOP** (invincible 3D voxel tumble, camera pull-up) or the
  **DUCK LASER**. Desktop: Space = hop, M = mega, L = laser, P = pause.
- **A 19-duck roster** of real species (drake *and* hen variants, with real field marks a
  birder would vouch for) plus secrets you earn — fly Rusty's Thermals near-perfect and the
  red-tail hands over his wings; lose to Sadie enough times and the good girl joins you herself.
- **Six bosses** with living intros and per-boss arenas: GERALD (and GERALD THE ETERNAL),
  SNAPZ, BARRY, BONGO, and the alternate final — **SADIE THE BOUNDLESS**, who is not evil,
  she just wants to play. All duels share a learned visual language: one golden stomp tell,
  boss-tinted ribbons, no screen-covering text.
- **The river splits.** The Ancient Duck holds the current and deals you a choice of
  **wager contracts** — DANGER PAYS, THE FEAST, SCAVENGER'S RUN, THE QUIET WATER, blessings,
  trials, and the occasional SKY ROUTE clean over a boss. Since v1.21.53 every branch is a
  **place**, not a multiplier: THE NARROWS physically pinch the river in around you, THE
  SHALLOWS hatch bugs under a warm sun, THE STILLS drift mist and fireflies over a muffled
  hush. You glide under your chosen sign at reading speed; *then* the current takes you.
- **Roguelike bones:** mid-run power-up drafts (synergy-starred), shrine boons between runs,
  a junkyard economy (trash is ammo, armor, and snacks), ON FIRE streaks, FROG LEGS log-bounce
  chains, river events, RUSTY'S THERMALS slipstream trial, and an ascension ladder (endless
  bread-fueled NG+) once you best the Eternal.
- **The ponds are real.** The route runs Scott's actual waters — Buker, Woodbury, Purgatory,
  Sand (camp), Emerald, Lake Cochichewick, and Jimmy — each with its own shoreline canon,
  landmarks, music, and one very specific memory per pond. The cow is watching. Lizzie the
  beagle has never once flushed the bird you were photographing.
- **A full codex** (ducks, foes, friends, powers, boons, snacks, flotsam, THE SHORELINE),
  a wearable wardrobe with true voxel melds (hats survive the MEGA tumble as real 3D slices),
  a jukebox, Big Day daily-seeded runs with streaks, and a run logbook with pinch-zoom stats.

## 🤖 The bot-sim: the game playtests itself

The crown jewel of the dev tooling. `--botsim` runs a **headless AI duck** through real,
full-rules campaigns — same physics, same bosses, same drafts — and reports what killed it,
where, and why. It is how the game gets balanced without a human grinding hundreds of runs.

```bash
# 30-run batch, reproducible seed
godot --headless --path . -- --botsim --runs=30 --seed=11 --persona=skilled

# personas: skilled | cautious | reckless   (reaction sharpness × draft greed)
# drop straight into one boss:  --boss=0|1|2      ascension runs:  --asc=N
# force the thermals minigame:  --thermals
```

What the bot actually has:

- **A per-boss threat model** — it reads every boss's shared attack vocabulary
  (tele/down/skim/hop-warn/throw-warn) and dodges, hops, and stomps like a player would,
  including **predictive glob-landing avoidance** and Sadie's post-throw stomp windows.
- **Persona-weighted drafting** — it values shields and ducklings like a decent player,
  and greedy personas drift back toward "shiny = good."
- **Fork sense** — it picks split cards, rides branch waters, and flies the Thermals
  (cautious bots have flown 93–100% slipstream grades).
- **Receipts** — every run logs distance, duration, death cause *by specific attack*,
  bosses beaten, hits taken, and drafted powers; batches print death-cause and power-up
  tables and write `tools/botsim_dashboard/data/botsim_report.json`.
- **A Grafana dashboard** (`tools/botsim_dashboard/`, docker-compose + Infinity datasource)
  that turns report JSON into death-cause breakdowns, distance distributions, and
  which powers the AI actually drafts.
- **Save hygiene** — bot runs never touch the real save (learned the hard way).

Balance methodology: cold-start forced-boss batches against a known-good baseline
(GERALD THE ETERNAL is the "good fight" bar). New bosses ship when the bot's win rate
lands in the same band. The bot has **won the full 30,000 ft campaign** — first as a
pintail with zero hits taken — and every new mechanic (frog-legs chains, branch waters,
the split chooser) gets a bot batch before it ships.

## 🛠 Dev harness: screenshots or it didn't happen

Nearly every screen and set-piece has a one-shot verification mode that boots the game,
stages the moment, and saves a PNG to `/tmp` — the standing rule is *verify renders
before handing back*. Highlights (~40 total, see `Main.gd`):

```bash
godot --path . -- --shotsweep              # 9 key screens in ONE run (nightly eyeball)
godot --path . -- --rivershot --theme=3    # any pond's river dressing
godot --path . -- --branchshot --mod=heron # any branch water (THE NARROWS pinched, etc.)
godot --path . -- --forkshot --film        # 26-frame filmstrip of the whole split sequence
godot --path . -- --bossshot --kind=bongo  # any boss at his float pose
godot --path . -- --perfshot               # 300-frame avg frame ms + draw calls
godot --path . -- --bounceshot             # FROG LEGS end-to-end (prints the chain state)
```

The filmstrip harness has caught real bugs (a log once killed the duck mid-cinematic —
the death card said "rude."). In-game, **SHOW FPS** (settings) adds a perf pill
(fps · worst frame · jank count), a >80ms **hitch tracer**, and a 10s `[pace]` census to
the in-app logs — mobile perf reports arrive with numbers, not vibes.

## 🎨 Art & audio: one voxel model, every sprite

No hand-drawn frames. `tools/voxel_duck.py` owns a **3D voxel model per species**; every
2D view — idle, 7-step banking sweep, side profiles, wing-spread hops, hero portraits,
24-frame turntables — is *rendered from the model*, and the MEGA hop tumbles the model's
actual horizontal slices as a real sprite-stack. The same pipeline melds every wearable
onto every head (including Rusty's and Sadie's) so hats never float.

- `tools/gen_sprites.py` — non-duck world art (logs, herons, water, items)
- `tools/gen_env.py`, `gen_heroes.py` — river scenery + per-pond landmark set-pieces
- `tools/gen_sadie.py`, `gen_rusty_duck.py`, `gen_sadie_duck.py` — the exotic characters
- `tools/gen_sfx.py`, `gen_music.py` — every sound and theme, synthesized from stdlib
  (Sadie's bark is two synth syllables; her boss theme is the only duel music in a major key)

After regenerating art: `godot --headless --path . --import` (skipping this loads stale art).

## 🚢 Releases

```bash
PATH="/opt/homebrew/bin:$PATH" tools/release.sh v1.21.54
```

One command: stamps `GAME_VERSION`, exports the **Android APK** + **web build**, publishes
a GitHub release, and force-pushes the web bundle to `gh-pages` (custom domain, PWA
manifest + social meta injected by `tools/web_meta.py`). Cache-stale bugs are engineered
away: every deploy writes `version.txt` (the game pings it and shows an update banner) and
**versions the pck** (`index-v<ver>.pck` + `mainPack`) so a stale HTML can never load
mismatched game data. Web perf: canvas renders at half device resolution with integer
pixel-perfect upscaling — measured on-device, not guessed (see `FEEDBACK_TODO.md` for the saga).

## Run it locally

```bash
/Applications/Godot.app/Contents/MacOS/Godot --path ~/duck_game       # play
/Applications/Godot.app/Contents/MacOS/Godot -e --path ~/duck_game    # editor
```

The whole game is a single `Main.gd` + immediate-mode `_draw()` — one scene, no nodes to
get lost in, everything greppable.
