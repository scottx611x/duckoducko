# 🦆 DUCKODUCKO

A whimsical top-down hopper for mobile. One thumb, your duck, an endless river of nonsense.

---

## 1. The pitch

You are a duck riding a river that scrolls *toward* you (top → bottom of screen).
The river is full of stuff — lily pads, logs, sleepy turtles, picnic debris,
rubber duckies, the occasional bewildered frog. You **tap to hop**. Time your
hops to clear obstacles, bonk collectibles, and stay on the water.

The fantasy is **lightweight and silly**: it should feel like flipping through a
charming flipbook, not surviving a gauntlet. Difficulty is gentle and the death
screen should make you smile, not swear.

---

## 2. The core mechanic — "the hop" in a top-down world

This is the one tricky bit, so we pin it down precisely.

The camera looks straight down. A real jump has no vertical axis on screen, so we
**fake height with two tricks at once**:

1. **The duck scales up** (e.g. 1.0 → 1.35 → 1.0) over the arc of the hop — bigger = "closer to camera" = higher.
2. **A drop shadow stays on the ground and separates** from the duck. At rest the
   shadow sits under the duck; mid-hop the shadow shrinks and offsets slightly, so
   the eye reads real elevation. Shadow gap = altitude.

```
   rest            apex             landing
   🦆              🦆  (big)         🦆
   ▟  (shadow      ·                ▟
   under)          ▖ (small, gap)   (under again)
```

**Two inputs (confirmed):**
- **Steer (horizontal):** the duck slides left/right across the river. The *world* still scrolls top→bottom; the duck only moves on the X axis. Two control schemes to prototype and pick by feel:
  - *Drag/lane:* duck follows your thumb's X position (or snaps to lanes). Direct, great for precision.
  - *Tilt:* accelerometer steer. Hands-free-ish, very whimsical, but accessibility opt-out required.
  - **Default to drag-to-steer**; thumb X drives the duck, tap-to-hop layered on top (see below).
- **Hop (tap):** a tap (distinct from a drag) → the duck hops. Need a small drag-vs-tap threshold so steering doesn't accidentally fire hops. Hop has a fixed duration, e.g. **0.45s**.

**Hop rules**
- While airborne, the duck **ignores water-level obstacles** (logs, pads) — it's above them. It can still collect **airborne** items (floating feathers, bugs).
- On the ground, the duck collides with water-level obstacles → that's a fail/bonk. So you **either steer around an obstacle or hop over it** — that choice is the core skill.
- **No double-jump** in MVP. A short cooldown after landing (~0.1s) prevents mashing. (Power-up could add double-hop later.)

**Why both inputs:** steering alone is a dodge-em-up; hop alone is a rhythm game. Together
you get real moment-to-moment decisions — dodge the wide log, but *hop* the one you can't
get around in time. Per-duck stats (§5b) tune how each duck favors one or the other.

---

## 2b. The MEGA HOP (the big payoff)

The normal hop clears a single obstacle. The **Mega Hop** is the screenshot moment: the
duck launches *way* up — out of the water, above everything — soars for a few seconds,
and comes down with a splash that ripples the whole screen.

**How it reads (same two tricks, cranked):**
- Duck scales up huge (→ ~2.2x) and the **shadow shrinks to a tiny dot far below** — the gap sells real altitude.
- Camera does a subtle **zoom-out / pull-up** at apex so you briefly see more of the river ahead — a little "bird's-eye" reveal. Whimsy + actual utility (you spot upcoming obstacles).
- At the top: clouds drift, maybe a passing flock, the duck does a triumphant spread-wing pose. ~2–3s of pure joy.

**What it does (gameplay):**
- **Invincible while lofted** — sails over *all* water-level obstacles, no dodging needed. A panic button and a victory lap at once.
- Sweeps up every collectible in your X-path on the way (the "vacuum" arc).
- Big landing splash = a shockwave ripple that startles nearby wildlife (turtles retract, frogs scatter) for comedy.

**How you trigger it — two candidates (prototype both, §11):**
- **Meter-fill (leaning this):** a "LOFT" meter fills as you collect feathers / nail near-misses. Full meter → a glowing prompt; tap the meter (or double-tap) to cash it in. Reward for *playing well*, no extra button clutter.
- **Charge:** hold instead of tap → duck crouches, squashes, a little "boing" anticipation, release to launch. More skill/intent, but fights with drag-to-steer for the touch input — riskier on mobile.

**Per-duck flavor (ties to §5b):**
- **Wood Duck** lofts highest and floatiest (sparkle trail in the sky).
- **Bufflehead** lofts fast but low — quicker, snappier mega hops, fills meter faster.
- **Merganser** lofts slow and heavy, lands with the biggest splash/shockwave.

**Whimsy hooks:** ducklings (§WHIMSY §4) all launch with you in a little vertical conga;
the music swells; on landing the "well." deck gets a *positive* variant ("**WHEE.**").

## 3. The world & scrolling

- Vertical endless scroller. Background (water) scrolls top→bottom at a base speed that **slowly ramps** with distance.
- World is built from **tiled river segments** streamed in at the top and recycled at the bottom (object pooling — important on mobile).
- Distance traveled = score. Show it as **"meters paddled"** with a tiny duck-footprint trail in the UI.
- Parallax: 2–3 layers (deep water tint, surface ripples/sparkles, floating debris) moving at slightly different speeds for depth and whimsy.

---

## 4. Obstacles & collectibles

**Water-level obstacles (hop over these):**
- 🪵 Log — wide, telegraphs early.
- 🪷 Lily pad cluster — clear gaps to land between, or hop the whole patch.
- 🐢 Turtle — slowly drifts sideways, so timing shifts.
- 🦆 Rubber ducky — bonking it = small score penalty + a comedic squeak (your real duck is offended).

**Collectibles:**
- 🪶 Feather — common, +score, little sparkle.
- 🍞 Breadcrumb trail — lines that guide you into a good hop rhythm (also teaches timing).
- 🐛 Bug (airborne) — only grabbable *mid-hop*, rewards good timing.

**Hazards (post-MVP):** waterfalls (speed bursts), fishing lines, a heron that swoops.

---

## 5. Progression & difficulty

- **Gentle ramp:** scroll speed and obstacle density increase slowly with distance. No hard walls.
- **Themed stretches** every ~500m that swap the palette and props: Lazy Pond → Park Picnic → Spooky Bog → City Fountain → Aurora Lake. Pure visual variety = the whimsy engine.
- **One life, endless run, leaderboard by meters.** Quick restart (tap to retry) is essential for mobile feel.
- Soft meta-goal: collect feathers to unlock duck cosmetics (see whimsy).

---

## 5b. The duck roster (pick-a-duck)

You're a birder — so the ducks should be *real species* with personality and light
stats, not skins. Pick your duck before a run; unlock more with feathers. Stats are
small (±15%-ish) so it's flavor + playstyle, not pay-to-win. The "right" feel comes
from how each duck biases the **steer vs. hop** choice from §2.

| Duck | Vibe | Hop | Steer | Signature trait |
|---|---|---|---|---|
| **Mallard** | The everyduck. Starter. | ◐ | ◐ | Balanced. The tutorial duck. Iridescent green head glints on a clean run. |
| **Wood Duck** | The show-off | ◑ floaty | ◐ | Longer, prettier hop arc (extra hang time). Leaves a little sparkle trail because it knows it's gorgeous. |
| **Bufflehead** | Tiny & twitchy | ◑ quick | ◑ snappy | Small hitbox, fast everything, short low hops. The hard-mode / high-score duck. |
| **Northern Pintail** | The gymnast | ◐ | ◑ glide | Best steerer — wide, smooth horizontal drift. That long tail streams behind it. |
| **Common Merganser** | The bruiser | ◐ heavy | ◐ | One free bonk per run (shrugs it off with a *hmph*). The forgiving duck. |
| **Wigeon / Teal / Goldeneye…** | bonus roster | — | — | More species as unlocks; this is where your reference library pays off. |
| **Rubber Ducky** | the joke unlock | — | — | Squeaks instead of quacks. Doesn't swim well (drifts). Pure comedy, secretly endgame flex. |

- **Selection screen whimsy:** ducks line up like a little lineup photo; the selected one
  preens and looks at the camera. Field-guide styling — each has a tiny "range map" and a
  fake-fact blurb (half real birder trivia, half nonsense).
- **Birder authenticity is the hook:** real plumage, real silhouettes, real-ish behavior
  cues. A birder will *recognize* these and grin; everyone else just thinks the ducks are cute.
- Cosmetics (hats etc., §6 / WHIMSY) stack on *any* duck.

## 6. Whimsy (the soul — don't cut this)

This is where the game lives or dies. Ideas to draw from:

- **Duck personality:** idle animations — preening, a little head-bob, blinks, an occasional indignant *quack* if you don't tap for a while.
- **Hop squash & stretch:** exaggerate the anticipation/landing. Juicy > realistic.
- **Reactive world:** ripples radiate from every landing; lily pads bob; turtles retract when you land near them.
- **Cosmetics:** tiny hats (top hat, sombrero, traffic cone), sunglasses, a cape. Bought with feathers. This is the retention hook *and* the comedy.
- **Death is cute:** run over a log → duck just sits there looking grumpy with a "well." text. No gore, no harsh fail sound.
- **Companions (post-MVP):** a line of ducklings trails behind you and mirrors your hops a beat later — adorable and a scoring multiplier.
- **Audio whimsy:** kazoo/quack-forward SFX, a loopy ukulele/banjo track that speeds up subtly with the scroll.

---

## 7. Art direction — **pixel art**

Committed direction: **beautiful, modern pixel art.** Cozy and readable, not retro-for-retro's-sake.

**Technical foundation (already set in `project.godot`):**
- **Nearest-neighbor filtering** (`default_texture_filter=0`) + **pixel snap** — keeps pixels crisp, no blur.
- **Low base resolution, integer-scaled up.** Pick a base canvas (candidates: **180×320** chunky, or **270×480** more detail) and let Godot scale it to the device with integer scaling so pixels stay square. *Decide before drawing real assets* — it sets the size of every sprite. (Current prototype runs at 540×960 with placeholder shapes; we'll drop to the pixel base when art starts.)
- Animations as **sprite sheets** → `AnimatedSprite2D` / `SpriteFrames`. Hop = squash-anticipate → stretch-rise → land-squash (juicy, exaggerated).

**Style:**
- **Limited palette**, 4–6 colors per themed stretch — palette swaps are how themes feel different cheaply (and pixel art makes palette-swapping trivial: same sprites, recolored ramp).
- Soft dithering for water/shadows; chunky readable silhouettes for obstacles (gameplay clarity first).
- The duck: small but expressive, BIG eyes, a 2–3 frame idle. Shadow is a soft dark ellipse sprite that scales/offsets (the §2 altitude trick).
- Modern pixel-art touches that still feel handmade: subtle palette-cycled water shimmer, normal-light glints on a clean run, a gentle CRT-free bloom.

**Your edge:** you shoot birds for a living. Real plumage palettes and poses → reference
for pixelling each species in the §5b roster. A pixel mallard traced from your own photos
will read *right* to other birders. That authenticity is the hook.

**Asset pipeline options (decide when art starts):** Aseprite (the standard, ~$20, great
Godot workflow) for hand-pixelling; or commission a pixel artist per theme pack. Either
way the code/gameplay is fully decoupled from art — swap placeholder shapes for sprites,
nothing else changes.

---

## 8. Audio

- Music: one chill loopable track per theme, tempo nudges with speed.
- SFX: hop (boing-ish), land (soft splash + ripple), feather (sparkle), bonk (sad squeak), milestone chime every 100m.
- Keep it mixable to **off** — many people play muted. Game must read fully without sound.

---

## 9. Godot architecture (target: Godot 4.x, GL Compatibility renderer for mobile)

Scene tree sketch:

```
Main (Node2D)
├── World (Node2D)
│   ├── ParallaxBackground        # water layers
│   ├── SegmentSpawner (Node2D)   # streams + pools river segments
│   └── ObstacleLayer (Node2D)    # pooled obstacles/collectibles
├── Duck (CharacterBody2D or Area2D)
│   ├── Sprite2D (AnimatedSprite2D)  # idle/hop/land/bonk
│   ├── Shadow (Sprite2D)            # separate node, animated offset+scale
│   └── HopController (script)       # state machine: GROUNDED → AIR → LANDING
├── HUD (CanvasLayer)
│   ├── ScoreLabel ("meters paddled")
│   └── RetryPanel
└── GameManager (autoload/singleton)  # state, speed, score, themes
```

Key technical decisions:
- **Object pooling** for segments/obstacles — never `queue_free()` + `instantiate()` on the hot path; recycle nodes.
- **Hop = a state machine + tween**, not physics gravity. Tween the sprite scale and shadow offset over the hop duration; flip a `is_airborne` flag that disables water-level collision layers.
- **Collision layers/masks:** Duck-Ground, Duck-Air, separate masks so airborne ignores water obstacles automatically — no per-frame `if` checks.
- **Input:** single `InputEventScreenTouch` / mouse fallback → `hop()`. Dead simple.
- **GameManager singleton** owns scroll speed, distance, theme transitions; everything reads from it.
- One project, exports to **Android (.apk/.aab)** and **iOS (Xcode project)**. Test in-editor with the Remote debug → device, or `Godot Remote` app for fast iteration.

---

## 10. MVP scope (first playable)

Smallest thing that proves the fun:

- [ ] Duck centered, tap to hop (scale + shadow separation).
- [ ] Water scrolls top→bottom at constant speed.
- [ ] One obstacle type (log) spawned at intervals; hop to clear, collide = fail.
- [ ] Score = distance; retry on tap.
- [ ] One feather collectible.
- [ ] Placeholder art (colored shapes are fine) + one hop SFX.

If hopping over logs *feels good* with placeholder squares, the game works. Everything
after that is content and polish.

### Milestones
1. **M1 – Feel:** the hop mechanic + scroll + log, in-editor. (Is it fun?)
2. **M2 – Loop:** score, fail, retry, feathers, 2–3 obstacle types, pooling.
3. **M3 – Whimsy pass:** real duck art, squash/stretch, ripples, SFX/music, one themed stretch.
4. **M4 – Mobile:** touch tuning, Android export on a real device, performance pass.
5. **M5 – Meta:** cosmetics shop, themed stretches, leaderboard.

---

## 11. Decisions & open questions

**Decided:**
- ✅ Title: **DUCKODUCKO**
- ✅ Two inputs: **drag-to-steer + tap-to-hop** (§2)
- ✅ **Pick-a-duck** with a roster of real species + light stats (§5b)
- ✅ **MEGA HOP** loft mechanic (§2b)

**Still open:**
- Endless only, or also short hand-crafted levels?
- Mega Hop: charged (hold) or meter-fill (collect)? Leaning meter-fill — see §2b.
- Tilt-steer as an option, or drag only? (Drag is the MVP default.)

---

## 12. Parking lot (future directions — not in MVP)

Captured so we don't lose them. None of these are scoped yet.

**Power-ups** (the Mega Hop §2b is the first of a family):
- **MEGA HOP** — implemented. Invincible loft + bird's-eye reveal.
- **DUCK LASER** — a charged beam that obliterates a devastating hole straight through
  whatever's in its path (logs splinter, a clear lane opens downstream). Screen-shake,
  a big *pew*, debris. The aggressive counterpart to the Mega Hop's evasive payoff.
- Room for more: shield bubble, slow-mo "zen paddle," magnet (auto-collect), decoy duck.
- Likely all share the LOFT-style meter pattern (earn by playing well), with the player
  choosing/equipping which power-up a duck carries.

**Roguelike direction** (could be the actual game, not just endless):
- Structure a run as a sequence of **river segments / rooms**; between them you pick an
  **upgrade** (draft 1 of 3) — bigger hop, double-hop, wider magnet, extra free bonk
  (Merganser trait as a pickup), faster LOFT fill, duckling slots, etc.
- **Per-run meta**: choose your duck (§5b) as your "class"; species traits become starting
  builds (Bufflehead = glass cannon, Merganser = tanky).
- **Permadeath + escalating difficulty**, with a feather-bought meta-progression between
  runs (unlock ducks, upgrade pool, cosmetics).
- **Themed stretches (§5) become biomes**; the Heron (WHIMSY §7) becomes a recurring
  mini-boss / elite encounter. A boss heron at the end of a biome fits naturally.
- Open question to resolve later: pure endless arcade vs. roguelike run structure — they
  pull the design in different directions, so pick before building progression systems.

**Duck-select screen** (the roster §5b made real):
- Grid/carousel of ducks; unlocked ones full-color, locked ones **ghosted/silhouetted** with
  an unlock hint (feathers needed). Mallard **drake + hen** both done in pixel art now.
- Each duck shows its **stats** (hop / steer / signature trait bars from §5b).
- Selecting previews the duck idling + its quack.

**3D presentation (a real pivot — decide before committing):**
- Want to **pan/orbit the duck in 3D** on the select screen, and have hops become
  **flapping → tumbling → 3D-spiraling** combos. That means the duck is no longer a flat
  sprite. Two viable routes, both keep the pixel-art look:
  - **Sprite-stacking / voxel-style:** stack many pixel-art slices to fake a 3D model you
    can rotate (great retro look, lots of slice art per duck, heavy-ish).
  - **Low-poly 3D model with a pixel/posterize shader + nearest textures:** real 3D rotation
    and tumbling physics, pixel aesthetic via shader. More flexible for spiraling hops;
    means modeling/rigging each duck instead of spritesheets.
- This touches the whole rendering approach — worth a dedicated spike (one duck, one screen)
  to feel it before reworking the 2D prototype. Big fork in the road; flag it explicitly.
- Cheap middle-ground for hops *now* (no 3D engine): add **tumble/spin sprite sets** or
  rotate the existing sprite during a hop for a "barrel-roll" — gets some of the whimsy
  without the architecture change.
