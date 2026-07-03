#!/usr/bin/env python3
"""
Pulls Sabinaya's MyAnimeList anime list server-side (no browser CORS issues)
and writes it to data/anime.json for the static site to read.

Runs from a GitHub Action, not from the browser -- so MAL's anti-bot layer
doesn't see it as a client-side scraper the way it sees Jikan requests.
"""
import json
import sys
import time
import urllib.request
import urllib.error

USERNAME = "Sabinaya_Sapkota"
OUT_PATH = "data/anime.json"

STATUS_MAP = {1: "watching", 2: "completed", 3: "on_hold", 4: "dropped", 6: "plan_to_watch"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": f"https://myanimelist.net/animelist/{USERNAME}",
}


def fetch_status(status_code, offset=0):
    url = f"https://myanimelist.net/animelist/{USERNAME}/load.json?status={status_code}&offset={offset}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_all():
    all_entries = []
    for status_code in STATUS_MAP:
        offset = 0
        while True:
            try:
                batch = fetch_status(status_code, offset)
            except urllib.error.HTTPError as e:
                print(f"HTTPError {e.code} for status={status_code} offset={offset}: {e.read()[:300]}", file=sys.stderr)
                break
            except urllib.error.URLError as e:
                print(f"URLError for status={status_code} offset={offset}: {e}", file=sys.stderr)
                break

            if not batch:
                break

            all_entries.extend(batch)

            if len(batch) < 300:
                break
            offset += 300
            time.sleep(1)  # be polite, mirror browser pacing

        time.sleep(1)

    return all_entries


def normalize(entry):
    status_id = entry.get("status")
    image_path = entry.get("anime_image_path") or ""
    if image_path and not image_path.startswith("http"):
        image_path = "https://cdn.myanimelist.net" + image_path

    anime_url = entry.get("anime_url") or ""
    if anime_url and not anime_url.startswith("http"):
        anime_url = "https://myanimelist.net" + anime_url

    return {
        "id": entry.get("anime_id"),
        "title": entry.get("anime_title"),
        "image": image_path,
        "url": anime_url,
        "status": STATUS_MAP.get(status_id, "unknown"),
        "score": entry.get("score", 0),
        "episodes_watched": entry.get("num_watched_episodes", 0),
        "episodes_total": entry.get("anime_num_episodes", 0),
    }


def main():
    raw = fetch_all()
    if not raw:
        print("Fetched 0 entries -- refusing to overwrite existing data/anime.json", file=sys.stderr)
        sys.exit(1)

    entries = [normalize(e) for e in raw]
    # de-dupe by anime id just in case a status changed mid-run
    seen = {}
    for e in entries:
        seen[e["id"]] = e
    entries = list(seen.values())

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"updated_at": int(time.time()), "entries": entries}, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(entries)} entries to {OUT_PATH}")


if __name__ == "__main__":
    main()
