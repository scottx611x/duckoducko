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
- [x] **BOT BOSS-COMBAT AI (grand-takeover pass, 2026-07-01)** — complete per-boss threat model (Gerald dive/skim/FEATHER-STORM gap-seek/eswarm, Snapz lanes/torrent, Barry hurl/wall via predictive glob landing, Bongo tongue/leap/gulp), speed-scaled log anticipation, danger-aware stomp lineups (no more Chrissy-flattens-stomper), persona-weighted DRAFTING (skilled bots buy shields now), shrine boons ON, `--seed=` for reproducible batches. RESULT: forced-Gerald clear rate ~15% -> ~100%; bot now reaches Snapz AND the Eternal (30km) in normal-ish runs. Remaining (parked): per-attack dodge-margin metrics, bigger persona batches.

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


## 2026-06-28 — press-feedback + act-on-release (v1.13.4) — DONE
- Scott: buttons should show a pressed indicator + only act on release. UI button-screens (menu/select/shop/settings/shrine/jukebox/logs/pause/death) now: PRESS depresses the wooden button (down 3px, darker, no shadow) + defers; RELEASE fires the action (slide >42px off to cancel). Gameplay hops + drag-based stats/codex screens unchanged. Verified press-visual via capture + smoke test passes.


## 2026-06-28 — knot/ascension/special polish (v1.13.5)
- Knot pattern now STABLE when a button is pressed (was re-hashing off the shifted rect.position; now hashes the original pos).
- ASCENSION menu deeper explanation: tap the MIDDLE of the ascension bar -> a panel listing every active (stacking) modifier w/ a plain-English description (ASC_MOD_DESCS). < > still dial the tier.
- SPECIAL button now reads 'SPECIAL · <equipped>' to mirror the WARDROBE button (category-first).


## 2026-06-28 — Barry on the minimap (v1.13.6)
- Minimap boss markers used hardcoded is_snapz=(i==1) -> boss slot 2 ALWAYS drew Snapz. Now uses the real boss_kinds[i], so BARRY's mugshot shows when he's the 2nd boss. (Same bug still in the run-detail mugshots ~8046, but past records don't store the kinds — would need saving them.)


## 2026-06-29 — hen-mega fix + 6 boons (v1.14.0)
- HUGE BUG (Scott): hen variants reverted to the DRAKE skin on MEGA HOP. Root: hen variants have NO voxel-stack art, so the mega tumble borrowed ducks[species][stack] (the drake). Fix: _eff_species() for the stack; hens now spin their OWN sprite + keep the golden aura (elif state==St.MEGA). Full 3D voxel TUMBLE for hens would need hen-stack art (follow-up).
- 6 new run-boons shipped: DOWN PAYMENT/PACK LEADER/MOMENTUM/DABBLER/SHOWBOAT/ECHO. Bot-sim COVERAGE GAP — the skilled bot only hit 4 boss clears in 11 runs so the higher-tier new boons barely surfaced; shipped on conservative/capped numbers (pace boons clamped). WATCH playtest for the feather->pace + 3-pace-stack (~1.9x) combos.
- NEXT: build MOODY (mega-frog boss, rotates with Gerald in slot 1). Art to be rendered + validated with Scott.


## 2026-06-30 — BONGO boss (mega-frog, slot-1 alt to Gerald) — IN PROGRESS
- Scott: new boss = MEGA version of the harmless RIVER FROG, rotates with Gerald in slot 1. Name evolved MOODY -> BONGO. Deadpan/unimpressed-but-colossal.
- BUILT: boss_kinds[0] = random gerald/bongo; _start_boss stats (hp+1, scale 1.3); entry SWELLS up from his log; _bongo_fight w/ 3 attacks — TONGUE LASH (lane snap glob), BELLY FLOP (tide wave + dazed stomp window), GULP (vacuum pulls duck_x toward maw); cloned Barry's fair dazed/recover structure. CODEX entry + taunts/stomp-lines/intros. Minimap marker.
- ART (Scott chose hi-res + turntable): authored build_bongo() voxel bullfrog in voxel_duck.py; generates bongo_0/1/2 + bongo_open battle frames + bongo/bongo_open 16-frame codex turntables. Wired tex_bongo into draw/codex/minimap. Procedural maw/eye overlays gated to placeholder-only.
- PENDING: bot-sim balance pass (running) -> then bump version + release.


## 2026-06-30 — BONGO boss SHIPPED (v1.15.0)
- Bot-sim (10 skilled runs): 5 boss clears, NO deaths to BONGO (beatable, not a wall), no crash. Rotation verified ~47% bongo / 53% gerald over 200 resets. BONGO hp=5 @ slot 0 (tankier than Gerald, fair for slot 1). Leans slightly easy — WATCH playtest; can harden hp/attack-gap if Scott finds him trivial.


## 2026-06-30 — BONGO de-cloned (his own froggy spunk) — Scott feedback
- Scott: BONGO shouldnt just be a Barry clone, needs his own spunk. Redesigned his kit to be distinctly FROG:
  - TONGUE LASH: a real extending pink tongue shoots from his maw at your tracked lane -> snaps -> retracts (lateral dodge). Replaces the falling-glob.
  - LILY-HOP BARRAGE: he HOPS 3x across the arena (big arcs), each landing throws a hop-able shockwave wave + ring, then winded -> dazed stomp window. Replaces the belly-flop tide.
  - GULP-N-BELCH: throat pouch inflates + inward air streaks (vacuum reads) pulling duck_x toward his maw, THEN belches a fan of 3 flies. 
  - idle: subtle throat-breathing pulse.
- BUG CAUGHT: an earlier sac edit targeted the first draw_texture_rect(gt...) in the file = _draw_haz_turtle, corrupting it; removed the orphan + placed throat code correctly in _draw_boss_bongo. (Lesson: anchor on UNIQUE text, not a line shared across draw fns.)
- Verifying via bot-sim then re-ship.


## 2026-06-30 — BONGO froggy kit SHIPPED (v1.15.1)
- Bot-sim (8 skilled): no crash, 5 boss clears, mean 10275m. BONGO appears (~50/50) + beatable; still no bot deaths to him (leans slightly easier than Gerald who killed 4/8). Tightened telegraphs (tongue 0.5->0.42, gulp 0.55->0.46, hop 0.46->0.42) for a bit more bite. STILL slightly soft for a skilled bot — WATCH Scott playtest; can add a phase2 (faster when low HP) or harder hit windows if he wants more threat.


## 2026-06-30 — 2 new WEARABLES SHIPPED (v1.16.0)
- LILY PAD HAT (cost 500): +1 duckling joins your brood each run (NEW axis — no wearable boosted ducklings before; fills the empty ducklings-category wear slot). SOU'WESTER (cost 450): +8% all-weather pace.
- Both authored across all 3 layers (flat icon gen_wearables.py, 3D worn + MEGA-meld voxel_duck.py build_hat + _WEAR3D_IDS). Scott approved both; asked to PUNCH UP THE LILY PAD (was green-on-green on the mallard) -> brightened pad + dark rim ring + bigger pink bloom, raised y11-13 domed. Now pops. MEGA-meld verified consistent.


## 2026-06-30 — Lucien art + BONGO fixes + dev menu (v1.16.1)
- LUCIEN art reworked (Scott: not a proper zany loon DJ): orange headphone band + cyan cups, bold checkered back + necklace, big red eyes, slim dagger bill (was a pale club), crest. build_lucien_dj + build_loon in voxel_duck.py. Console kept.
- BONGO bugs (Scott): (1) had GERALD text at half-HP (fell into gerald else -> 'GERALD IS FURIOUS' + gerald feather-storm ult) + ascension-revive line -> added bongo branches ('BONGO IS CRANKY' / 'ugh. STILL here.'), no feather-storm. (2) triple lily-hop waves too closely spaced (0.42s apart = unjumpable) -> added a 'hopland' settle (0.7s) between hops, ~1.1s apart now.
- SCOOTYBOOTY dev buttons (Scott: too crowded): replaced the inline 5-boss row with ONE 'DEV' button -> a PLAYTEST menu overlay (6 bosses incl BONGO + 4 utilities: +5000ft/+500 feathers/fill loft/+3 shields). dev_menu state + DEV_MENU const + _dev_menu_rect/_dev_do/_draw_dev_menu.


## 2026-06-30 — BONGO face dot fix (v1.16.2)
- Scott: weird dot on BONGO's face. Cause: the throat-breathing chin-pouch draw_circle ran EVERY frame (idle breathing) = a faint pale dot on his chin always. Fix: gated the pouch to only the gulpwarn/gulp stages (where the throat actually inflates). Idle face is clean now.


## 2026-06-30 — granular BONGO deaths + dev-menu pause (v1.16.3)
- Scott: still Gerald in BONGO death text; asked if bongo deaths are granular. They were NOT — bongo deaths used cause 'gerald' (so death msg + logbook said GERALD). Barry had the same latent gap (cause 'beaver' wasn't in any map -> showed as 'the river'). Fixed BOTH across 4 spots: death message (_boss_hits_player bng branch: 'BONGO's tongue snatched you' / 'BONGO's splash washed you under'), _killer_label, the logbook 'named' death-bucket dict (BONGO/BARRY (boss) + ic + col), and _sim_death_icon_path (bongo_0/beaver_0).
- Scott: dev menu should PAUSE game progress. Added 'and not dev_menu' to the _update_play gate (~5119) so duck/hazards/distance/boss freeze while the playtest menu is open; picking an option closes it + resumes.


## 2026-06-30 — Lucien 808 bassline + beat-drop (v1.16.4); airpods REVERTED
- Scott reversed the pass-2 Lucien (airpods/taller/short-bill): 'this art is worse, go back, big DJ cans are fine.' Reverted voxel_duck.py via git checkout -> big-cans Lucien restored + regenerated. LESSON: cans were never the problem; the taller+slim+airpods combo read worse.
- NEW: tapping Lucien (store + boon draft) plays an 808 BASSLINE stepped note-by-note (_lucien_808 cycles LUCIEN_808 pitches via the djdrop sfx) so repeated taps build a riff. Every full bar (8 taps) + a periodic in-run timer (drop_t ~24-34s, not during boss/tut/draft) triggers party_t -> a BEAT DROP: the duckling brood goes FERAL in _draw_ducklings (x-jitter + frantic bounce + head-bang roll wiggle + rainbow hsv tint) + 'LUCIEN DROPS THE BEAT' flash.


## 2026-06-30 — REVERT beat-drop feature (v1.16.5)
- Scott: 'hate this feature revert Lucien dropping the beat.' Fully removed the v1.16.4 808-bassline + periodic beat-drop: LUCIEN_808/_lucien_808, party_t, drop_t, the periodic drop timer, and the duckling feral animation (jitter/bounce/roll/rainbow) in _draw_ducklings. Tapping Lucien is back to the plain djdrop scratch. 0 refs remain.
- Art upgrade for Lucien in progress (voxel_duck.py, staged) — showing Scott renders for approval before shipping (keeps big cans; white chest + prouder head + glossy + shorter bill). NOT in this release.


## 2026-06-30 — Lucien art upgrade + profile frame + BONGO faces duck (v1.16.6)
- LUCIEN art UPGRADE (Scott flip-flopped then: 'sorry I like it try it out'): fuller bright WHITE CHEST (reads as a proper loon, black back/white front, not a dark blob), head held PROUD on a longer neck, glossy sheen + hot specular highlight, crisper checkered back, neater SHORTER bill (range 6). Big DJ cans KEPT. build_lucien_dj + (portrait unchanged this round).
- PROFILE frame: Scott wanted a profile view in his DJ routine. Added lucien_dj_p10 rendered at 68deg (own bbox crop so it doesnt shift the front frames); Main.gd loads 11 frames + LUCIEN_SET routine includes idx 10 twice for a side-on beat.
- BONGO facing: Scott 'isnt friggin locked looking right?' -> _draw_boss_bongo now flips horizontally to FACE the duck (face = 1 if duck_x>=boss.x else -1 via draw_set_transform). Verified L/R.


## 2026-06-30 — badge fix + hen text + menu flap/preen + Lucien HEAD-TURN (v1.16.7 pending)
- Codex NEW badge was under the SHOP button (drawn before it + positioned too high overlapping shop bottom). Now drawn AFTER the buttons (on top) + seated at the codex row vertical-center. 
- Hens all said 'trimmer + nimbler, the clever hen' -> added HEN_TAG per-species dict; select subtitle uses HEN_TAG.get(species). Each hen now has her own tagline.
- Menu ducks periodically FLAP/PREEN on their own: idle_anim timer in _process fires select_flap_t/select_preen_t (select) or menu_flap_t/menu_preen_t (title) every ~3.5-7.5s; draws add a hop+wing-arcs (flap) and a head-dip+nibble (preen).
- LUCIEN head-turn (Scott: the one whole-model profile frame is TRASH; wants his HEAD alone turning): refactored build_lucien_dj with head_yaw param — head/bill/eyes/crest/cans built into a temp dict, ROTATED around the neck axis, merged onto the fixed body+console. p8/p9 are now real head-turns (head_yaw ±0.62); removed the trash p10 profile.

- v1.16.7 SHIPPED: all 4 (codex badge / per-species hen tags / menu duck flap+preen / Lucien head-turn frames).


## 2026-06-30 — duckling-hat bank fix + dev boss icons + BONGO tongue (v1.16.8)
- Duckling WEARABLES fucked up on turning (+ during the upgrade draft): the hat used _pick_wear3d (already banked via duck_vx) AND got the duckling roll transform = DOUBLE-BANK/detach. Fix: _wear3d_idle() returns the FRONT frame; ducklings bank via the roll transform only. Draft case is the same _draw_ducklings path -> fixed too.
- DEV playtest menu now shows boss MUGSHOT icons (Gerald/BONGO/Snapz/Barry/Eternal/Bread) via _dev_icon(act); utilities stay text-only.
- BONGO tongue came out of his NOSE: mouth origin was gsz.y*0.06 (eye level); moved to gsz.y*0.19 (his real mouth/maw).


## 2026-06-30 — REAL menu-duck flap/preen poses (v1.16.9 pending)
- Scott: the flap/preen were too subtle/fake ('need to see wings OUT and flappin, neck bent, really getting in there preening'). Replaced the bob+arcs with REAL voxel poses:
  - build() gained a preen param -> post-process rotates the HEAD cluster down+back into the flank (y-z rotation about the neck base). 
  - render loop now saves <sp>_flap0/1 (wings=out/out_up at HERO angle) + <sp>_preen0/1 (preen -96/-112deg) per species.
  - Main.gd: _menuanim(sp) lazy-loads them; menu + select ducks blit alternating flap frames (wings really flap) / preen frames (head buried, nibble wiggle) during the idle windows. Hat drawn at hero yaw during flap; hidden during preen (head tucked).

- v1.16.9 SHIPPED: real flap (wings spread) + preen (neck bent into feathers) menu-duck poses.


## 2026-06-30 — remove preen, keep flap + wearables (v1.16.10)
- Scott: get rid of the preen, keep the wing flap, dont remove wearables. Removed the preen trigger/draw branches + dead vars (menu/select_preen_t); menu ducks now ONLY flap. Wearables stay ON during the flap (hat drawn at hero yaw, no longer hidden). preen frames left on disk unused (harmless).


## 2026-07-01 — flap at CURRENT facing (v1.16.11 pending)
- Scott: the flap locked the duck to a fixed forward-right hero view — weird when it was rotating/facing away. Fix: render a WINGS-OUT TURNTABLE (<sp>_flap_%02d, 24 yaws at hero pitch) instead of the 2 fixed-hero flap frames; _flapspin(sp)+_flap_frame(sp,yaw) pick the wings-out frame at the duck CURRENT yaw. Menu + select draws now alternate folded<->wings-out at _mspin/select_yaw -> the duck flaps IN PLACE at any facing; hat rides the same yaw. Dropped the deg_to_rad(20) hero override + preen frames.

- v1.16.11 SHIPPED: flap plays at the current facing (wings-out turntable), no more snap to front.

## 🎨 GRAND TAKEOVER MANDATE (Scott, 2026-07-01: "take an honest pass over my whole game so far. take over: great art, great replay value, anything else you want. don't resurface till it is great")
- [ ] Honest full-game assessment (art, replay value, feel, UX) — log findings here
- [ ] ART: raise weakest visuals to Gerald-Eternal bar (Scott's stated quality bar)
- [ ] REPLAY VALUE: design + ship systems that make runs feel different (my judgment)
- [ ] Work the 9 OPEN items above where they intersect (esp. standing "everything visually appealing" bar)
- [ ] Playtest via --botsim before claiming anything works; 🟡 anything I can't verify in-motion


### 📋 HONEST ASSESSMENT (2026-07-01, from screenshots + full code/art audit)
**Genuinely great:** character art pipeline (voxel→turntables; ducks/bosses/Sadie rich + consistent), whimsy writing (death deck, boss intros), systems depth (boons/drafts/wearables/ascension/codex/logbook), dev tooling (botsim, shot harness). The Eternal intro's mood = the bar the rest should hit.
**Honest problems, by leverage:**
1. **THE RIVER IS THE WEAKEST ART IN THE GAME.** ~85% of every frame is flat color + sparse dot speckle + two thin repeating bank strips, for 30,000 ft. Characters have love; the canvas is placeholder-grade. Biome washes swap palette but composition never changes (Bog ≈ Aurora ≈ Pond in different hues). DESIGN §7 promised shimmer/parallax; WHIMSY §5-6 promised floating nonsense + per-theme gags — mostly absent in frames.
2. **Boss arenas are empty** — mid-fight frames are a sprite at the top of a bare field. Intro mood doesn't carry into the fight.
3. **Replay structure is 100% fixed**: same boss marks (5k/15k/30k), same biome order/length, same draft cadence. Only variance = 2 boss coin-flips + card RNG + loadout. After first ascension, runs FEEL identical; retention leans wholly on the feather grind + ascension stat-mods.
4. **Bot can't fight bosses** (baseline: skilled bot dies AT Gerald, 1 hit taken) → I can't validate boss work autonomously (open item, line ~111).
5. **Text overlap bugs**: boss-intro title clips the taunt bubble (s_eternal), stacked "3200 ft/3400 ft" milestone text (s_snapz_snap). Small, constant whimsy-killers.
6. **Sparse stragglers**: heron = 4 flat frames (the signature nemesis!); PIKE fully built + 32 turntable frames but unreachable (pulled for Beaver — could return as branch-exclusive, NOT main rotation, respecting the pull).

### 🎯 PLAN (leverage order)
- [x] **LIVING RIVER pass** — shipped: bank foam seams, current streaks, shallow bank margins + deep channel, biome-weighted WATER SCENERY (lilies/duckweed/stones/snags + whimsy floats: bottle, flip-flop, sailboat, frog-on-raft), real pixel-art BANK PROPS per pond (cattails, picnic set, gravestone+dead tree, sandcastle, lamppost, fern+shrooms, snowy pine+snowduck) + a rare COW watching you. Rooted scenery rides the scroll, floaters lag at 0.85x (depth read). 43 new sprites via tools/gen_env.py (voxel pipeline, style-matched). 🟡 VERIFIED via --rivershot themes 0/2/5 stills — Scott should feel it in motion.
- [x] **Boss arena dressing** — per-boss mood tint + vignette + drifting arena motes (Snapz murk/bubbles, Barry lumber, Bongo bayou, Pike cold blue, Eternal blood-red). 🟡 stills pending in-motion check.
- [x] **REPLAY: river FORKS** — the river SPLITS (~12k, then every ~10k): island wedge + two signed channels (pond name + modifier: FEATHER RUN / HERON COUNTRY / CALM WATER / JUNK DRIFT / SNACK BAR / rare PIKE'S HOLLOW). Your side at the wedge = your route; branch modifier lasts most of the stretch. Duck is eased off the island (no grass-paddling). 🟡
- [x] **REPLAY: river EVENTS** — announced, temporary: SQUALL (rain + feathers), TAILWIND (current surge + 2x snacks), LOST DUCKLING (reach the raft -> +1 duckling; miss it and it paddles off, gently sad), FLOTSAM FLUSH, HERON PATROL. ~1-2 per run between bosses. 🟡
- [x] **REPLAY: BIG DAY (daily seed)** — menu pill (golden, rising sun): today's date seeds the run's BONES (boss lineup, shrine deal, each draft's 3 cards, fork spots+choices) — same river for everyone today, replayable all day, per-day best tracked under the pill. (Renamed from 'daily migration' — MIGRATION was already a boon; BIG DAY is the birder term anyway.)
- [x] **Bot boss-combat AI** — see BOT NOTES above; forced-Gerald clears went ~15% -> ~100%, bot reaches the Eternal.
- [x] **Fix text overlaps** — boss speech bubbles suppressed during letterboxed intros (title used to clip them); float-texts anti-stack (step down, capped at 3).
- [x] **Heron art enrichment** — real voxel heron: 16-frame codex turntable (wired into COMPENDIUM) + 2 top-down strike-dive frames replacing the old 4-frame side-view blob in gameplay. Gerald's plumage palette = same species family.
- [x] **Snapz maw-facing** — open-maw turntable now runs through the WIND-UP too (warn/snap/stuck) and the maw points AT the strike lane while he closes on it, then glares at the duck once he's over it. 🟡 (feel = Scott's call, per the no-retune rule this changes ART/READ only, not timings)
- [x] **BOTSIM SAVE POLLUTION FIX** — bot runs were banking feathers + writing run_history/best_m into the REAL save on every batch death. Now sim runs persist nothing. (Save backed up before today's batches.)

### 🚢 RELEASE STATUS (2026-07-01 eve)
- Committed locally: `36f7561` (v1.17.0 work). Web bundle exported + boots locally (HTTP 200).
- [x] RELEASED by Scott's go-ahead (2026-07-01 eve): pushed to main, v1.17.0 live — GH release (APK + web zip) + Pages deploy verified (site 200, assets present). https://duckoducko.scott-ouellette.com
- Save backed up to scratchpad before today's sim batches; bot runs no longer touch the save going forward.

## ➕ PLAYTEST (Scott, 2026-07-01 eve, on v1.17.0)
- [x] **BIG DAY unexplained** v1.17.1 — tap now opens an explainer card (sun + "one river, dealt fresh each morning" + today's best + FLY TODAY'S RIVER button; tap-off backs out). Verified via --bigdayshot.
- [x] **Lilypads distracting** v1.17.1 — scenery now sparse (interval 1.0-1.9s, hard cap 9), hugs the banks (middle belongs to gameplay), 20% smaller, sunk cool+translucent (0.88a), never during bosses, lily/lilyflower weights cut ~35-50%. Verified via --rivershot: center channel clear.
- [x] **Laggy** v1.17.1 — water FX gated to gameplay screens only (menus back to pre-1.17 cost), streaks 14->9, foam 14->10 segs, bubbles 3->2, streaks/foam+shimmer all skipped during boss fights (arena tint owns those frames), scenery capped. 🟡 feel check on Scott's phone.

## ➕ PLAYTEST (Scott, 2026-07-01 night, on v1.17.1 — "this is cooler but")
- [x] **Fork split too fast** v1.17.2 — three fixes: a "the river SPLITS ahead!" call ~800 ft early; the current EASES to 55% while the split is unpicked (real time to read both signs); forks now RARE + meaningful (2-3 per campaign — see waltz item). 🟡 feel check.
- [x] **Pike battle pulled** v1.17.2 — PIKE'S HOLLOW removed from the fork pool (strike two on Pike; not blind-redesigning him a third time). Rare slot is now GOLDEN REACH (a golden-hour branch). ❗ PARKED: if Pike ever returns he needs a horizontal ambush redesign (lurking shadow + lateral torpedo strikes — a pike does not stand on its tail); needs Scott's sign-off on the concept first.
- [x] **Missing codex records — ROOT CAUSE FOUND** v1.17.2 — load-order bug: owned-wearable + magic-bread codex backfills ran BEFORE `codex_seen` loaded from the save, so the load wiped them EVERY boot. Backfills moved after the load. (Also: Pike had no codex entry at all — moot now that the Hollow is pulled.)
- [x] **Wearables during UPDRAFT** v1.17.2 — double-banking bug: glide banks the duck via the shared rotation transform (sprite stays wings-out front pose) but wearables ALSO swapped to side/bank view frames by steer speed — banking twice = hat ripping off on quick maneuvers. Wearables now hold their FRONT frame during glide and bank via the transform, like the duck. (Prop beanie too.)
- [x] **"Waltz through" — ROOT CAUSE FOUND** v1.17.2 — I set fork/event cadence in raw units while reasoning in FEET: forks fired every ~1,000 ft (the winning bot run took 22 forks!), events near-constantly → a feather/snack firehose → free shields/specials. Now: forks ~7.2k ft + ~18-21k ft (2-3 per campaign), events ~8 per campaign, reward mults trimmed a notch (squall 1.3, feather-run 1.45, snack-bar 1.5). 🟡 needs a real difficulty verdict from Scott's next run.
- [x] **Logbook ducks missing wearables** v1.17.2 — run records only ever stored the HEAD item; body (vest/cape/jetpack/satchel/turtle) was never recorded. Now records `wearb` + composites body-then-hat in all 3 logbook duck icons + a body chip in the run detail. (Old records lack the field — they'll stay hat-only; new runs are complete.)

### 🧹 SAVE HYGIENE (same session)
- [x] **Bot WIN path leaked into the save too** — the die() gate (v1.17.0) didn't cover victories: scootybooty's bread run banked +4,936 feathers + wrote history. Win path now gated on bot_mode.
- [x] **Smoke test now snapshot/restores the save** — it used to rename the duck + rewrite feathers/history on every run (this is HOW the dev save's name became "scootybooty" weeks ago).
- [x] **Local dev save cleaned** — all 40 history entries were bot runs: purged; duck_name back to "ducko"; feathers 5045->109 (exactly minus the bot win); best_m 0 (106245 was a bot artifact). Pre-cleanup copy in session scratchpad. NOTE: Scott's PHONE save was never at risk (bots only run via CLI).
- [x] **Hens not showing on main menu** v1.17.3 — the menu hero ignored the HEN toggle (select screen honored it, menu always drew the drake). Now the hen owns the menu too, with the drab-tint fallback for species without hen art. Verified via --henmenushot.
- [x] **Save pollution, FINAL layer** v1.17.3 — verifying the hen fix caught the name field reading "scootybooty" AGAIN: `_sim_start_run` set the bot name BEFORE `bot_mode=true`, so `start_game()`'s last_species _save() fired as a "player". Also gated `_save()` itself on bot_mode (mid-run saves: boss-clear, unlocks). PROVEN clean: full bot run -> zero scootybooty refs, save byte-identical. Dev save re-cleaned (history purge regex fixed — the first two purges silently failed on the pretty-printed format).

## ➕ PLAYTEST + NEW ASK (Scott, 2026-07-02-ish, on v1.17.3)
- [x] **Mega-hop + immediate-flight weirdness = the ECHO boon** v1.18.0 — Scott's memory was right: "half specials" = ECHO's 60%-power encore. THREE bugs: (1) the encore fired a fixed 0.4s after the primary — mid-mega; (2) WILD CARD re-rolled on the encore, so mega -> surprise mid-air TAKE WING ("immediate flight sequences"); (3) if the encore no-opped against a mid-mega guard, the LOFT refund stuck = free full bar. Now: the encore WAITS for the primary to fully play out, and repeats the SAME special.
- [x] **MEGA SADIE — SADIE THE BOUNDLESS** v1.18.0 — alternate FINAL boss, 50/50 draw with the Eternal at 30k (Big-Day-seeded like the rest). She is not evil, she wants to PLAY: CHUCKIT RAIN (canoe-sized balls that BOUNCE sky-high), ZOOMIES (water-line tear, doubles back in phase 2), CANNONBALL (belly-flop -> wave from upriver), ult at half HP = THE POINT (bird-dog stance -> triple pounce). After a throw she watches the balls fly, panting, proud = stomp window ("BOOP HER!"). GOLDEN intro (subverts the dread), warm bubble, happy-bark taunts, "best duck. BEST duck." on defeat, codex entry + turntable. Balance: cold-start bot wins 2/8 vs the Eternal's 3/8 — at the bar, a shade spicier. Per-attack death attribution added to die() (botsim tuning gold). 🟡 her sprite at boss scale is the wardrobe pose set — a dedicated hi-res boss render (Barry-style art pass) is the known upgrade; needs Scott's eyes on the fight FEEL first.
- [x] **Dedicated beautiful Sadie render** v1.18.1 — NEW tools/gen_sadie.py: one upgraded voxel model (canon traits: dark-chocolate coat, AMBER eyes w/ pupils+brows, floppy ears w/ inner fold, tan collar + gold tag, happy tongue), rendered as: 11 hi-res BOSS frames (idle bob pair, THE-POINT glance L/R, play-bow crouch, mid-air pounce, proud-tongue-out daze, 4 gallop) + wardrobe replacements at exact legacy dimensions (greet/p0-p4 @110, spins @56x40). Boss draw wired with graceful fallback. 2 visual iteration rounds (fixed: muzzle occluded the eyes, starburst pounce, unreadable play-bow, emaciated boss gallop). Verified in-scene: boss fight + wardrobe. 🟡 in-motion feel = Scott's call.

## ➕ BOSS PRESENTATION PASS (Scott, 2026-07-02: "bosses should be the whimsical spirit of the game")
- [x] **Living intros** v1.18.2 — the letterbox is now a SCENE: each boss signs the seam in his own ink (swamp green / timber orange / lily green / cold blue / gold / blood red), FLEXES with a pose-pulse as the name slams up, and performs a signature gesture (Gerald: wing-spread feather flourish + screech; Snapz: churning bubble ring + crunch; Barry: proud woodchip spray; Bongo: one slow unimpressed ribbit; Sadie: tail-thunder spray + happy bark; Pike: a single silent ripple). The DUCK reacts in its bubble ("that is a BIG turt." / "do WE have a permit?!" / "SADIE?! you're ENORMOUS!"). 🟡 pacing feel.
- [x] **Huge white mid-fight text KILLED** v1.18.2 — enrage/ult calls now show as a slim boss-tinted ribbon under the pips (small text, dark strip, colored edges); "PATCHED UP"/"TAILWIND" became quiet float-texts; the redundant "HIT!" label is gone entirely.
- [x] **ONE stomp language** v1.18.2 — unified `_draw_stomp_tell`: a soft breathing golden halo + rising sparkles on every vulnerable boss, plus a quiet rising chime the moment the window opens. ALL chevrons + "STOMP!"/"BOOP HER!" banners removed (Gerald keeps his dizzy stars, Barry his star-crosses — those are character, not instruction). Post-stomp text is now a small "boop!".
- [x] **Hit feedback** v1.18.2 — every boss hit: stronger white flash + comic TEARS springing from the eyes + a golden star-pop + a pained squeak. You always know it landed.
- [x] **Sadie posture + RED collar** v1.18.3 — rebuilt to the reference photo: upright seated torso column (no more humped back), head high over a proud chest, collar now HER harness brick-red (196,58,52) + tag. All boss/wardrobe/codex frames regenerated together.
- [x] **Bongo hind legs** v1.18.3 — great folded haunches bulging at his rear flanks + long webbed toes tucking forward, a mottle on each haunch. Frames + turntables regenerated (new tools/regen_bosses.py mirrors voxel_duck's exact render calls).
- [x] **Barry butt + hind legs** v1.18.3 — a real rump bridging body->paddle-tail (the tail no longer floats), haunches + clawed hind feet. 🟡 all three: in-motion eyeball.
- [x] **Sadie boss missing from dev menu** v1.18.4 — SADIE button added (proud-portrait icon); panel auto-sizes to the roster now.
- [x] **"What happened to the fork idea?"** v1.18.4 — it never left: the cadence fix pushed the first split to ~7.2k ft, past where runs were ending — invisible. First fork now ~3.8k ft (before Gerald), later ones stay rare (~every 11k ft).
- [x] **Sadie face-flip + gallop rebuilt** v1.18.5 — she now mirrors to FACE the duck in every pose (Bongo's fix pattern; zoomies flip by travel direction). Gallop frames rebuilt on the NEW model: one continuous fuselage with a real stretch->tuck cycle, ears pinned, tail streaming — the old swimming-gait render (stacked spheres = "Pokey") is gone.

## 🌙 OVERNIGHT PASS (Scott, 2026-07-02: "loop to fixup and beautify")
- [x] **Consistency/codex** v1.19.0 — (1) ALL 22 boons + 5 specials now have codex entries (ARTIFACTS shelf had one lonely loaf), with taken-counts, seen-triggers on pick, and history backfills; (2) **the MYSTERY EGG gacha was completely UNREACHABLE** — reels/jackpot fully built but the button was never drawn or hit-tested (lost in a refactor). Rewired on the duck-select screen: wobbling egg button + price, charges, spins, hatches.
- [x] **Unlock difficulty** v1.19.0 — legendary flotsam now ~1-in-90 spawns (was 1-in-22; codex filled in ~2 runs), tiered NOTICED thresholds (3/4/5 sightings; legends count from their 2nd — you don't forget a gnome), the EGG now APPRECIATES (+250 per hatch), and wearables gained a ★4 GILDED tier at 4x base cost (the hoard-drainer).
- [x] **New boons** v1.19.0 — POND KARMA (near misses pay LOFT + a feather), MIDNIGHT SNACK (golden-hour snacks tip a feather), PIED PIPER (every duckling brings a friend).
- [x] **Whimsy gameplay** v1.19.0 — SNACK COMBO: quick chains ring a rising scale, "x5!" pays a golden burst; skill tastes like music.
- [x] **KEEP-PLAYING hooks** v1.19.0 — death screen shows your NEXT UNLOCK with a live progress bar ("next: SOU'WESTER — 220 more") or "WAITING at the shop!" pulse; menu shows the LIFE LIST ("62% of the river known" — codex completion, birder-style); BIG DAY streaks ("4-day patrol!") tracked + shown on the card.
- [x] **Art fixups** (this pass + tonight's arc) — egg button art, gallop rebuild, anatomy pass, boss presentation all landed this cycle.

## 🌙🌙 FREE-REIN OVERNIGHT LOOP (Scott, 2026-07-02 night: "do not sit idle... sounds, literally everything... don't stop until usage runs out")
Worklist (work top-down, ship each when green, add findings):
- [x] SOUND v1.19.1 — SADIE BARKS now (synth two-syllable BORF, her own voice in every bubble); dedicated marimba COMBO note (pitch climbs the chain); and a real find: **thud.wav never existed** — Barry's log hurls, chuckit bounces + intro gestures were all silently no-op'ing. Synthesized + registered; full audit: every _sfx() call now maps to a real, loaded wav.
- [x] (folded into the sound item above)
- [x] Persona batches v1.19.2 — cautious 8-run batch exposed ambient-SADIE as the top killer (4/8); root cause: the bot never learned she's HOPPABLE. Hop response added: 4->1 deaths on the same seed. Reckless batch: 0/8 wins, deaths spread evenly (Chrissy/Sadie/bosses) — correct for a greed persona that ignores telegraphs; no game tuning warranted.
- [x] Audit — every remaining ❗/🟡 is Scott-gated (in-motion feel checks, Pike redesign sign-off, upper-ascension feel, #97/#104 boss-feel calls). Nothing closable solo remains.
- [x] Codex detail verified via new --codexshot v1.19.2 — lore card rendered but the hero circle was EMPTY for boons (detail resolver didn't know them); tex_boon now served. Specials show the ring-glyph (fine).
- [x] Perf sanity — additions since the v1.17.1 trim are all bounded (ribbon/tell/tears/combo floats: <25 draw cmds worst-case, gameplay-gated); headless mem 95MB. Real frame-rate word needs Scott's phone.
- [x] **The conga SINGS** v1.19.3 — WHIMSY §4 fulfilled: each duckling peeps a rising note as it pops up in sequence behind you; a clean run is a little song.
- [x] **Menu pond lives + killers attend funerals** v1.19.4 — menu: 48s dawn->dusk light cycle + drifting scenery under the title; death screen: your killer's portrait gloat-sways beside "bested by...". Verified via shots.
- [x] **Lake Cochichewick SINGS + SPARKLE WAKE** v1.19.5 — finale-biome hops chime up a pentatonic scale (WHIMSY §6 payoff); new 900-feather SPARKLE WAKE meta: hops trail stardust forever (flair sink).
- [x] **"again?" + bot leads Sadie** v1.19.6 — retry prompt is now the duck itself, hopeful eyes, asking "again?" (WHIMSY §9); bot hop-timing for ambient Sadie now LEADS her crossing (same-seed Sadie deaths 4->0).
- [x] **SADIE HAS HER OWN BOSS THEME** v1.19.7 — the only boss music in a HAPPY key: C major, 160 BPM, composed to feel like the biggest game of fetch ever played (gen_music.py, 12s seamless loop). Gerald keeps his dread; she gets joy.
- [x] **Gilded star gleams** v1.19.8 — the ★4 GILDED tier pulses gold in the wardrobe (it cost a hoard; it should look like it). Also verified: the EGG button correctly hides when no non-secret ducks remain locked (shot-mode cheat_unlock was hiding it in verification shots — real saves show it).
- [x] **Shop self-sizing** v1.19.9 — SPARKLE WAKE (perk #9) had wrapped into a third row and CRASHED through the SPECIALS header + tiles (fixed-y bands). All shop bands (specials header/grid, wardrobe + jukebox rows) now compute from row counts. Caught on my own shot sweep, same night it shipped.
- [x] **Sadie's collar fixed** v1.19.10 — the ring was placed on pre-rebuild geometry and pierced her throat; it now recolors the actual neck SURFACE voxels (wraps whatever shape she has, by construction), tag hanging from the front. All her art regenerated together. Verified in the wardrobe shot.
- [x] **Fetch repertoire** v1.19.10 — four acts, picked per play: CLASSIC (nose-out, play-bow, pounce, catch), SKY TOSS (flicks it high, coils, LEAPS to snag it), KEEP-AWAY (zoomies weave — you can't have it), THE DIG (drops it behind her, digs furiously with flying dust, pops up triumphant). 🟡 in-motion feel.
- [x] **Death screen decrowded** v1.19.11 — the "again?" invitation was colliding with the power tooltip + button row INSIDE the panel; it now floats on open water below, spoken by the actual dead duck sitting there (redundant portrait blit removed).
- [x] **Slowdowns** v1.19.11 — particle BUDGET (pile-ups recycle oldest at >140, never grow unbounded) + Scott's chosen MODERATE scenery cut (~half density, cap 9->6, banks 9->7 slots). Hero landmarks (next release) shift art weight to fewer, bigger pieces.
- [x] **HERO LANDMARKS** v1.20.0 — per Scott's consult (moderate density cut + shape left to me): ONE memorable set-piece per pond, drifting by every ~800ft as an event: Buker's half-sunken rowboat (oar adrift), Woodbury's dock end (checkered picnic basket + flexed rod to a bobber), Purgatory's huge dead tree (crow perched), Sand's listing striped buoy (gull atop), Pleasant's mossy two-tier fountain, Emerald's boulder with glowing mushrooms, Cochichewick's LOON on an aurora reflection. New tools/gen_heroes.py, 4 visual-iteration rounds, verified in-scene. Landmarks draw proud + opaque; small scenery stays sunk-translucent.
- [x] **Hero set-pieces naturalized** v1.20.1 — all landmarks now scenery-scale (rarity IS the landmark) and SHORE-anchored, leaning into the river like real pond things. The two theme-park pieces replaced: fountain -> a half-sunken log with THREE painted turtles sunning (necks up, red ear dashes); buoy -> a driftwood ROOT-BALL beached on a sandbar, the gull keeping its perch. Tree/rowboat/boulder/dock/loon kept, shrunk ~15%. Verified in-scene at Pleasant.
- [x] **PERSONAL POND THEMES** v1.20.2 — every arrival banner now carries Scott's line for that water; Buker opens at THE BOAT LAUNCH (aluminum skiff tied to the post); Woodbury keeps the turtle log on the big water; Purgatory stays shallow + weedy; SAND POND IS CAMP (pontoon boat hero, bonfire rings + barred owls on the banks, Sadie visits ~3x as often — camp dog's home water); Pleasant runs thick with minnows + an anchored skiff fishing by itself; Emerald went Colorado (pines over ferns) for the Mrs.; Cochichewick has Lizzie the beagle on the bank and the Weir Hill red-tail ALWAYS makes one pass over his own water. 🟡 all in-motion feels.

## 🌙🌙🌙 OVERNIGHT LOOP 2 (Scott, 2026-07-04: "find some other useful things")
- [x] --shotsweep v1.20.3 — one windowed run captures 9 key screens to /tmp/sweep_*.png (menu/select/shop/wardrobe/3 rivers/boss/death); all verified non-blank. Also found+fixed a --codexshot NAME COLLISION (my boon shot was shadowing the original dev mode; mine is now --boonshot).
- [x] Endless verified — events + forks already fire post-bread (only tutorial/boss/death gate them; Pike branch correctly filtered). No change needed.
- [x] --asc= sim arg + ASC-6 batch v1.20.3 — 0/8 wins but runs still reach 15-30k with deaths spread wide across causes; brutal but FAIR, no degenerate attack dominates. The ladder holds.
- [x] Micro-juice v1.20.3 — Sadie's chuckit SQUEAKS on its bounce (it IS a dog toy); the menu hero's outfit catches a passing glint every ~5s.
- [x] **Sadie: BEST GIRL wardrobe pass** v1.20.4 — (1) THE FULL FETCH: real throw into deep right field, full-gallop chase with kicked-up spray (her actual run frames, facing her travel), pounce, proud gallop home, skid-stop drop at your feet (3.4s act); SKY TOSS leaps higher; KEEP-AWAY is now two FULL-WIDTH zoomie laps; THE DIG pops up with a triumphant hop. (2) Bubble moved up-and-right, tail pointing back to her — off her head. (3) NEW: she has an OPINION about every wearable you equip ("arrr? ARRR!!", "trash bandit?!", "you can FLY?! take me with you!!") + a soft "aw." on doff, with a bark. 🟡 in-motion.
- [x] **Mobile death-screen white square FIXED** v1.20.4 — the killer portrait did a load() inside _draw(): fine on desktop, white square on the web export. Now resolved from boot-loaded textures via the codex resolver (the exact path gameplay already renders on phones).
- [x] **RUSTY RETHOUGHT** v1.21.0 (Scott: flyover annoying; wanted catered advice OR a minigame — built BOTH):
  (1) CATERED ADVICE — Rusty reads YOUR run before opening his beak: no shields past 800ft -> "flying BARE, are we?"; unused LOFT -> "that bar is a WEAPON"; zero near-misses -> "the river pays NERVE"; no ducklings, skipped snacks, hot combo praise. Generic pool only when nothing stands out.
  (2) RUSTY'S THERMALS — a rare no-risk/high-reward FORK branch: hazards truce (no logs/herons/Sadie/Chrissy), Rusty sweeps in to lead, golden hoops weave down the river — thread them for feathers+loft with a rising chain ("chain x5!"), misses just cool the thermal. At the course's end he coaches you with the catered line. 🟡 in-motion feel.
- [x] **Sadie run de-horrified** v1.21.1 — sadie_run_0..7 (wardrobe fetch + in-river chase) were still the OLD June swimming-gait renders; all 8 regenerated from the new model — the same source as the boss dash Scott called "far superior". Verified on sheet: continuous body, collar, tongue, clean 4-beat gallop.
- [x] **Forks breathable** v1.21.1 — on split: logs + herons CLEARED and neither respawns until you pick; scenery spawn paused (clean stage); current eases deeper (45%); wedge starts 120px further upstream. The choice is now actually choosable. 🟡 feel.
- [ ] **1x1 shoreline art + text per pond** — collaborative session, Scott drives.
- [x] **Sadie de-weinered** v1.21.2 — the run pose was a long-low fuselage with stub legs (dachshund geometry, verbatim "she looks like a weiner dog"). Rebuilt: SHORT back, DEEP lab chest, LONG 7-segment legs off a high shoulder line, haunch muscle. Boss + wardrobe + ambient all regenerated from the one pose.
- [x] **Version stamp mystery SOLVED** v1.21.2 — Settings showed a hand-maintained GAME_VERSION frozen at "1.16.11" (the comment literally said "keep in sync" — nobody did). Now release.sh sed-stamps the tag into the constant at every release; menu footer shows it too. Never hand-bump again.
- [x] **Rusty is IN YOUR HEAD** v1.21.2 — the advice now mines run HISTORY before this-run stats: three straight deaths to the same killer gets a specific coaching line ("she's HOPPABLE, duckling. i counted."), death-distances clustering within 800ft gets "you always sink near N ft — i've COUNTED", 4-run duck loyalty gets teased, upgrade ruts get called out, hoarding 2x the cheapest unlock gets "spend a little, scrooge-duck", Big Day streaks get respect. Never repeats the same read twice in a row. This-run tier + generic pool below that. 🟡
- [ ] 1x1 SHORELINE SESSION: Buker ✅ LOCKED as-is (Scott). Next up: Woodbury.
- [x] 1x1 SESSION · Woodbury LOCKED v1.21.3 — picnic gear NUKED; jetskis moored at the banks (red + teal, FLOATING w/ mooring post + rope after Scott's "jetskis don't sit on docks..."); line de-Tacoma'd to "the big water. all of it."
- [x] **THE SHORELINE codex** v1.21.3 (Scott: "can bank entities have records?") — new codex category: all 15 bank fixtures + 7 landmarks have named, lored records (Lizzie: "a professional."; the cow: "no explanation has ever been offered."), discovered by VISITING each pond (arrival + fork entry mark its fixtures seen; the cow only when her rare slot actually rolls). Icons + detail views wired; counts feed the LIFE LIST %.
- [x] 1x1 SESSION · Purgatory LOCKED v1.21.4 — gravestones removed; OSPREY roosting on a snag joins the dead-tree banks (white head, dark eye-stripe — the real field marks); codex record swapped grave->osprey.
- [x] 1x1 SESSION · Sand LOCKED v1.21.5 — camp untouched per Scott + THE CAMP DOCK: a long straight orange-brown dock drifts by (~once per Sand visit); Sadie spots the end board (bark), sprints the full runup at a gallop, LEAPS with a tucking spin, SPLOOSH! + ripples, gone swimming. Codex: "the end board is worn smooth. you know why." 🟡 in-motion.
- [x] 1x1 SESSION · Pleasant LOCKED v1.21.6 — lamppost evicted ("that is weird"); two shore-side ANGLERS on the banks: one mid-cast (orange vest, dashed line out), one hunched on an overturned bucket. Codex records for both.
- [x] 1x1 SESSION · Emerald + Cochichewick LOCKED v1.21.7 — Emerald as-is; Cochichewick's LOON landmark nixed (Scott) — the birding water carries itself with Lizzie + the Weir Hill red-tail; codex record removed so the life list stays completable. 🏁 SHORELINE TOUR COMPLETE: all 7 ponds Scott-approved.
- [x] **THE TRUE CHAIN** v1.21.8 (Scott + tacomalakes.org) — JIMMY POND added as the 7th water (quiet coves, cattail banks, calm bed, no landmark until Scott themes it); PLEASANT REMOVED entirely (not a Tacoma lake — anglers/skiff art parked on disk, unwired); name stays "Purgatory Pond" per Scott. Final roster: Buker · Woodbury · Purgatory · Sand · Emerald · Cochichewick · Jimmy. All theme-indexed tables re-cut; Cochichewick checks reindexed (hawk pass + hop-chimes now theme 5); atmospheres remapped; zero script errors in regression.
- [x] **Jimmy = good fishin'** v1.21.9 — Pleasant's parked kit found its true home: shore anglers on Jimmy's banks, the anchored skiff as its landmark, minnows running triple, line "good fishin'. the quiet kind." Codex records restored under Jimmy.
- [x] **Codex detail views fixed** v1.21.9 — the detail resolver only knew characters/boons/shoreline; SNACKS, RIVER TRASH, WEARABLES and POWER-UPS all showed empty circles in their detail pages. Resolver now serves every shelf (snacks->item sprite, trash->flotsam sprite, wearables->shop icon, powers->the boon icon sheet).
- [x] Confirmed: Pleasant fully excised (zero references) — Scott's sighting was a cached web bundle; hard refresh.
- [x] **Deep lore pass, POWER-UPS** v1.21.10 — all 28 upgrades now carry river mythos in their codex pages (samples sent to Scott for redlines); the draft-card text rides below as a footnote.
- [x] **THERMALS dev button** v1.21.10 — dev menu drops you straight into Rusty's course mid-run (Rusty icon), for fast feedback.
- [x] **Zoomies = the POUNCE** v1.21.11 — Scott's call: her best sprite (mid-air pounce) rotated nose-down into travel, and the crossing is now THREE BOUNDS instead of a flat slide. The "poeky run" is gone from the fight.
- [x] **Sides reeled in + cow faces the water** v1.21.12 — bank slots 7->4 (each side ~every 580px now), accent pieces rarer; side-facing props (cow/Lizzie/anglers/jetskis/owl) MIRROR on the right bank so they watch the river, not the woods.
- [x] **Pond order SHUFFLES per run** v1.21.12 (Scott: "always the same order?") — it was; now Buker always opens (every trip starts at the launch) and the remaining six shuffle per run. Big Day seeds the day's route. Forks stay compatible via route-position sync.
- [x] **Golden hour HALVED** v1.21.12 — wife's verdict: haze/sun too distracting. Gradient/glow/rays all ~50%, one fewer layer each.
- [x] **Cameo pile-up ended** v1.21.12 — "turtle + Chrissy + herons + Sadie at once": new stage manager — only ONE major ambient character at a time (Sadie/Chrissy/turtle mutually exclusive), airborne herons capped at 2 outside boss fights.
- [x] **Mario stomp flair + hurt indicator** v1.21.13 — every stomp (heron, snapping turtle, all bosses) now: BOUNCES you back up off the target, rings a double shock-ripple (white inner ring), and REVERBERATES — two decaying sfx echoes trail the hit. Getting tagged (shield pop, duckling loss, any boss hit) breathes a tasteful RED edge pulse in from the screen borders — never a full flash, halved under reduce-flash. 🟡 feel.
- [x] **Dock jump REMOVED** v1.21.14 — "nightmare fuel," gone entirely (art parked on disk).
- [x] **Sides cut AGAIN** v1.21.14 — bank slots 4->2 (ONE piece per side per screen), water scenery cap 4 + slower stream. Also: the rivershot harness was pre-seeding 16 pieces regardless of live caps — density shots LIED; now seeds 6.
- [x] **Rusty's no-show ROOT-CAUSED** v1.21.14 — he's hard-gated to <1000 ft; the Thermals (3.6k+) and the Weir Hill pass have been silently DEAD since birth. New hawk_summon override + when the Thermals start he sweeps in IMMEDIATELY with the course briefing ("thread the GOLD RINGS — each one pays. CHAINS pay more. FLY!"), hoop hits float "+N", and his sendoff carries your tally ("12 of 15 rings!"). 🟡 needs Scott's re-verdict on the game itself.
- [x] **The duck FLASHES RED when hurt** v1.21.14 (Scott's ask; edge pulse alone unobserved — most hits kill instantly, only shield/duckling saves show it) — red strobe on the duck sprite itself, plus the edges.
- [x] **Codex icons were specks — FIXED** v1.21.24 (Scott: "lots of codex entries missing their turntable icons") — audited every list section with a new 8-depth codex screenshot sweep (now part of --codexshot): nothing was truly missing, but all 19 DUCK rows + the boss/enemy/friend rows blitted their raw sprite CANVASES, whose fat transparent margins shrank the actual pixels to near-invisible specks (a 64px canvas holds a ~26px duck → drawn ~14px). New opaque-pixel fitting (_tex_used_rect cache + _blit_fit crops the margins and fills the icon box, capped 3x upscale) — every duck/char icon now fills its box and reads at a glance. 🟡 eyeball the codex list.
- [x] **Power-up cadence thinned** v1.21.23 (Scott: "powerups are dished out far too often") — mid-run draft marks widened: first draft ~600m (was 400m), gaps grow ×1.32 per draft (was ×1.25). Net: ~10 drafts across a full campaign instead of ~13, and 4–5 before the first boss instead of 6. Minimap draft pips use the same formula (kept in sync). Balance-checked like-for-like on the cautious bot (seed 11 + thermals): old cadence 2/2 campaign wins → new 1/2, the win a clean 0-hit run — harder but fair, which matches your standing "waltz through" complaint. Boss boards, shrine, and thermals rewards untouched (those are earned). 🟡 feel.
- [x] **Rusty codex turntable rescued** v1.21.22 — the playable-Rusty sprite set silently OVERWROTE the codex guide turntable (both lived at rusty_spin_*); the compendium's classic big glide turntable now lives at rustyguide_spin_* (all three codex lookup maps updated), and the playable set keeps rusty_spin_* for duck-select. voxel_duck.py regen writes the right names going forward.
- [x] **Mid-Thermals power-up interruption KILLED** v1.21.21 (Scott: "I was just stopped for a power-up mid trial... bad") — the course start already pushed the 400m draft mark past the course end, but SOMETHING still re-armed it; now the roguelike draft is HARD-GATED: it can never open while stretch_mod == "rusty", full stop. It fires right after the course instead.
- [x] **THERMALS intro made helpful** v1.21.21 (Scott: "still start too abruptly without any helpful intro") — a proper INTRO CARD now holds center screen through the whole run-up: "RUSTY'S THERMALS / shadow his GOLDEN slipstream / hold the line: 90% pays a LEGENDARY / grading starts at FLY!", with BIG pulsing runway digits (3·2·1) replacing the easy-to-miss banner flashes. You get ~8s of reading + positioning before a single tick is graded.
- [x] **100% = RUSTY IS PLAYABLE** v1.21.21 (Scott: "anything special for a 100%? unlock Rusty as a playable character? lol" — not a joke anymore) — fly his course at 99%+ and he hands over his wings: full playable-species sprite set rendered from his own voxel model (tools/gen_rusty_duck.py — back-view GLIDE instead of paddling, real wingbeat hops, fierce face close-up, 24-frame turntable + flap set, mega-hop voxel stack). Secret roster slot ("fly his thermals PERFECT to earn his wings"), stats 0.92 hop / 0.88 steer / 0.88 pace / 0.95 size, and he does not quack — he SCREECHES. Unlock sendoff: "a TRUE PERFECT?! that settles it, kid — from now on you can fly as ME." Roster grid auto-reflows to 19. 🟡 the earn itself is brutal by design.
- [x] **THERMALS: fair rewards + countdown + trail reads + nicer Rusty** v1.21.20 (Scott: "got 80% and still got a legendary which feels wrong... visual indicator that I'm on the trail... start is very abrupt... rusty is kind of a jerk calling me a dweeb... some 3.2.1 is warranted") — (1) REWARD BUG: the 70–89% tier dealt from a "rarity ≥2" pool that LEAKED LEGENDARIES; new exact-tier dealer — 90%+ = board of PURE legendaries (better than before: all 3), 70–89% = epics exactly, never legendary. (2) 3··2··1··FLY! countdown after his briefing — grading doesn't start until FLY! (rising chimes, banner flashes); course lengthened to ~28s wall-clock wherever it starts (was shrinking at high run speed). (3) ON-TRAIL: gold aura ring + golden sparkle wake peeling off the duck; OFF-TRAIL: pulsing gold chevrons point from the duck back to the line. (4) TONE: "dweeb" retired — "SHADOW ME, kid", "HOLD it, ace!", and the low-grade line is now encouraging ("every great wing started somewhere"). Also flotsam gated off the course (junk builds would magnet trash mid-minigame). 🟡 verdict.
- [x] **Trash power-ups couldn't collect trash — FIXED** v1.21.19 (Scott: "trash related power-ups that don't actually allow me to collect trash?") — root cause: flotsam only ever spawned GLUED TO THE BANKS (16–52px off the grass) while the magnet radius was 165px with a pull SLOWER than the river — from mid-river the math made grabs impossible; the boons only worked if you rode the bank edge. Now: with any junk boon drafted (TRASH MAGNET / PACK RAT / JUNK SLINGER), flotsam floats the WHOLE river reachable; TRASH MAGNET specifically gets a real 330px bank-to-bank radius + a pull faster than the current, so trash genuinely drifts to your lane like the card says. 🟡 feel-check on a junk build.
- [x] **THERMALS made an actual CHALLENGE** v1.21.18 (Scott: "WAY too easy... should turn off other in-game things... rusty should face away as he leads... ramp up the difficulty for it to be worth a legendary") — (1) HARD TRUCE: the course now shuts off EVERYTHING — snacks, trash, herons, river events, mid-run draft cards (pushed past the course), logs; also killed a sneaky old "while Rusty is on screen, rain snacks" branch that was flooding the course. Pure: you, him, the line. (2) DIFFICULTY: a third fast juke-wave fades in as the course runs (it gets nastier the deeper you fly), scoring band tightened ±34→±26px (ribbon redrawn to match), his slipstream PULLS you 25% faster, and the course is ~2x longer so the grade is earned over ~20s. Bot calibration: a near-perfect tracker now lands 88–93% — the legendary (90%) sits right at the edge of humanly-possible; skilled-persona wobble drops to 68–88%. (3) He FACES AWAY: new hawk_lead_0-2 back-view voxel renders (tail to camera), banking into his own weave, wheeling around to face you only for the grade. HUD meter moved below his flight line. 🟡 verdict.
- [x] **Wardrobe Sadie dash de-janked** v1.21.17 (Scott: "sadies dash in the wardrobe looking jank af") — the shop fetches were STILL running the old gallop frames (the "scariest thing I've ever seen" animation, surviving in one last place). All three running moves (fetch chase, proud return, keep-away laps) now use the boss-zoomies treatment: her POUNCE pose rotated nose-down into three flying bounds. New --wardrobeshot --fetch=chase|return|lap harness froze her mid-run for verification — both directions eyeballed. 🟡 in-motion feel.
- [x] **THERMALS "no minigame" FIXED** v1.21.16 (Scott: "I feel like I rolled up on Rusty in place of a boss and there was no minigame?") — root-caused with a new --thermalshot harness + --thermals botsim flag. THREE compounding failures: (1) the briefing Rusty flew OFF ~10s in, while a second confusing Rusty sprite sat at the ribbon head — now ONE Rusty who personally flies the course head the whole way (banks his own weave, cheers when you lock in); (2) the graded sendoff was delivered to a hawk that had already LEFT — below 70% the course just silently stopped = "no minigame"; now he's still there, hovers, says your grade to your face ("RUSTY'S GRADE: N%" flash too), THEN departs; (3) Rusty on-screen blocks boss spawns, so near a boss mark it read as "Rusty instead of my boss" — he now holds the course together and the boss arrives right after. Also: ribbon brightened + widened to EXACTLY the ±34px scoring band, and a live HUD meter ("HOLD HIS LINE / IN THE STREAM N%" with a gold notch at the 90% legendary mark). Bot now shadows the line by persona — cautious flew 93–100%, drafted legendaries, and WON two full campaigns. 🟡 re-verdict.
- [x] **THERMALS 2.0 — total rebuild** v1.21.15 (Scott: "incredibly dumb and easy… a minigame should feel like a novel distinct thing and have some meaningful reward if executed well") — hoops are GONE. Now a SLIPSTREAM-TRACKING game: Rusty flies the course ahead of you, weaving a live golden ribbon down the river (two stacked sine weaves — wide + quick — so his line genuinely snakes); you hold his wake. Graded 10x/sec while in the stream: rising combo hum, +feathers as you hold it, gold aura on the duck when you're locked in. SENDOFF IS GRADED: ≥90% = "PERFECT WING" +60 feathers **+ a 3-card LEGENDARY draft**; ≥70% = +30 + 2-card legendary pick; below = +10 and coaching. New briefing: "SHADOW ME, dweeb — stay in my SLIPSTREAM! fly it near-PERFECT and i'll deal you something LEGENDARY." 🟡 needs Scott's verdict — dev menu THERMALS button drops you straight in.
- [x] **WARP: NEXT POND dev button** v1.21.15 — dev menu jumps you past the next pond boundary (landmark arrives quick); tap repeatedly to cycle all 7 waters.
- [x] **Duckling-loss red flash MISSED** v1.21.15 (Scott: "I didn't flash red when I lost a duckling I don't think") — the flash WAS firing (every loss path routes through _ouch()) but died in ~0.3s. Now: stronger (1.1), slower decay (1.5/s → ~0.7s visible), strobe slowed 30→16Hz so eyes can track it. 🟡 feel.
- [x] **×pace HUD retired** v1.21.14 — read as leftover telemetry, and its per-run reset wasn't obvious. Stat still logs to the LOGBOOK.
