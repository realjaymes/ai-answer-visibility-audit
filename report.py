"""Summarize the audit into data/summary.json and output/report.md."""
import json
from collections import Counter
from config import BRAND

def main():
    ans = json.load(open("data/ai_answers.json"))
    site = json.load(open("data/site_check.json"))
    suggest = json.load(open("data/suggest.json"))
    doms, cos = Counter(), Counter()
    for a in ans:
        doms.update(set(a.get("domains", [])))
        cos.update({c.split(" Instant")[0].split(" ProDesk")[0].strip() for c in a.get("companies", [])})
    summary = {
        "questions_asked": len(ans),
        "brand_mentions": sum(1 for a in ans if a.get("brand_mentioned")),
        "top_cited_domains": doms.most_common(10),
        "top_named_companies": cos.most_common(10),
        "autocomplete_seeds": len(suggest),
        "autocomplete_queries": sum(len(v) for v in suggest.values()),
        "pages_checked": len(site),
        "pages_under_25_raw_words": sum(1 for s in site if s["raw_words"] < 25),
        "raw_words_total": sum(s["raw_words"] for s in site),
        "rendered_words_total": sum(s["rendered_words"] for s in site),
    }
    json.dump(summary, open("data/summary.json", "w"), indent=2)
    lines = [f"# AI visibility audit: {BRAND['name']}", "", "```", json.dumps(summary, indent=2), "```", ""]
    for a in ans:
        lines += [f"## {a['question']}", f"Theme: {a.get('theme')}", "", a.get("answer", ""), "",
                  "Companies: " + ", ".join(a.get("companies", [])), "Sources: " + ", ".join(a.get("sources", [])), ""]
    open("output/report.md", "w").write("\n".join(lines))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
