## BEAVER BOSS (replaces pulled Pike, 2026-06-26)
- [x] v1.11.108-109 - FRONT-facing beaver (Scott-approved art) + its OWN lane-fitting fight: HURLS LOGS down telegraphed lanes (dodge/hop), TAIL-SLAP foam wave (hop it), LOG-WALL with a gap (weave), dips low to be STOMPED. Verified: renders front-facing, throws logs, no crashes. NEEDS PLAYTEST (feel/difficulty). TODO polish: beaver stomp lines (uses GERALD_STOMP_LINES now), codex entry, then add to boss_kinds pool.

## CLOUD = CINEMATIC SKIP (Scott chose, 2026-06-26)
- [x] v1.11.107 - fly-through mini-game CUT entirely (Scott: "so trash, easiest + least visually pleasing", + "catching the magic bread is an END-GAME thing" - bread goal was wrong). NOW a short NON-interactive GORGEOUS cinematic: golden-hour sky + sun/god-rays + 3-layer parallax clouds + soaring banking duck + feather trail -> swoop down past the boss -> +60 feathers. No controls, no bread, no difficulty to balance. NEEDS PLAYTEST (motion/feel).

## CLOUD MINI-GAME REWORK (Scott: "friggin horrible", 2026-06-26)
- [x] v1.11.105 REWORKED for clarity (Scott: no clear point/goal, bad controls, bad motion). NOW: visible golden-BREAD goal descends from the top; vertical progress bar (bread icon + climb marker); SNAPPY lerp steering (was sluggish move_toward 360); parallax cloud layers + banking duck; clear 'FLY UP TO THE BREAD / dodge storms - grab feathers' objective + 'FEATHERS xN' + 'CATCH IT!'; catch = BOSS SKIPPED + feathers. NEEDS PLAYTEST (controls feel = Scott's call).

# DUCKODUCKO — Feedback Tracker (exhaustive)

Every playtest ask I can reconstruct from the whole session, with honest status.
Skim it — if something's wrong or missing, tell me and I'll fix the entry + the code.
Status key: ✅ done+shipped · 🟡 shipped but UNVERIFIED in-game (you should eyeball) · ❗ OPEN (not done/partial) · ❓ unsure I did it right

## 🔁 PROCESS (so this stops happening)
1. Log each ask here BEFORE coding; SPLIT compound messages into one line each.
2. "Done" needs a checked box + version #. Never answer "finished?" with yes — read OPEN/VERIFY back.
3. 🟡 VERIFY ≠ ✅ DONE. Re-confirm in-game before promoting.
4. Re-read OPEN/VERIFY at every stopping point.

## ➕ PLAYTEST (Scott, 2026-06-22 eve)
- [x] **Snapz fight distinct + wacky** v1.11.9 — replaced the Gerald-like tail-sweep with a wacky PINBALL SHELL-SPIN (tucks in, careens around ricocheting off the banks, then flops down DIZZY = stomp window)
- [x] **Gerald banks/turns in-fight** v1.11.12 — sprite now leans toward the duck while floating + turns into attacks (uses his orientation, not one static view)
- [x] **Boss ULTIMATES** v1.11.26 — each boss has a signature once-per-fight ult (at half-HP, escalating): GERALD = FEATHER STORM (weave the drifting gap), SNAPZ = TIDAL SLAM (hop the foam walls).
- [x] **Crazy logs + DEADFALL(thwomp) disabled** v1.11.8 — "not fun", put ON ICE (conditions kept in comments to revive)
- [x] **Turtle shell BIGGER** v1.11.5 (~28% larger dome)
- [x] **Turtle/hat clipping FIXED** v1.11.5 (menu hero now draws body-first, hat on top)
- [x] **Lucien beak VISIBLE + gape w/ pink tongue** v1.11.10 (steel-ridged bill; gape frame, chin-up, periodic in the routine)
- [x] **DJ-DROP SFX** v1.11.10 — replaced the scratch with a punchy 808 sub-bass drop + kick on every Lucien tap
- [x] **Lucien head-turn** v1.11.10 — head-turn yaw frames woven into the routine for a subtle sway
- [x] **Thunder Feet boss damage** v1.11.13 — buffed + scales with stacks, with a THUNDER! popup
- [x] **Boss-clear heal** v1.11.13 — beating a boss patches you up (+1 shield)
- [x] **Junkyard HUD subtler** v1.11.11 — hoard meter shrunk + dimmed + moved below the buttons; RECYCLED/DUMPSTER banners → quiet float-text
- [x] **Boss rewards scale** v1.11.13 — was only returning 1 card on the first boss; now ALWAYS 3 (1 epic + 2 varied lesser on boss 1, scaling to legendaries by the Eternal)
- [x] **Gerald skim transition smooth** v1.11.12 — he now descends INTO the rake during the wind-up (no teleport)
- [x] **Gerald flies head-on** v1.11.12 — sprite rotates to face the rake direction (no crab-walk)
- [~] **Boombox** — wiring VERIFIED (plays music_boombox when worn, no boss/tutorial). Beat 'sick'-ness needs Scott's ear (can't judge audio)
- [x] **Spring-log ring softened** v1.11.6 (was a big pulsing cyan circle; now a faint rim — chevrons/warm-wood still mark it)
- [x] **Picker quip overlap FIXED** v1.11.6 (moved the quip bubble down over the duck's head)
- [x] **SADIE matched to her photos** v1.11.19 — rich dark-chocolate coat, her signature AMBER eyes, floppy ears, tan collar, happy tongue (Scott sent reference pics of the real girl)
- [x] **SADIE wardrobe mascot** v1.11.14 — friendly ball-less Sadie (lolling tongue + warm spotlight) greets you in the wardrobe with rotating barks; tap her for more. The wardrobe's its own place now.

## 🎮 AUTONOMOUS MANDATE (Scott handed me control 2026-06-22 — "do your best, don't resurface until done, have fun")
Work the OPEN list with my own judgment, then playtest: find bugs, theorize enhancements, design boon
synergies, add varied TRASH-leveraging power-ups (e.g. trash-magnet → free bonk). Ship as I go.

## ➕ JUNKYARD REWORK (Scott playtest, 2026-06-23)
- [x] **Trash unified** v1.11.22 — the river FLOTSAM itself is now the trash: scenery normally, but with a junkyard boon it magnets in + is collectable (collect rings, faster spawn). Killed the separate lane-trash. No more uncollectable-junk confusion.
- [x] **Both coexist** v1.11.21 — SCRAP SHELL reserves 3 orbiting pieces (defense); JUNK SLINGER only fires the EXCESS beyond those 3 (offense). No more starving each other.
- [x] **Trash ORBITS the duck** v1.11.21 — up to 3 collected pieces circle you with a protective ring; each one shatters to eat a hit.
- [x] **JUNK SLINGER fires the REAL trash** v1.11.20 — a pickup-order QUEUE; it chucks the actual pieces, and rarity scales the damage/blast (commons bonk, rares EXPLODE + AoE + boss chip)
- [x] **Trash visible** v1.11.20 — was 0.74 scale (way smaller than scenery props); bumped to 1.7
- [x] **Trash bobs / snacks hover** v1.11.20 — trash bobs IN the river, snacks float ABOVE with a cast shadow
- [x] **HUD ring** v1.11.20 — killed the bin meter; the hoard now reads as a subtle green second ring around the minimap duck
- [~] **Balance** v1.11.20 — slower fire (1.05/junker), consumes the queue, rare trash is scarce. Watch for OP — easy to tune.

- [x] **Fetch BEAUTY pass** v1.11.36 — built a full-body RUNNING Sadie voxel (legs, 2-frame gallop gait, floppy ears, lolling tongue, wagging tail plume); she now runs on real legs during the chase/return (gait alternates), squashes on the pounce, kicks up dust, and the chuckit SPINS as it flies. Flip handled cleanly via the side-profile sprite.
- [x] **Sadie FETCHES on tap** v1.11.35 — tap her and she throws the chuckit, bounds after it (running bob), pounces ("GOT IT!"), trots back (flipped, ball in mouth) + drops it, tail going wild. A full fetch loop.
- [x] **Sadie keeps her CHUCKIT** v1.11.34 — her orange+blue Chuckit ball sits at her feet in the wardrobe (she ditched it from her MOUTH to greet, but it is right there); bark lines reference it ("throw it after?")

## ➕ PLAYTEST (Scott, 2026-06-23 #2)
- [x] **Sadie fixed** v1.11.29 + v1.11.33 — on the MAIN shop WARDROBE button (facing right, like Lucien); v1.11.29 wrongly DELETED her from the wardrobe + killed her barks. v1.11.33 RESTORED her as a tappable, barking shopkeeper in the wardrobe (facing right, clear of the now-compacted grid). She is now in BOTH places + keeps her personality.
- [x] **DUCK SLOTS slot machine** v1.11.30 — the mystery egg is now a 3-reel slot: spin for a chance; a 3-DUCK jackpot (~12%) unlocks a duck, other combos pay feathers, most spins miss. Unlocking the roster is a real gamble now.

- [x] **Sadie plays REAL FETCH** v1.11.39 — FOUND the bug: leftover white (240,240,246) 'life-glint' voxels at (+/-2,6,9) on her ball-free face (my earlier removals never matched) = the startled eyes. Killed them, gave her warm AMBER irises. Now the in-place fetch works: idle she bobs/glances (Lucien-style pose cycle); tap her (or every ~8s on her own) and she DROPS her voxel chuckit, play-bows, POUNCES on it (lunge+squash), and pops back up with it in her mouth. Cute, not a cat, not scary.
- [x] ~~Sadie ANIMATED v1.11.38~~ superseded by v1.11.39 — was a frozen sprite; now a 4-pose set (idle/head-bob/glance-L/glance-R) cycled via a SADIE_SET routine + a gentle bounce, and a fast excited bob+bounce when tapped. She's alive now. NOTE: literal ball drop/retrieve fetch is NOT in — the ball-free face kept rendering with bad startled eyes; deferred. She stays ball-in-mouth.

- [x] **Sadie has LEGS** v1.11.40 — the swimming model was just head/shoulders (floating on land). Added a sitting-lab lower body (front legs + paws + haunches) via a legs= flag, regenerated all her pose sprites. She is a proper sitting dog now.
- [x] **Sadie speech bubble over her face** v1.11.40 — lifted it well above her head (was overlapping her face, worse now that she is taller with legs).

- [x] **Duck-name field removed from select** v1.11.47 — it is a MAIN-MENU thing (lives below "tap to play"); was crammed between the WILD CARD/WARDROBE buttons + ASCENSION bar in select. Now hidden on select, shown only on the menu.

- [x] **Sadie: huge feet + real fetch + better run** v1.11.48 — (1) trimmed her clown paws. (2) Rebuilt the run as a proper 4-FRAME GALLOP (gather/push/flight/land) with thick legs, sturdy body, eager head, lolling tongue, rocking bounce — a happy lab, NOT a cat. (3) The fetch now has REAL DISTANCE: she flings the chuckit ~300px across, GALLOPS after it (4-frame cycle), grabs it, gallops back (flipped, ball in mouth), settles home.

## ➕ SELECT DUCK BELLY-UP (Scott, 2026-06-24)
- [x] **Duck-select duck rendered belly-up/awkward** v1.11.46 — the turntable idle-spun through ALL 360deg (incl. the flat swimming model's belly-up back views) + randomized angle on duck-switch, so it parked at fucked angles. Now: drag to spin freely, but it EASES back to a flattering front-3/4 when idle; duck-switch starts facing front too.

## ➕ SNAPZ TORRENT v2 (Scott playtest: boring/easy + ugly droplets)
- [~] **TORRENT reworked** v1.11.98 NEEDS PLAYTEST — was lane-gap bolts (sit in the gap = trivial). Now: FAST bolts AIMED at the duck (lead-less, with a spread fan), rapid 0.45s cadence, 5-6 volleys, 2 bolts (3 in phase2) -> you must KEEP MOVING, can't camp. Speed 400, from up high (stays back). Tune speed/cadence/count if too hard/easy.
- [x] **water bolt VISUAL** v1.11.98 — the flat droplets looked bad; now a glossy blue orb (3 concentric + highlight) with a tapered MOTION TAIL behind its velocity = a streaking water jet. Verified via capture.

## ➕ POLISH + BIG FEATURE (Scott playtest, 2026-06-26)
- [x] butterflies REMOVED v1.11.99 (Park Picnic atmosphere, too distracting)
- [x] water reflection ovals REMOVED v1.11.99 (the per-biome caustic light-pools; kept the colour WASH so ponds still differ). Fireflies KEPT.
- [~] select duck rotation v1.11.99 NEEDS PLAYTEST - was narrow one-sided sway (0.32+sin*0.4); widened to symmetric sin*0.7. Confirm it is the "rotating nicely" Scott meant.
- [x] POSITIVE: boss fights much better now (Scott).
- [x] **CLOUD-LAUNCH skip-a-boss mini-game COMPLETE** (v1.11.100-103) NEEDS PLAYTEST — rare cloud geyser spawns (~once per 2-4min, only when a boss is ahead) -> ride it -> LAUNCH into the sky -> FLY-THROUGH mini-game (weave dark storm-clouds, grab gold feathers, ~7s, loot HUD + timer) -> smooth dive LANDING past the skipped boss with a '+N feathers' payout. Built over 4 loop cycles. Scott to playtest the full sequence + the spawn rarity/feel.

## ➕ SNAPZ MAW-FACING (Scott, 2026-06-25) — terminal lunge/stuck always faced right
- [x] **stompable Snapz now FACES the strike lane** v1.11.96 — root: the snap/stuck pose used a FIXED frontal sprite (tex_snapz[2]); the open-maw turntable (snapz_open_spin_00-15) existed as art but was NEVER LOADED. Fixed: load tex_snapz_open + draw uses it for snap/stuck, indexed by yaw; widened the lane->yaw map (x3.4, clamp 1.6) so lanes hit frames ~12(maw-left)/0(down)/4(maw-right). VERIFIED via capture: left lane -> faces LEFT, right -> faces RIGHT. (Debug pain: the loader/draw edits got clobbered by temp-capture file writes a couple times.)

## ➕ SNAPZ PLAYTEST #2 (Scott, 2026-06-25) — played v1.11.94
- [~] **NEW: stay-back ranged attack (TORRENT)** v1.11.95 NEEDS PLAYTEST — Scott wanted Snapz to sometimes STAY BACK + shoot, distinct from Gerald orbs, random per encounter. Added torrentwarn->torrent: he rears HIGH (y=168, not lunging) + spits WATER BOLTS (distinct cool-blue jets, NOT green muck) down 2 of 3 lanes leaving a GAP each volley (slide into the gap); 3-4 volleys (scales w/ idx). Random pick in LURK like Gerald (~28%% p1 / 40%% p2). Also tagged the between-chomp spit as water for consistency.
- [x] **never-repeat chomp lane** v1.11.95 — the v1.11.94 edit silently failed (text mismatch); now consecutive chomps avoid the previous lane so they visibly move L/C/R.
- [ ] **MAW FACING (Scott)** — the BITE uses a FIXED frontal sprite (tex_snapz[2]); never faces down/left to match the lane. There IS an unused open-maw turntable (snapz_open_spin_00-15). NEXT: use it during snap/warn, indexed so the open maw points AT the strike lane. Await go-ahead.
- [ ] still open from #1: ultimate = announced frenzy or distinct mechanic? loom-toward-you during wind-up?

## ➕ SNAPZ PLAYTEST #1 (Scott, 2026-06-25) — he played v1.11.92
- [x] **Boss music too loud / ignored settings volume** v1.11.94 — REAL BUG: boss_player.volume_db was hardcoded to -3.0 (~14dB hotter than the river) in BOTH the play-start (5424) and the live settings handler _apply_music_vol (8279). Both now = _music_vol_eff() (same as the river, honours the toggle/mute).
- [~] **Snapz HP felt high** v1.11.94 NEEDS RE-PLAYTEST — boss HP 4+2*idx -> 3+2*idx (Snapz 6->5, Gerald-Immense 4->3, Eternal 8->7 @asc0). Also helps the bot-sim Gerald-wall finding.
- [~] **Chomps only hit the RIGHT side / not varied** v1.11.94 NEEDS RE-PLAYTEST — duck-lane bias 3x->2x + never repeat the previous lane, so consecutive chomps visibly move L/C/R instead of camping his side. (Root: 60% bias tracked the player to one side.)
- [~] **Ultimate not seen** v1.11.94 NEEDS RE-PLAYTEST — only fires at half-HP (now reachable faster w/ lower HP); made it bigger + unmistakable: 4-chomp swept FRENZY, screen FLASH "FEEDING FRENZY!", a jolt. OPEN Q for Scott: is an announced chomp-frenzy the ultimate he wants, or a DISTINCT new mechanic (whirlpool/geyser)?
- [ ] "feel like he is coming to get ya" — partially (2x bias still leans at you); may need the boss to LOOM/approach more visibly. Await re-playtest.

## ➕ BOT-SIM HARNESS (self-playtest, 2026-06-25)
- [x] **scootybooty bot-sim v1** — `godot --headless --path . -- --botsim --runs=N --persona=skilled|cautious|reckless`. An AI duck drives target_x + hop() via a danger-field heuristic (herons/boss-telegraph/globs/logs/tides/Sadie/haz_turtle), auto-resolves shrine+draft picks, records per-run metrics (dist, dur, death CAUSE via die() cat, bosses, hits, feathers/trash/snacks), prints an aggregate + writes user://botsim_report.json. Stall guard flags infinite runs. Inert in normal play (flag-gated; NOT released as a version).
- FINDINGS v1: skilled bot reaches Gerald (boss 1) ~5000m but DIES to him (also early donny/sadie deaths before threat model expanded). Does not yet WIN bosses.
- [x] **--boss=N + boss-combat AI** — bot can be dropped straight into a chosen boss + now chases/stomps vulnerable bosses. FINDING: dropped into the NEW Snapz, the skilled bot beats it 6/6 taking ~1 hit -> the 3-lane chomps are DODGEABLE/FAIR (objective half of the Snapz playtest validated). FINDING: Donny is a 100%% death wall after (bot lacks Donny-awareness OR he is overtuned).
- [x] **power-up metrics + Grafana sidecar** — report now captures drafted power-ups (picked dict) + boons; restructured into flat Grafana-friendly arrays (summary/deaths/ups/runs) written to tools/botsim_dashboard/data/. Built tools/botsim_dashboard/ (docker compose: Grafana-oss + Infinity datasource + nginx fileserver, auto-provisioned datasource+dashboard). VERIFIED end-to-end on localhost:3001 (3000 was taken). Panels: KPIs, death causes, power-up frequency, per-run table.
- [ ] NEXT: add Donny (+ remaining char hazards) to the bot threat model so it reaches Snapz/Eternal via real progression; bigger persona batches; per-attack dodge-margin metrics; improve boss-combat AI (reliable bait->dodge->stomp) so the bot clears Gerald + reaches SNAPZ/Eternal — needed to actually validate the Snapz chomp redesign without Scott. Then per-attack dodge-margin metrics + bigger persona batches.

## ➕ BOSS REWORK (Scott, 2026-06-25) — IN PROGRESS (loop)
- [x] **Stomp over-advertising -> subtle** v1.11.91 — the vulnerable-boss "HIT ME" glow was a big pulsing gold billboard; cut to a faint warm hint (both the Gerald `dazed` + Snapz `stuck` glows), slower pulse, gentler brighten. Cross-board.
- [~] **SNAPZ redesign cycle 1 (spin OUT, 3-lane chomps IN)** v1.11.92 — NEEDS PLAYTEST. Ripped out spinwarn/spin/cyclonewarn/cyclone entirely (state cases + draw vortex + danger-ring all removed). LURK now always -> CHOMP: picks 1 of 3 lanes (left/center/right) BIASED to the duck's current lane (3x weight) so most chomps force a read+dodge; never repeats a lane in a combo. Ultimate (FEEDING FRENZY) = a rapid 3-lane chomp combo (chains 3 chomps in different lanes). Added a chomp LANE telegraph (red ring at the strike lane, grows as the snap nears). Helpers: _snapz_pick_lane()/_snapz_lane_x(). bossshot now shows the chomp.
- [~] **Gerald the IMMENSE variety** v1.11.93 NEEDS PLAYTEST — phase 1 was ~80%% slam (skim-rake only 20%%); bumped phase-1 skim to 30%% for a better slam/skim mix (phase 2 stays 42%%). He already has a real ultimate (FEATHER STORM). The Eternal (asc 2) untouched.
- [ ] NEXT: per 'don't iterate the same feel twice', do NOT re-tune Snapz until Scott playtests. Move to: audit Gerald(non-eternal)/heron/other bosses, upgrade toward Gerald-Eternal quality.

## ➕ RACCOON MASK FIXES (Scott, 2026-06-25)
- [x] **Raccoon missing from wardrobe** v1.11.88 — no flat wear_raccoon.png existed (wardrobe loads art/wear_<id>.png); the gen had 3D worn sprites but no make_raccoon() flat icon. Added make_raccoon() to gen_wearables.py + registered it; generated wear_raccoon.png. Now shows in the grid.
- [x] **Worn artifact** v1.11.88 — the build had a snout stripe at z16-20 that floated forward past the bill (the stray sliver) + ears tucked at z5-6 (back of head). Dropped the snout stripe; moved the ears to z14 (head-top, by the mask). Regenerated all wear3d_raccoon sprites. Reads as a clean bandit mask now.
- NOTE: raccoon is still excluded from the MEGA-hop stack-meld (hats dict in voxel_duck ~2489) so the mask won't ride the MEGA tumble — minor, separate, not reported.

## ➕ CHRISSY SLEEKER (Scott, 2026-06-25)
- [x] **Chrissy rebuilt long + sleek** v1.11.87 — was ~23x13 voxels (1.8:1) = squat, didn't read as a wooden speedboat. Rebuilt build_boat() to ~33x11 (3:1): long raked bow tapering to a point, gentle barrel-back stern, twin green cockpits along the longer deck, mahogany planking + gold seams, chrome windshield, transom flag. Regenerated donni.png (in-game) + the 16-frame donni_spin (codex). Reads as a classic Chris-Craft runabout now.

## ➕ RIVER / SCENERY OVERHAUL (Scott, 2026-06-25) — PLANNED THREADS COMPLETE
Goal: water/scenery too flat ('Pokemon on Gameboy'); make each of the 7 biomes a UNIQUE, beautiful set (water + logs + side-land + whimsy). Biome identities already exist in code: Lazy Pond, Park Picnic, Spooky Bog, Sand Pond, City Fountain, Emerald Lake, Aurora Lake. Currently only 2/7 have atmosphere FX; water/banks are just a tint.
- [~] **Pace-independent pond duration** v1.11.81 — NEEDS PLAYTEST. Biome was raw distance/THEME_LEN, so at ramped speed (~3x) ponds flew by 3x faster. Added biome_progress (advances at constant BASE_SPEED) driving the biome index -> each pond lasts a steady ~42s regardless of pace. Tune THEME_LEN if 42s feels long/short.
- [x] **Per-biome atmosphere (all 7)** v1.11.82 — each pond now has its own floating whimsy: Lazy cottonwood fluff, Park butterflies, Bog fog, Sand heat-haze+motes, City mist, Emerald FIREFLIES (brightened), Aurora ribbons+snow (moved aurora to the correct biome 6). Added --bioshot dev capture (all 7). Some are intentionally subtle (fog/mist); can amp any. Visual.
- [x] **Water calmed (less distracting)** v1.11.90 — Scott: updated water was distracting. The wash (per-biome colour) was fine; the brighter caustics + moving ripple-lines pulled the eye. Removed the ripple-lines, halved caustic intensity + steadied their blink. Keeps per-biome colour variety, calm motion.
- [x] **Per-biome water WASH** v1.11.86 — Scott: water still looked the same (a tint-mult on one tile barely shifts it). Added a real per-biome colour WASH over the water (murky green Bog, turquoise Sand, indigo Aurora, vivid Emerald, steel City) + brightened the caustics + drifting wave-line highlights. Water now clearly differs per pond.
- [x] **Per-biome water caustics** v1.11.83 — water was the SAME scrolling tile everywhere (the flat feel). Added drifting parallax caustic light-pools, colour + intensity varying per pond (gold on Sand, cool on City/Aurora, murky green in Bog), so the water reads with depth + life. Visual.
- [x] **Per-biome shore decor** v1.11.84 — added _draw_bank_decor(): scrolling per-biome shoreline props (Lazy cattails, Park picnic umbrella, Bog dead trees, Sand sandcastles+flag, City lampposts, Emerald ferns, Aurora snowy pines). Sits on the 26px bank, leans <=16px into water (no item overlap). Some subtle (bank is narrow) but each pond now has distinct side-land. DONE.

## ➕ TRASH SHIELD: INFINITE FIX + ORBIT ATTACH (Scott, 2026-06-25)
- [x] **Infinite-shield exploit closed** v1.11.79 — TRASH MAGNET did `shield_charges += 1` every 5th trash with NO cap (and shield_charges was never clamped), so river trash = unlimited shields. Capped the trash-magnet gain at shield_charges < 3 (v1.11.80; was 5 — too safe given how easy trash is to grab): trash can sustain up to 3 bonk-shields, never infinite. Other shield sources (one-time picks, boss heals, halo) untouched. SCRAP SHELL's orbit armor was already bounded (24-trash hoard, upkeep-gated) — left as designed. [feel tweak — fine to retune the cap]
- [x] **Trash orbit stays attached in flight** v1.11.79 — `_draw_trash_orbit` was pinned to (duck_x, BASE_Y), so during MEGA/UPDRAFT it orbited empty water while the duck flew up. Added `duck_render_pos` (the duck's on-screen centre each frame) and the orbit now follows it up. Verified via MEGA capture.

## ➕ SNACK PROGRESS REFRAMED (Scott, 2026-06-25 morning)
- [x] **Snack power-ups reworded: 'carries you further' not 'adds distance'** v1.11.78 — Scott's call: keep the mechanic, fix the confusing framing. Reverted the v1.11.77 balance nerf (back to 0.6). Reworded the snack-progress descriptions (PIRATE HAT, GOLDEN BILL, LIFE JACKET, BREADWINNER) from '+X% distance/score' to 'every snack carries you +X% further downriver' — reads as forward progress per snack, not a weird capped-distance stat. No balance change.

## ➕ UPDRAFT WINGS REDO (Scott, 2026-06-25 morning)
- [x] **UPDRAFT now flies on its NATIVE wings** v1.11.75 — Scott (rightly) hated the procedural triangle wings I bolted on overnight. Removed them; during the glide the duck now uses its OWN wings-out voxel frames (cur["hop"], the same flap pose Rusty uses), at a soaring ~8fps beat. Reads as a real duck flying, banking with steer. NEEDS PLAYTEST for the motion feel.

## 🌙 OVERNIGHT ART LOOP
**PASS COMPLETE — 17 visual improvements shipped (v1.11.58 → v1.11.74).** Later idle ticks verified these systems already polished, no change warranted: pause screen, fade transitions, Shadow Drake, CHRISSY/Donny, boost logs (glow+chevrons), heron dive telegraph (growing strike shadow), wingduck escorts, snacks/ducklings (shadows). No gameplay-FEEL changes were made (all pure visual; nothing needs playtest). Loop left alive on slow idle ticks for anything genuinely worth shipping.
 (2026-06-25)
- [x] **Landing splash droplets** v1.11.74 — touchdown had a ripple + splash SFX but no droplets; added a 7-droplet water splash on every hop landing (the most-frequent action) for more juice. Transient effect — shipped on code inspection (same proven particle pattern as collect/mega), not a frame capture. Also: CHRISSY (Donny) is a lovely Chris-Craft runabout, no change needed. Visual only.
- [x] **Boss codex spotlight** v1.11.73 — extended the warm display spotlight (cycle 6, ducks only) to the BOSS specimens too (Gerald/Snapz/etc.), so every codex entry is showcased consistently. Gerald's heron model looks great. Visual only.
- [x] **Locked-duck padlock** v1.11.72 — locked ducks on select showed a gray silhouette + bare 'LOCKED' text; added a small drawn padlock icon next to it for a clearer, more polished locked state (added a reusable --lockshot dev capture). Visual only.
- [x] **Biome arrival banner tint** v1.11.71 — the 'now paddling into <Pond>' banner was always blue; each biome's name now takes on its own palette tint (Emerald Lake reads green, Sand Pond sandy, etc.) so the arrival feels like that place (added a reusable --biomeshot dev capture). Note: the 7 biomes are real North Andover ponds — nice local touch. Visual only.
- [x] **MEGA HOP power aura** v1.11.70 — the giant invincible leap had no 'power' read; added a pulsing GOLDEN energy ring + glow around the MEGA voxel-tumble so it feels crushing/invincible (added a reusable --megashot dev capture). Visual only. That's all 5 specials (MEGA/LASER/AFTERBURNER/TORNADO/UPDRAFT) now polished.
- [x] **TORNADO waterspout funnel** v1.11.69 — the tornado special was just a sparse spray ring; added a real swirling WATERSPOUT funnel (6 rotating spiral arms widening upward) rising from the duck + a churned spray base, so it reads as a spinning waterspout (added a reusable --tornadoshot dev capture). Visual only.
- [x] **AFTERBURNER speed lines** v1.11.68 — the dash had only the shared fire trail; added blazing orange SPEED STREAKS rushing past + a hot glow around the duck while dash_t is active, so it reads as a fast ablaze dash (added a reusable --burnshot dev capture). Visual only.
- [x] **QUACK LASER beam intensified** v1.11.67 — the beam was a flat pale band; rebuilt it as a SEARING beam: wide halo + hotter mid + white-hot core + energy bands racing UP the beam + a muzzle flash where it erupts from the duck (added a reusable --lasershot dev capture). Visual only.
- [x] **Menu duck-fact readability** v1.11.66 — the menu's duck-fact line was washed out at 0.6 white; warmed it to a readable cream tint so the facts (a charming birder touch) actually read. Note: gameplay snacks + ducklings already cast shadows/hover — the game is genuinely well-grounded. Visual only.
- [x] **Menu hero pond ripple** v1.11.65 — the main-menu duck floated with only a faint shadow; added a soft contact shadow + gentle expanding pond ripples so it sits ON the river (also added a reusable --menushot dev capture). Visual only.
- [x] **UPDRAFT banking** v1.11.64 — completes the flight ask: the duck now BANKS (tilts up to ~24deg) into your steer while soaring, on top of the flapping wings + wind streaks. Visual only.
- [x] **Codex specimen spotlight** v1.11.63 — duck specimens in the codex floated with no backing; added a soft warm display spotlight behind them so each bird feels showcased like a gallery exhibit (birder-friendly). Visual only.
- [x] **Ascending duck golden halo** v1.11.62 — the magic-bread feast duck got lost on the busy rainbow backdrop; added a soft pulsing golden halo behind it so the star of the victory pops. Visual only.
- [x] **Draft rarity aura** v1.11.61 — rare/epic boon cards now get a soft pulsing GLOW behind them (blue for rare, brighter gold for epic; commons none) so a good pull pops. Visual only.
- [x] **Death-screen skull marker** v1.11.60 — the killer line led with a literal letter "x" (read as a glitch); replaced with a small drawn bone-skull icon on both the death screen + logbook run-detail. Minor: the log-death subtitle still reads "a log (left of the log)" — wording, low priority.
- [x] **SHELL CYCLONE vortex** v1.11.59 — replaced the static concentric arcs with 3 ROTATING spiral arms + a foam rim + rim spray, so the cyclone reads as a real roaring vortex (visual only; spin feel untouched).
- [x] **UPDRAFT wings** v1.11.58 — the glide wings were tiny dark triangles that did not read; now BIG flapping mallard wings (dark leading edge, white trailing edge, feather slat) spread off both sides + more wind streaks. Reads as real flight now.

## ➕ SADIE RUN + MORE (Scott, 2026-06-25)
- [x] **Sadie run ABANDONED -> cute in-place pounce** v1.11.56 — the across-screen run was a SEPARATE side-profile model that never looked like her (eerie/Pokey, thin legs). Reverted: she plays fetch IN PLACE with her actual greeter model (drops the chuckit ahead, play-bows, POUNCES with a squash, catches it). Looks like HER now. | - [x] **Snapz spin full-size** v1.11.56 — kept him COLOSSAL (no jarring shrink); a bigger leap-arc clears the lane at the turns + the danger ring carries the hitbox read. | ~~v1.11.54 8-frame trot~~ — root cause: 4 discrete frames SNAP between poses = robotic. Rebuilt as an 8-FRAME smooth trot with a CONTINUOUS gait trace (legs interpolate, no snapping) + slim tapered legs. Attempt #6 — NEEDS Scott playtest (+ hard refresh for cache).
- [x] **Sadie run YELLOW EYES** v1.11.55 — the run model had a big amber eye ellipse that glowed yellow at speed; swapped for small dark kind eyes.
- [x] **Stats compacted + bigger duck** v1.11.57 — HOP/STEER/PACE/SIZE now a tidy 2x2 grid (2 rows, not 4); duck preview bumped 6.0->6.9 for more presence.
- [~] **TAKE WING -> UPDRAFT** v1.11.57 — renamed; added wind streaks + beating-wing visuals during the glide. DEEPER flight feel (proper flap animation, pronounced banking) queued for the overnight art loop.

## ➕ POLISH (Scott, 2026-06-24 late)
- [x] **Duck quip bubble crowding the duck** v1.11.51 — bubble had nowhere to go (above=duck/hat, below=name) on the packed screen. Dropped the bubble for a light QUIP CAPTION in quotes under the title — no chunky box crowding anything.
- [x] **Settings ON/OFF misaligned** v1.11.51 — the toggle text drew above the box (baseline math). Now both the label + ON/OFF are vertically centred in the box.
- [x] **Sadie legs pool-noodly/too big** v1.11.52 — thinned + SHORTENED the trot legs, TAPERED them (thin ankle to thicker thigh) + small neat paws, proportional to her body now. | - [x] **Speech bubble RESTORED** v1.11.52 — Scott liked it; put it back high in the freed top space (tail down to the duck), clear of the duck + title. | - [x] **Sadie run still not dog-like** v1.11.51 — the BOUND (both leg-pairs in sync) read as hopping. Switched to a TROT: near front + near rear always SPLIT (one planted, one swinging, half-cycle out of phase) + a knee bend so legs aren't stiff posts. Softer in-game bob.
- [x] **Version name stuck at 1.11.40** v1.11.51 — a silent sed mismatch froze GAME_VERSION while code kept incrementing; resynced to 1.11.51.

## ➕ BALANCE + SNAPZ (Scott, 2026-06-24)
- [x] **SNAPZ spin SIZE + HITBOX** v1.11.53 — he was COLOSSAL (3.1x) so the spin ate the screen + the hitbox was unreadable. Now he TUCKS into a compact spinning shell (1.3x spin / 1.6x cyclone, matching the hitbox) + an explicit RED DANGER RING at the strike zone that brightens when he is deadly-low and fades when he leaps safe-high. | - [x] **SNAPZ spin DODGEABLE** v1.11.50 — it swept the full lane AT the waterline the whole time (14px arc) = undodgeable, in your zone everywhere. Now a BIG vertical arc: deadly-low only crossing centre, LEAPS HIGH at the turns so the edges are safe zones to weave to. Slower sweep + tighter hitbox. | - [x] **SNAPZ spin SMOOTHED** v1.11.44 — ripped out the pinball wall-bounce (the sharp velocity flips were the jank). Now a SMOOTH sine SWEEP across the lane (amplitude eases in, dips low crossing centre, rises at the turns) — a readable rhythm you hop. Cyclone ult uses the same, wider+faster.
- [~] **Late-game play-forever** v1.11.45 — two root causes: (1) DIFFICULTY PLATEAU: log + heron density both capped (the +0.25 log floor / the 0.6 heron clamp) so the threat flatlined past the bread. Added ENDLESS HEAT: hazard density climbs 1x to 5x the longer you push past where endless began. (2) PERMANENT INVINCIBILITY: a snack+loft+GLIDE build hoovered enough snacks mid-glide to refill the meter before it ended = chain forever. LOFT now fills at 0.4x while invincible, so there is always a vulnerable gap between specials. NEEDS PLAYTEST to tune.

- [x] **Sadie run was disturbing** v1.11.49 — root cause: each frame cropped to its OWN bbox, so the body jittered horizontally + the bounce got cropped away (legs flailing in place). Fixed: stable body/head, smooth gait, all 4 frames on ONE union canvas (no jitter), and the BOUND arc applied in-game (rbob) so she actually rises/falls as she runs.
- [x] **Sadie bubble follows her** v1.11.49 — while fetching, her speech bubble now rides above her head instead of staying home (she ran through it).
- [x] **Hen/Random below PLAY** v1.11.49 — moved the DRAKE/HEN + RANDOM buttons from the top to under PLAY; reflowed the duck/name/stats/PLAY up 44px into the freed space.

## ➕ MENU CLEANUP (Scott, 2026-06-24)
- [x] **Redundant wardrobe text** v1.11.42 — removed the HEAD/BODY equipped-outfit text at the top of select (you already see your outfit ON the duck + as icons in the WARDROBE chip)
- [x] **Rusty tap-me** v1.11.42 — moved the "tap me!" prompt up under his perch, off the PERKS header it was colliding with
- [x] **Drake/Hen glyph** v1.11.42 — was ALWAYS the female symbol; now draws male (circle+arrow) for DRAKE, female (circle+cross) for HEN
- [x] **Duck-select QUIP BUBBLE overlapping the duck** v1.11.42/43 — Scott clarified it was the tap-to-change speech bubble. Lifted it from y236 to y212 so the tail clears the duck hat (e.g. turtle shell), still below the DRAKE/RANDOM buttons. (Also removed the redundant top HEAD/BODY outfit text.)
- [x] **Name-field bleed** v1.11.42 — the duck-name LineEdit (a UI node, renders on top) bled through the wardrobe/slot modals (the floating "ducko" box); now hidden whenever a modal covers select

## ➕ SADIE + SNAPZ FIX (Scott, 2026-06-23 eve)
- [x] **Sadie facing/scary/voxel-ball/cat-run** v1.11.37 — she faced her REAR (yaw 208 = back-3/4); fixed to front (yaw 18). Dropped the big glowing amber eyes (scary). Greeter is now the proven-cute SWIMMING model, dry chocolate coat, proudly holding her VOXEL chuckit, facing you. Tap = excited bounce + bark. DROPPED the cat-gallop fetch run (it was the problem) — can revisit a proper lab-bound later.
- [x] **Snapz fight reworked AGAIN** v1.11.37 — my depths-ambush was bad (the red-circle thrashing). REVERTED it. Restored the whimsical SHELL SPIN but POLISHED: smooth eased careen (charges toward you, no teleport-lunge), bounces off banks, continuous wake + foam spray, the shell visually spins (turntable). New ultimate SHELL CYCLONE: amped longer/faster spin in a water vortex, he announces it, long stomp window after. NEEDS PLAYTEST for feel.

## ➕ BOSS PASS (Scott, asc 2 playtest, 2026-06-23)
- [x] **Gerald #1** v1.11.31 — added a shadow racing on the water below him (sells flying/altitude), bigger swoop arc, calmer float-tilt; removed the "FEATHER STORM!" text banner (the gathering feathers + safe-beam telegraph it)
- [x] **Snapz reworked** v1.11.32 — KILLED the pinball shell-spin. New DEEP AMBUSH: he vanishes into the murk (faded dark shape + bubbles), STALKS under the duck, then ERUPTS from below with a snap (red ring telegraphs where — you must keep moving). Jaws jam after = stomp window.
- [x] **Snapz ultimate** v1.11.32 — replaced TIDAL SLAM with FEEDING FRENZY: a flurry of 5-7 rapid tracking ambushes from the depths, then he is exhausted (stomp window).
- [x] **Snapz back legs** v1.11.32 — defined muscular hind limbs (thigh + splayed clawed foot) that read from the side/back turntable angles, instead of stubs tucked behind the shell.
- [x] **Gerald the ETERNAL** v1.11.31 — dropped Feather Storm; his own ult is now HERON SWARM (8 waves of spectral kin raining down); faster heron-add cadence (harder)

## 🆕 NEW — autonomous additions (shipping as I go)
- [x] **Death-screen glow-up** v1.11.28 — the fallen duck (with its exact outfit) bobs above the eulogy as a memorial: somber-tinted on a death, golden-haloed on a win, drifting feathers for mood
- [x] **RACCOON MASK wearable** v1.11.27 — a trash-bandit head piece (mask + ears + striped snout); snacks AND river flotsam magnet in from way farther (great for junkyard builds, useful for any)
- [x] **Glide shadow** v1.11.24 — a shadow races on the water under your glide, shrinking as you climb (sells the height)
- [x] **GOLDEN HOUR** v1.11.24 — now and then the river bathes in warm low-sun light for a stretch (a birder favourite)
- [x] **The whole BROOD takes wing** v1.11.16 — ducklings soar with you in formation during a glide (+ a 'wheee!')
- [x] ~~Migrating FLOCK~~ REMOVED v1.11.23 (Scott: "flying v is dumb")
- [x] **TAKE WING (glide special)** v1.11.15 — ducks FLY! a new special: soar high + invincible for ~3.6s, banking free with your steering, hoovering snacks in a wide arc, drifting a feather trail, then a soft touchdown. (Scott's idea.)
- [x] **JUNKYARD trash cluster** — DONE v1.10.92: river trash now becomes a resource. 3 new power-ups:
      **TRASH MAGNET** (trash drifts into your lane; every 5 grabbed = a free BONK — your exact idea),
      **PACK RAT** (each bit of trash = +3 feathers), **JUNK SLINGER** (your hoard auto-chucks to bonk
      herons / chip logs). Full collection system + HUD hoard meter (bin + count + 5 bonk-pips) + synergy
      cluster (trashmag↔packrat↔junker + magnet/gold/cannon) + voxel icons.

## ❗ OPEN — owe you these
- [x] **Settings menu overcrowded** — DONE v1.10.87 (verified): re-spaced everything — toggles no longer cramped,
      VIEW-LOGS no longer overlapping PLAY-TUTORIAL, SFX-test duck moved below the buttons (was over RESET)
- [x] **More settings** — DONE v1.10.93: added **SCREEN SHAKE** (off for comfort) + **REDUCED FLASHING**
      (photosensitivity — dampens boss white-flash + jukebox disco strobe), both persisted. Also fixed a latent
      bug where MEGA-DEEP QUACKS never actually saved.
- [x] **Boss FIGHTS "way better"** — DONE v1.10.95: added a NEW horizontal **SKIM-RAKE** attack (Gerald banks
      wide + rakes low across the lane — you HOP it; telegraphed band + sweep arrows; more frequent in phase-2),
      plus a clear **DAZED WEAK-POINT** telegraph (pulsing golden target ring + bobbing chevron) so the stomp
      window is unmistakable. Fight now cycles: dive · skim · spit · combo-chain · adds · tail-sweep · phase-2.
- [~] **Music COMPOSITION** — HELD honestly: tune is already structured (24-bar A/A form, motif dev, clean resolution) + loop fixed. I cannot HEAR output, so a subjective rewrite is the one place my judgment is blind. Left for Scott's ears + a vibe direction rather than risk a regression.
- [x] **Lucien in the BOON/draft menu** — DONE v1.10.94: replaced the static loon with his compact DJ booth running the same scratch/tap/drop routine + a spotlight, consistent with the shop
- [x] **Scenery transitions smoother** — DONE v1.10.96: banks soft-fade like the water (was a hard cut), wider wash band (220px), slower sweep.
- [ ] **"Everything visually appealing / good UX"** — standing bar, never closed
- [ ] **Upper-ascension mechanics felt "weird/clunky"** generally (crosswind + thwomp fixed individually; the broader feel not audited)

## ✅ VERIFIED (Claude pre-checked via code/capture)
- [x] **HUD pinned during MEGA** — code: the pin block (affine_inverse) wraps status icons + pace flames +
      minimap/timeline; corner buttons pinned separately. Shouldn't drift.
- [x] **Wearables ride the duck on hops** — drawn inside the duck's hop transform (+ mega stack interleaves them)
- [x] **Power-up pips span the whole map** — loop shows up to 10 upcoming drafts across the full timeline
- [x] **Ducks menu fits** — capture confirms 18 ducks in 2 clean rows of 9, none off the bottom
- [x] **Rusty not in two places** — moot: the boon helper is now LUCIEN; Rusty is only tutorial + shop

## 🟡 VERIFY — need YOUR eyes in-game (feel/motion, can't capture)
- [x] **"THWOMP" was Nintendo IP + a stone face in a wood game = wrong** — DONE v1.10.88: renamed to
      **DEADFALL** (real logging term); rebuilt the model as a heavy gnarled WOODEN log (bark, splintered
      cut-ends, knots, moss) — no stone, no face. Telegraph + impact kept.
- [x] **DEADFALL/crazy logs** — MOOT (disabled on ice per Scott)

## ➕ MISSES I dropped AGAIN (Scott, 2026-06-22)
- [x] **Donni → Chris-Craft ("Chrissy") boat inspo** — DONE v1.10.89: rebuilt as a classic Chris-Craft —
      varnished mahogany, cream king-plank + covering boards, chrome windshield, red twin cockpits, burgee, barrel-back stern
- [x] **RENAME the boat character Donni → CHRISSY** — DONE v1.10.91: codex name, catchphrase ("can't catch
      CHRISSY!"), death msg, wake labels, bonk flashes all say CHRISSY now (internal `donny` id left as-is)
- [x] **Bread "still looks bad"** — DONE v1.10.90: rebuilt as a clean round sourdough BOULE — golden crust
      shading dark at the hearth base, a clean bloomed cross-score showing pale crumb, light flour dusting
      (was a lumpy loaf with blotchy messy scoring). Re-rendered sprite + 16-frame codex turntable.

- [ ] **Bread fly-in + Donni's wake pass** look right in motion (voxel models verified static only)
- [ ] **Jukebox disco** is fun + Lucien's routine (scratch L/R, tap, drop) reads

## ✅ DONE (shipped)
### Ducks / hens
- ✅ Real per-species dimorphic HENS + accurate plumage · slight stat variation · ♀ toggle moved to a good spot + stats now change · reconciled the standalone Hen Mallard · hen art viewable in codex (toggle) · text/quips for new ducks · 3 new ducks + the Loon(Lucien) · ? RANDOM ? roll (random duck + random wearables + maybe hen) · menu-duck wing-flap on weighted taps · goldeneye N64 quips (slappers/dam/license)
### Wearables
- ✅ Two-slot head+body system + synergetic combos + set bonus · "far more bodies" (cape/vest→life jacket/jetpack/satchel) · turtle shell + all body items now on the BACK not the head (was the build_hat None bug) · life jacket no longer renders through the pirate hat (z-order) · scarf/cozy-scarf revalued · boombox moved to a HEAD item · ducklings wear your outfit (toggle, "DUCKLING BROOD MATCHES YOU") · duckling fixes: trail further back (off the butt), wearables sit lower (no float), keep gear on jumps
### Bosses
- ✅ Snapz directional fight (left/mid/right/tail) + rear legs + open-jaw codex turntable (works any angle) · Snapz BIG + frontal-locked in codex · Gerald cinematic swoop entrance (random side, low pass, settle) replacing the trash shadow · longer/menacing intros · Gerald beak opens in-fight + codex · one legendary per boss (1st) / two (2nd) + synergetic lower-rarity alongside · distinct death msgs (chomp vs muck-glob) · softer "bested by" wording · timeline snapz big
### Lucien / jukebox / music
- ✅ Loon added as Lucien (DJ + boon sage; Rusty stays tutor/shop) · codex entry + preview · voxel DJ rig (console + turntables + LED) that rotates (cycles views) + bounces + scratches · record-scratch SFX on tap (shop/boon/codex) · black loon w/ contrast fix · jukebox in shop (own whimsical screen) · preview-before-buy + BUY buttons · scootybooty unlocks tracks · longer ambient tracks · MUSIC LOOP fixed (was QOA lossy codec → PCM/IMA + crossfade) · boombox heavy rap beat
### UI / shop / misc
- ✅ Rusty smarter (archetype-aware advice, varied, not "rare bird"/"on fire is a berry") · settings decluttered (jukebox out) · toggle text un-clipped · shop special live demos in modal · select shows HEAD/BODY outfit readout · graphs fixed · thwomp reworked (fair telegraphed positional hazard) · crosswind + breeze direction art · special-hop frequency lowered · crazy/tumbling logs built · mega-hop collection nerf · scootybooty unlocks ascensions · donni outline softened · on-fire no longer a berry
### Crash + icons
- ✅ Web crash: leaned audio memory ~16MB→5MB (IMA-ADPCM) + `[boot]` console breadcrumbs · ALL boon/power-up icons → tiny VOXEL objects (27 models) · Donni/bread re-modeled + spinnable codex turntables

## ➕ MISSES I dropped (logged from Scott)
- [x] **Hen/Random buttons** — placement + style. DONE v1.10.82: moved below the title (was overlapping it),
      restyled as clean pills (♀ + DRAKE/HEN, a die icon + RANDOM)
- [x] **THWOMP overhaul** — DONE v1.10.84: a proper VOXEL stone face (glowing furious eyes, jagged teeth, moss,
      squints on slam) replacing the rearing log; bold telegraph (red double-ring + looming shadow + chevrons);
      heavier impact (big shockwave ring + stone dust + moss bits + shake)
- [x] **Crazy logs tamed** — DONE v1.10.84: rarer (3.5%, starts 4500m), calmer weave (105 vs 175), slower tumble
- [x] **SHOP made whimsical** — DONE v1.10.85: a duck-disco — spinning disco ball casting colored spotlight
      beams, a dancing DUCKLING crowd bopping along the bottom, a rainbow equalizer pulsing to the beat
- [x] **Lucien's booth detail + DJ routine** — DONE v1.10.86: detailed console (equalizer face, knobs, faders,
      flanking speakers, LED strip); he cycles a routine — scratch right deck → scratch left → tap mixer →
      throw a wing (or BOTH) up for the DROP, with a hype-pop bounce
- [x] **In-app APPLICATION LOG viewer via scootybooty** — DONE v1.10.83: scootybooty → Settings → "VIEW APP LOGS";
      captures boot phases + `[env]` (OS/godot/res/mem) + run starts + deaths (errors red). `_log()` buffer (200 lines).
- [x] **Duck-menu wardrobe button wasn't BODY-item aware** — DONE v1.10.81: the select-screen wardrobe chip now
      shows BOTH slots (head icon + body icon, empty-slot rings) instead of just the head item
- [x] **Turtle shell sat too low on the back** — DONE v1.10.81: raised the shell ~2 voxels (prof y7-10) so it sits proud

## 🆕 JUNKYARD expansion (v1.10.98)
- [x] **DUMPSTER DIVE** (rare) — every 10 trash grabbed coughs up a guaranteed RARE snack (junk→treasure)
- [x] **SCRAP SHELL** (epic) — your hoard is armor: a hit is eaten by 4 trash + brief i-frames (wired at the
      die() chokepoint so it covers EVERY hit-death); strong with TRASH MAGNET feeding the bin
- [x] **Synergies wired**: DUCKLING SCHOOL now tractors trash too · ON FIRE + trash = FLAMING junk that melts
      logs 2x · full synergy-tag web across the 5-card cluster
(Moved 2 of the PROPOSED trash toys to DONE.)
- [x] **Snapz new attack** v1.10.99: a telegraphed **MUCK GEYSER** — a 7-glob bullet-hell fan across the lane in phase-2 (now BOTH bosses got new moves).

## 💡 PROPOSED (theorized during playtest — Scott picks what's fun)
### More trash power-ups (the JUNKYARD theme has legs)
- **SCRAP SHELL** — your hoard is armor: each piece of trash absorbs a bonk (spend junk, not your life)
- **DUMPSTER DIVE** — every 10 trash auto-spawns a guaranteed RARE snack (junk → treasure)
- **OIL SLICK** — chuck trash behind you; logs that hit the slick slow/stall (zoning/defense)
- **RACCOON** — snacks you grab leave a bit of trash you can re-grab (snack↔trash combo loop)
- **HOARDER'S LUCK** — +draft-rarity odds the more trash you're holding (build-around)
### Boon synergies to wire
- TRASH MAGNET + THICK FEATHERS → trash-bonks overcharge the shield (stack higher)
- JUNK SLINGER + CRUMB CANNON → junk joins the cannon's 3-way spread (double dakka)
- PACK RAT + GOLDEN BILL → trash feathers also doubled
- TRASH MAGNET + ON FIRE → collecting while lit flings FLAMING junk (melts logs)
- DUCKLING SCHOOL → ducklings tractor trash too, not just snacks
### General enhancements
- Near-miss on trash = style/LOFT (rewards greedy grabs)
- High-ascension "JUNKYARD" modifier: river chokes with trash (more hazard + more payoff for trash builds)
- Gerald picks up & hurls trash as a boss attack (ties the theme together)
- Codex JUNKYARD stats page: trash grabbed by type (extends the flotsam codex)
- A "trash crown" / raccoon-mask wearable cosmetic


## 2026-06-27 — UNDERWATER STRETCH shipped (v1.12.0)
- Scott: 'logs get monotonous' + wanted a fresh layer-shift (dive underwater / clouds). Built a WHIRLPOOL-triggered UNDERWATER DIVE: steer into the vortex -> swim a continuous stretch (same steer + hop=kick) hopping sunken logs, dodging darting fish, grabbing pearls (+feathers), then surface. CLOUD fly-over NUKED (Scott: 'it is bad'). Per-species kicking feet. Bot-sim fairness-passed (bot dives + survives, no fish death-spike, a WON run). DONE + LIVE.


## 2026-06-28 — boss consistency pass + Barry spin + shadow unlock (v1.12.1)
- Scott: boss test had inconsistencies (Barry showed GERALD lines). Holistic pass: revive + enrage now per-kind (Barry no longer borrows Gerald's outbursts); dead var + comments cleaned; verified the rest of the Gerald refs are legit.
- Shadow Drake unlock -> ASCENSION-gated (>=1, i.e. beaten the river once); trait+lore text updated. (threshold tunable)
- BARRY: now SPINS + tail-smacks -> in his ENTRANCE (surfaces from the water, no more Gerald sky-dive) AND a battle attack (spin wind-up -> smack). **NEEDS PLAYTEST** (the spin feel + entrance).


## 2026-06-28 — UI: Sadie's Wardrobe + removed DUCK SLOTS (v1.12.2)
- Wardrobe renamed to SADIE'S WARDROBE (title + nav buttons) to match Sadie the greeter.
- Removed the DUCK SLOTS slot-machine (feather gacha) from duck-select — redundant since ducks are already bought with feathers (select a locked duck -> unlock). Dead _draw_slot/_start_slot_spin left parked. (Open space where the button was; can rebalance the select layout if wanted.)


## 2026-06-28 — REMOVED underwater stretch + web-font icon fixes (v1.12.3)
- Scott on the underwater: 'absolutely horrible, no whimsy no pizzazz, 3d nature of the mode isn't used in movement, trash, get rid of it.' FULLY REMOVED (all funcs/vars/hooks/bot logic/capture flag; game verified runs clean).
- LESSON (important): the underwater was the RIVER RESKINNED below the surface (hop sunken logs, dodge fish) — it never used the depth/3D in HOW YOU MOVE, so it felt identical to the surface with a coat of paint. A real layer-shift mechanic must change the MOVEMENT/verb, not just the visuals + obstacle skins. Don't rebuild this without a genuinely different movement model.
- Fixed web-bundle missing icons (web font lacks the glyphs): the menu settings (⚙ -> procedural gear), SKIP ✕ -> SKIP, logbook nav ‹› -> < >, trend ▬ -> -.
- STILL TODO (Scott, same review): logbook run-detail SPACING ("the Mallard" subtitle overlaps; THE TALLY bleeds into SNACK MENU); death-screen menu/logbook buttons need PADDING.


## 2026-06-28 — wooden button redesign (v1.13.0)
- Scott: redesign all in-game buttons with whimsy/ducks, more custom + 'more wood'. Built central _draw_button() = crafted WOODEN SIGN (oak primary/walnut secondary, grain, knot, nail-heads, carved letters). Rolled across MENU, DEATH (+padding fix), DUCK-SELECT (PLAY/DRAKE/RANDOM/MEGA-HOP/WARDROBE), PAUSE, SHOP, shared back, gear->cream.
- STILL TODO: settings sub-buttons (PLAY TUTORIAL/VIEW LOGS/RESET), TUT_SKIP, stats-expand toggle; then logbook run-detail spacing overlaps.


## 2026-06-28 — button polish + logbook spacing (v1.13.2) — DONE
- Per-button RANDOMIZED knot placement (Scott: knots were all in the same spot) — 1-2 knots at hashed positions/sizes + varied grain, stable per button.
- Logbook RUN-DETAIL spacing fixed: de-cramped the header (subtitle/paddling/bested/killer no longer collide), pushed POWERS/relics/TALLY down, widened TALLY->SNACK gap, moved the date off the hint. Verified via --dbg gallery.
- Button redesign + logbook polish COMPLETE.


## 2026-06-28 — boss select + Barry codex icon (v1.13.3)
- Scott: Barry rarely/never showed. Boss selection now: boss1=GERALD, boss2=random(SNAPZ/BARRY), boss3=Eternal (per Scott).
- Barry had NO codex icon (recurring bug): _codex_tex had no 'beaver' case (list icon) AND beaver wasn't in the tex_codex_spin load (detail turntable). Added BOTH. Plus a boot GUARD that logs any boss/enemy/friend codex entry missing an icon or turntable -- so this stops recurring.
- Duck-select wear button label -> 'WARDROBE' (wardrobe screen title stays SADIE'S WARDROBE).
- STILL PENDING: press-feedback + act-on-release for buttons (Scott asked; investigated _input/_on_press, not yet implemented).
