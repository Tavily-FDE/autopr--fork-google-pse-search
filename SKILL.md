---
name: google-pse-search
description: >
  Web search skill powered by Google PSE (Programmable Search Engine) API
  with optional Tavily search as a parallel/fallback provider.
  Primary search tool for all web queries — Korean and English alike.
  Better search quality than DuckDuckGo, especially for Korean content.
  Triggers: "search for", "find", "look up", news/current events, recent info,
  date-filtered searches, site-specific searches, any general web search request.
  Requires environment variables: GOOGLE_PSE_KEY, GOOGLE_CX_ID.
  Optional: TAVILY_API_KEY (enables --provider tavily and --provider auto fallback).
  Falls back to Tavily (if configured) or duckduckgo-search on quota exceeded (HTTP 429/403).
---

# Google PSE Search

## Search Tool Priority

```
1st: google-pse-search  ← this skill (default for all web searches)
     --provider google   (default) uses Google PSE API
     --provider tavily   uses Tavily API directly
     --provider auto     uses Google PSE, falls back to Tavily on 403/429
2nd: web_fetch          ← when URL is known (official docs, specific pages)
3rd: duckduckgo-search  ← fallback when neither Google PSE nor Tavily is available
```

## Basic Usage

```bash
# Skill directory
SKILL_DIR=~/.openclaw/workspace/skills/google-pse-search

# Default search (Korean, kr region)
python $SKILL_DIR/scripts/search.py "query"

# English search
python $SKILL_DIR/scripts/search.py "search query" --lang en

# Recent results (last 7 days)
python $SKILL_DIR/scripts/search.py "query" --date d7

# More results (up to 10)
python $SKILL_DIR/scripts/search.py "query" --num 10

# Site-specific search
python $SKILL_DIR/scripts/search.py "query" --site example.com

# Exact phrase / exclude terms
python $SKILL_DIR/scripts/search.py "query" --exact "must include" --exclude "exclude this"

# Pagination (page 2)
python $SKILL_DIR/scripts/search.py "query" --start 11

# Use Tavily as search provider (requires TAVILY_API_KEY)
python $SKILL_DIR/scripts/search.py "query" --provider tavily

# Auto mode: Google PSE with Tavily fallback on quota errors
python $SKILL_DIR/scripts/search.py "query" --provider auto
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--num N` | 5 | Number of results (1–10) |
| `--lang LANG` | ko | Language code (ko/en/ja/zh) |
| `--gl GL` | auto by lang | Region code override |
| `--date DATE` | — | Date restriction (d7/m1/y1 etc.). Tavily maps d1→day, d7/w1→week, m1→month, y1→year; other values are unsupported. |
| `--exact PHRASE` | — | Phrase that must appear in results |
| `--exclude TERM` | — | Term to exclude from results |
| `--site SITE` | — | Restrict to a specific site |
| `--start N` | 1 | Start index for pagination |
| `--raw` | — | Print raw JSON (debug) |
| `--provider` | google | Search provider: `google`, `tavily`, or `auto` |

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Missing env vars | .env not configured | Set GOOGLE_PSE_KEY and GOOGLE_CX_ID |
| HTTP 403/429 | Quota exceeded | Use `--provider auto` for Tavily fallback, or duckduckgo-search |
| HTTP 400 | Invalid parameters | Check option values |
| 0 results | Query or filter issue | Adjust query or remove filters |
| Unsupported flag warning | --exact/--exclude/--start used with Tavily | These flags are Google-only; a stderr warning is emitted |

## API Reference

→ See `references/api-params.md` for full parameter list, date restriction formats, and language codes.
