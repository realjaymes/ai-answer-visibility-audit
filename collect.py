"""Collect real engineer questions from Google autocomplete and the Reddit archive (Arctic Shift).

Pure standard library. Writes data/suggest.json and data/reddit.json.
"""
import json, time, urllib.parse, urllib.request
from config import SUGGEST_SEEDS, SUBREDDITS, REDDIT_TITLE_TERMS, REDDIT_AFTER

UA = {"User-Agent": "engineer-question-audit/0.1 (research; contact james@marketinginaction.xyz)"}

def get_json(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
                d = json.loads(r.read().decode("utf-8", "replace"))
            if isinstance(d, dict) and d.get("error"):
                raise RuntimeError(d["error"])
            return d
        except Exception as e:
            time.sleep(20 * (i + 1))
    return None

def collect_suggest():
    out = {}
    prefixes = ["", "how ", "why ", "best ", "vs "]
    for seed in SUGGEST_SEEDS:
        found = set()
        for p in prefixes:
            q = (p + seed) if p != "vs " else (seed + " vs")
            d = get_json("https://suggestqueries.google.com/complete/search?client=firefox&q=" + urllib.parse.quote(q))
            if d and len(d) > 1:
                found.update(d[1])
            time.sleep(0.4)
        out[seed] = sorted(found)
    return out

def collect_reddit():
    posts = {}
    for sub in SUBREDDITS:
        for term in REDDIT_TITLE_TERMS:
            url = ("https://arctic-shift.photon-reddit.com/api/posts/search?" +
                   urllib.parse.urlencode({"subreddit": sub, "title": term, "after": REDDIT_AFTER, "limit": 100}))
            d = get_json(url)
            for p in (d or {}).get("data") or []:
                if p.get("removed_by_category") or (p.get("_meta") or {}).get("removal_type"):
                    continue
                posts[p["id"]] = {
                    "id": p["id"], "subreddit": p.get("subreddit"), "title": p.get("title", ""),
                    "score": p.get("score", 0) or 0, "comments": p.get("num_comments", 0) or 0,
                    "created_utc": p.get("created_utc"), "url": "https://www.reddit.com" + p.get("permalink", ""),
                    "term": term,
                }
            print(sub, term, "posts so far:", len(posts), flush=True)
            json.dump(sorted(posts.values(), key=lambda p: -(p["comments"] + p["score"])), open("data/reddit.partial.json", "w"))
            time.sleep(8)
    return sorted(posts.values(), key=lambda p: -(p["comments"] + p["score"]))

if __name__ == "__main__":
    import os, sys
    if "--reddit-only" not in sys.argv or not os.path.exists("data/suggest.json"):
        s = collect_suggest(); json.dump(s, open("data/suggest.json", "w"), indent=2)
        print("suggest queries:", sum(len(v) for v in s.values()))
    r = collect_reddit(); json.dump(r, open("data/reddit.json", "w"), indent=2)
    print("reddit posts:", len(r))
