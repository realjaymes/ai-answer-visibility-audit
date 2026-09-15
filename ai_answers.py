"""Ask a web-searching AI model the top engineer questions and record who it cites.

Uses the OpenAI Codex CLI with live web search (`codex --search exec`), a proxy for
what ChatGPT-style assistants return. Writes data/ai_answers.json.
"""
import json, re, subprocess, sys, tempfile, os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from config import BRAND

PROMPT = """An engineer asks you: "{q}"
Search the web and answer as a helpful assistant would, in 3-5 sentences, naming any specific companies, services or tools you would point them to.
Then output one final line of JSON only, in this exact shape:
{{"companies": ["<company or tool names you mentioned>"], "sources": ["<every URL you relied on>"]}}"""

def ask(q):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        out = f.name
    cmd = ["codex", "--search", "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--color", "never",
           "-C", tempfile.gettempdir(), "--output-last-message", out, PROMPT.format(q=q)]
    try:
        subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=420)
        txt = open(out).read()
    except Exception as e:
        return {"question": q, "error": str(e)}
    finally:
        pass
    body, _, last = txt.rstrip().rpartition("\n")
    start = last.find("{")
    try:
        d = json.loads(last[start:])
        d.setdefault("answer", body.strip())
    except Exception:
        d = {"companies": [], "sources": re.findall(r"https?://[^\s)\]\"']+", txt)}
    if not d.get("answer"):
        d["answer"] = body.strip() or txt
    d["question"] = q
    d["domains"] = sorted({urlparse(s).netloc.replace("www.", "") for s in d.get("sources", []) if s.startswith("http")})
    blob = (json.dumps(d)).lower()
    d["brand_mentioned"] = BRAND["name"].lower() in blob or any(x in blob for x in BRAND["domains"])
    return d

if __name__ == "__main__":
    questions = json.load(open("data/ai_questions.json"))
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(ask, [q["question"] for q in questions]))
    for q, r in zip(questions, results):
        r["theme"] = q["theme"]
    json.dump(results, open("data/ai_answers.json", "w"), indent=2)
    print(sum(1 for r in results if r.get("brand_mentioned")), "of", len(results), "answers mention the brand")
