# 🦆 The Whimsy Bible

The gameplay is "tap to hop." That's the skeleton. *This* is the meat. The rule for
everything below: **the player should want to show someone.**

Tags: `[cheap]` = doable with code + placeholder art, grab early. `[art]` = needs
real assets. `[later]` = post-MVP, parking it here so we don't forget.

---

## 1. The duck has FEELINGS

The duck is the whole game. It should feel alive even when nothing's happening.

- `[cheap]` **Impatience:** don't tap for ~4s and the duck looks back at you, taps a webbed foot, lets out a single judgmental *quack*. ~8s: it does a little stretch and yawns. The game is bored of you.
- `[cheap]` **Hop personality:** every ~10th hop is a "fancy" hop — a little spin, or a heel-click. Random, unannounced. Players will screenshot it.
- `[art]` **Blink + idle breathing.** Tiny chest bob, occasional double-blink. Costs almost nothing, sells "alive" completely.
- `[cheap]` **Near-miss reaction:** clear an obstacle by a hair and the duck does a relieved little shake mid-air, feathers ruffling. Reward style, not just success.
- `[later]` **Mood drift:** long clean run → duck visibly struts/grins. Lots of bonks → it sulks, shoulders down, smaller hops. Pure cosmetic, huge personality.

---

## 2. Death is a punchline, never a punishment

Failing should make you laugh and immediately retry.

- `[cheap]` **The "well."** Hit a log → duck stops, sits, a small text bubble: *"well."* / *"rude."* / *"that's a log."* / *"ok."* Rotate through a deck of one-word duck commentary.
- `[cheap]` **Rubber-ducky humiliation:** bonk a rubber ducky and your real duck stares at it, then at the camera, *then* fails. The pause is the joke.
- `[art]` **Comedy ragdoll-lite:** a single exaggerated bonk frame — googly eyes, splayed feet. No physics needed, one drawn pose does it.
- `[later]` **Death gallery:** the game quietly logs your funniest deaths (it screenshots the bonk frame). "Your Greatest Failures" menu. People love their own bloopers.

---

## 3. Cosmetics = the comedy engine AND the retention hook

Bought with feathers. Stack freely — that's where it gets stupid (good).

- `[art]` **Hats:** top hat, sombrero, traffic cone, tiny crown, party hat, a single slice of bread balanced on the head, a smaller duck.
- `[art]` **Eyewear:** sunglasses (duck refuses to acknowledge danger), monocle (fancy quacks), 3D glasses.
- `[art]` **Capes/accessories:** superhero cape that actually flutters in the scroll wind, a backpack, a fanny pack, a tiny scarf for the Spooky Bog.
- `[cheap]` **"Quack pack":** unlock different quack sounds — kazoo quack, air-horn quack, a duck that says "quack" in a tiny human voice, a goose honk (mislabeled, on purpose).
- `[later]` **Trail cosmetics:** hops leave sparkles / bubbles / tiny musical notes / a rainbow.

---

## 4. The ducklings (the heart-melter) `[later]`

A line of ducklings trails behind the duck and **mirrors your hop a half-beat later**,
like a little conga line of consequences.

- Each duckling you rescue (a collectible) adds to the line AND bumps your score multiplier.
- They peep in a rising chime when they hop in sequence — a clean run *sounds* like a little song.
- Bonk an obstacle and you lose the *tail* duckling, not the run — a softer, sadder, funnier failure state. It paddles after you for a second, then gives up. Devastating. Adorable.

---

## 5. The world is in on the joke

Reactive, living water. Most of this is `[cheap]` because it's code + tweens.

- `[cheap]` **Ripples everywhere:** every landing radiates a ripple ring. Obstacles bob. The whole surface is gently alive.
- `[cheap]` **Startled wildlife:** land near a turtle → it retracts with a *blip*. Land near a frog → it leaps away with a startled croak. Fish dart from your shadow.
- `[cheap]` **Floating nonsense:** non-interactive props drift by — a tiny sailboat, a message in a bottle, a duck-sized rubber raft with a sunbathing frog, a single rogue flip-flop.
- `[art]` **Background gags:** a cow on the far bank watching you. A picnicker who waves. A heron pretending it's a lawn ornament (until §7).

---

## 6. Themed stretches as comedy set-pieces `[art]`

Every ~500m the palette and props swap. Each theme gets ONE signature gag:

- **Lazy Pond** — baseline. Dragonflies, cattails, a snoozing turtle island.
- **Park Picnic** — breadcrumbs everywhere (it's raining bread), a dog that occasionally lunges from the bank, abandoned sandwiches as collectibles.
- **Spooky Bog** — fog, will-o'-wisps, the duck gets a tiny scarf, gravestones reading *"here lies a log."* SFX go reverby.
- **City Fountain** — coins instead of feathers, you're hopping between fountain tiers, a pigeon judges you, neon ripples.
- **Aurora Lake** — night, northern lights, bioluminescent ripples, every hop chimes a different note. The "pretty" payoff theme.

The transition itself is a gag: the water visibly changes color in a sweeping line that
washes down the screen, and the duck reacts ("ooh.").

---

## 7. The Heron (recurring nemesis) `[later]`

Every game needs a villain. Ours is a heron with theatrical menace.

- It appears on the bank in early themes doing *nothing*, very obviously pretending to be a statue.
- First real encounter: it telegraphs a swoop with a slow shadow growing across the water — you hop to dodge, and it misses and sulks.
- Beating a "heron gauntlet" stretch could be a milestone. It shakes a tiny fist as you escape. Running rivalry, zero dialogue needed.

---

## 8. Audio whimsy `[art/audio]`

- `[cheap]` **Hop = boing, land = soft splash + the ripple.** Two sounds carry 80% of the juice.
- `[art]` **Ukulele/banjo/kazoo loop** per theme; tempo nudges up subtly with scroll speed so tension is *felt*, not shown.
- `[cheap]` **Milestone chime** every 100m, pitch rising each step so progress sounds like climbing a scale.
- `[cheap]` **Clean-run music layer:** stack an extra instrument track in after N seconds without a bonk; lose it on bonk. The game gets musically richer the better you play.

---

## 9. Tiny delights (the salt) `[cheap]`

The throwaway stuff that makes it feel handmade:

- The score counter is "meters paddled," with a trail of little webbed footprints filling a bar.
- Pause menu: the duck just floats there, blinking, occasionally preening. Maybe it falls asleep if you pause too long.
- First launch: the duck waddles in from off-screen, settles, looks at you expectantly. No "PRESS START."
- Loading hints are duck "facts," half of them obviously fake. ("Ducks invented the kazoo.")
- The retry prompt isn't "GAME OVER" — it's the duck offering you a tiny "again?" with hopeful eyes.

---

## Grab-first shortlist (max whimsy / min effort)

If we want the prototype to feel magical with placeholder art, do these `[cheap]` wins:
1. Ripple ring on every landing.
2. Idle impatience quack + foot-tap.
3. "well." death deck.
4. Near-miss relief shake.
5. Rising-pitch milestone chime + clean-run music layer.

These five make colored squares feel like a *duck*.
