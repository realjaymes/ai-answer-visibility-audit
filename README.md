# Engineer Question & AI Visibility Audit

Checks whether a company shows up when its buyers ask AI assistants their real questions, and whether AI crawlers can read its site.

1. `collect.py` pulls real queries from Google autocomplete (and Reddit via the Arctic Shift archive, which rate-limits heavily).
2. `ai_answers.py` asks a web-searching OpenAI model (`codex --search exec`) each question in `data/ai_questions.json` and records named companies, sources and brand mentions.
3. `site_check.py <sitemap>` compares words a non-JavaScript crawler sees against a rendered browser, per sitemap page.
4. `analyze.py` groups collected questions into decision themes; `report.py` writes `data/summary.json` and `output/report.md`.

Configure themes, seeds, subreddits and brand in `config.py`. Standard-library Python; needs the Codex CLI and Google Chrome.

First run: Arcessio, 2026-09-15.
