"""Compare what a non-JavaScript crawler sees on a site versus a rendered browser.

Most AI answer-engine crawlers fetch raw HTML without running JavaScript, so a
client-rendered site can look nearly empty to them. Writes data/site_check.json.
"""
import json, re, html, subprocess, sys, urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def words(h):
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return len(re.sub(r"\s+", " ", t).split())

def raw(url, ua="GPTBot"):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

def rendered(url):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000", "--dump-dom", url],
                          capture_output=True, text=True, timeout=90).stdout

def sitemap_urls(sitemap):
    return re.findall(r"<loc>([^<]+)</loc>", raw(sitemap, "Mozilla/5.0"))

if __name__ == "__main__":
    sitemap = sys.argv[1] if len(sys.argv) > 1 else "https://arcessio.ai/sitemap.xml"
    rows = []
    for u in sitemap_urls(sitemap):
        if "/careers" in u:
            continue
        r, d = raw(u), rendered(u)
        title = (re.findall(r"<title>([^<]*)</title>", r) or [""])[0]
        rows.append({"url": u, "title": title, "raw_words": words(r), "rendered_words": words(d)})
        print(rows[-1])
    json.dump(rows, open("data/site_check.json", "w"), indent=2)
