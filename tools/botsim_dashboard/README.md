# DUCKODUCKO Bot-Sim Dashboard

A throwaway **Grafana sidecar** that turns the headless bot-sim's metrics into pretty pictures —
death-cause breakdowns, distance distributions, and which power-ups the AI duck actually drafts.

No database: Grafana's [Infinity datasource](https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/)
reads `data/botsim_report.json` directly (served by a tiny nginx sidecar).

## 1. Generate a report

From the **repo root** (not this folder):

```bash
# a chunky batch makes nicer charts
godot --headless --path . -- --botsim --runs=30 --persona=skilled
# personas: skilled | cautious | reckless     drop into one boss: --boss=0|1|2
```

That writes `tools/botsim_dashboard/data/botsim_report.json`.

## 2. Bring up Grafana

```bash
cd tools/botsim_dashboard
docker compose up -d
open http://localhost:3001          # sign in: admin / admin
```

The **DUCKODUCKO Bot-Sim** dashboard is auto-provisioned. It auto-refreshes every 10s, so just
re-run the sim and the panels update (hit the nginx report fresh).

```bash
docker compose down                 # when you're done
```

## What's in the report

| section   | shape | feeds |
|-----------|-------|-------|
| `summary` | object | the KPI stat row (runs / median / mean / best dist / wins) |
| `deaths`  | `[{cause, count, pct}]` | the "Death causes" bar chart |
| `ups`     | `[{id, count}]` | the "Power-ups taken" bar chart |
| `runs`    | `[{species, dist_m, dur_s, death, bosses, hits, ups, boons}]` | the per-run table |

Death `cause` strings come straight from the game's `die(cat)` taxonomy
(`gerald` / `snapz` / `donny` / `sadie` / `log` / `heron` / `turtle` / …), so a spike in any one
column is a real "this thing is a wall" signal.

## Notes
- The Infinity datasource fetches **server-side** via Grafana's proxy, so the internal `fileserver`
  hostname works and there are no CORS issues.
- Panels use Infinity's `backend` parser with `root_selector` + `columns`. If a panel shows "No data"
  after a Grafana version bump, open it and re-pick the parser — the JSON shape is stable.
