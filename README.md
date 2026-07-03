# My Anime List page

`index.html` renders anime cards from `data/anime.json`. That JSON file is
generated automatically once a day by `.github/workflows/update-anime.yml`,
which runs `scripts/fetch_anime.py` on GitHub's servers and commits the
result — so the browser never has to talk to MyAnimeList or a third-party
scraper directly (no CORS issues, no rate limits, no "list isn't public"
false negatives).

## First-time setup

1. Push this to your repo (or drop these files into your existing portfolio repo).
2. Go to the repo's **Actions** tab → **Update anime list** → **Run workflow**
   to trigger the first sync manually (don't wait for the daily 06:00 UTC cron).
3. Once it finishes, `data/anime.json` will be committed with your real list,
   and the page will pick it up on next load.

## If the Action fails

Check the Action's log. Two likely causes:
- MAL blocked the GitHub runner's IP for that run — re-run it, this is usually transient.
- Your list privacy is genuinely restricted. Check
  MAL → Edit Profile → Privacy → make sure "Anime List" (separate from your
  overall profile) is set to public.

## Updating the username

Change `USERNAME` in both `scripts/fetch_anime.py` and the `USERNAME` constant
in `index.html`'s script.
