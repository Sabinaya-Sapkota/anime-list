🎴 My Anime List
A live, auto-updating anime tracker card gallery — pulled straight from MyAnimeList and rendered as a clean, filterable card grid.
Live site: sabinaya-sapkota.github.io/anime-list
![status](https://img.shields.io/badge/status-active-brightgreen) ![auto--sync](https://img.shields.io/badge/data-auto--synced%20daily-f60b0b)
---
What this is
A single-page site that displays an anime list as a card gallery — poster, title, watch status, episode progress, and score — with tabs to filter by All / Watching / Completed / On Hold / Dropped / Plan to Watch. Each card links straight to the anime's MyAnimeList page.
Instead of calling a third-party API from the browser every time someone visits (which is slow, rate-limited, and breaks whenever MyAnimeList changes something), this project fetches the list once a day in the background and commits it as a small JSON file. The site just reads that file — fast, reliable, no external dependency at page-load.
How it works
```
┌───────────────────────┐   daily cron    ┌──────────────────────┐   static fetch    ┌────────────┐
│  MyAnimeList profile   │ ─────────────▶  │  GitHub Action        │ ────────────────▶ │ index.html │
│  (source of truth)     │ fetch_anime.py  │  → data/anime.json    │                   │ (the site) │
└───────────────────────┘                  └──────────────────────┘                   └────────────┘
```
`scripts/fetch_anime.py` — runs on GitHub's servers, pulls the anime list, normalizes it, writes `data/anime.json`
`.github/workflows/update-anime.yml` — triggers the script daily (and on-demand via the Actions tab)
`index.html` — reads `data/anime.json` and renders the cards; no build step, no framework
Tech stack
Vanilla HTML / CSS / JS (no frameworks, no build tools)
Bootstrap Icons for iconography
Python 3 (standard library only — no dependencies to install) for the sync script
GitHub Actions for scheduling
GitHub Pages for hosting
Running your own copy
Want to point this at your own MyAnimeList profile?
Fork this repo.
In `scripts/fetch_anime.py`, change `USERNAME = "Sabinaya_Sapkota"` to your MAL username.
In `index.html`, update the `USERNAME` constant near the top of the `<script>` block to match.
Make sure your MAL list is public: MyAnimeList → Edit Profile → Privacy → Anime List set to public.
In your fork's Settings → Pages, set source to "Deploy from a branch" → `main` → `/ (root)`.
In the Actions tab, run the Update anime list workflow manually once to generate your first `data/anime.json`.
Visit your new `https://<your-username>.github.io/<repo-name>/`.
After that, it keeps itself in sync automatically once a day — no maintenance needed.
Project structure
```
.
├── index.html                       # the site
├── data/
│   └── anime.json                   # auto-generated snapshot of the anime list
├── scripts/
│   └── fetch_anime.py               # pulls + normalizes list data
└── .github/workflows/
    └── update-anime.yml             # daily scheduled sync
```
Notes
Data updates once every 24 hours, not in real time — recent status changes on MyAnimeList may take up to a day to appear here.
If a sync run ever fails (MyAnimeList rate-limits are the usual culprit), the site just keeps showing the last successful snapshot rather than going blank.
---
Built by Sabinaya Sapkota · Portfolio · MyAnimeList
