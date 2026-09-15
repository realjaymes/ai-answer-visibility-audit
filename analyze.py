"""Group collected questions into Arcessio's decision themes and rank them by real engagement.

Reads data/suggest.json and data/reddit.json. Writes data/themes.json and
data/ai_question_candidates.json (top question-style titles per theme, for editorial
selection into data/ai_questions.json before running ai_answers.py).
"""
import json, re
from collections import defaultdict
from config import THEMES

# Queries about buying a machine, careers, or unrelated meanings of the seed words.
EXCLUDE = re.compile(r"machine cost for woodworking|in india|in south africa|in ethiopia|school|smell|experience|"
                     r"find customers|get jobs|get machine shop work|sell a machine shop|part number|router|"
                     r"dying trade|what machines are|how to score|design a checklist|transportation|"
                     r"cnc machines cost|good cnc machine cost|shop rate|charge for|job|hiring|salary|resume|career",
                     re.I)

def theme_of(text):
    t = text.lower()
    for theme, keys in THEMES.items():
        if any(k in t for k in keys):
            return theme
    return None

def main():
    suggest = json.load(open("data/suggest.json"))
    reddit = json.load(open("data/reddit.json"))
    themes = defaultdict(lambda: {"search_queries": [], "reddit_posts": [], "reddit_comments": 0, "reddit_score": 0})
    for seed, queries in suggest.items():
        for q in queries:
            if EXCLUDE.search(q):
                continue
            th = theme_of(q) or theme_of(seed)
            if th:
                themes[th]["search_queries"].append(q)
    for p in reddit:
        if EXCLUDE.search(p["title"]):
            continue
        th = theme_of(p["title"])
        if th:
            t = themes[th]
            t["reddit_posts"].append(p)
            t["reddit_comments"] += p["comments"]
            t["reddit_score"] += p["score"]
    ranked = []
    candidates = []
    for th, t in themes.items():
        t["search_queries"] = sorted(set(t["search_queries"]))
        t["reddit_posts"].sort(key=lambda p: -(p["comments"] + p["score"]))
        ranked.append({"theme": th, "search_query_count": len(t["search_queries"]),
                       "reddit_post_count": len(t["reddit_posts"]), "reddit_comments": t["reddit_comments"],
                       "reddit_score": t["reddit_score"], "top_search_queries": t["search_queries"][:15],
                       "top_reddit_posts": t["reddit_posts"][:15]})
        qs = [p for p in t["reddit_posts"] if "?" in p["title"]][:8]
        candidates += [{"theme": th, "question": p["title"], "comments": p["comments"], "url": p["url"]} for p in qs]
    ranked.sort(key=lambda r: -(r["reddit_comments"] + 5 * r["search_query_count"]))
    json.dump(ranked, open("data/themes.json", "w"), indent=2)
    json.dump(candidates, open("data/ai_question_candidates.json", "w"), indent=2)
    for r in ranked:
        print(f'{r["theme"]:28} posts={r["reddit_post_count"]:4} comments={r["reddit_comments"]:6} queries={r["search_query_count"]}')

if __name__ == "__main__":
    main()
