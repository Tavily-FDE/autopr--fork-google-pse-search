#!/usr/bin/env python3
"""
Google PSE (Programmable Search Engine) search script.

Usage:
  python search.py "query"
  python search.py "query" --num 10
  python search.py "query" --lang en --gl us
  python search.py "query" --date d7
  python search.py "query" --exact "must include phrase"
  python search.py "query" --exclude "exclude word"
  python search.py "query" --site example.com
  python search.py "query" --start 11
  python search.py "query" --raw

Environment variables required:
  GOOGLE_PSE_KEY   API key
  GOOGLE_CX_ID     Programmable Search Engine ID
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required.")
    print("  pip install requests")
    sys.exit(1)

API_URL = "https://customsearch.googleapis.com/customsearch/v1"

LANG_MAP = {
    "ko": ("lang_ko", "kr"),
    "en": ("lang_en", "us"),
    "ja": ("lang_ja", "jp"),
    "zh": ("lang_zh-CN", "cn"),
}


def get_env():
    api_key = os.environ.get("GOOGLE_PSE_KEY")
    cx_id = os.environ.get("GOOGLE_CX_ID")
    missing = []
    if not api_key:
        missing.append("GOOGLE_PSE_KEY")
    if not cx_id:
        missing.append("GOOGLE_CX_ID")
    if missing:
        print(f"Error: Missing environment variable(s): {', '.join(missing)}")
        print()
        print("Add them to ~/.openclaw/workspace/.env:")
        print("  GOOGLE_PSE_KEY=your_api_key")
        print("  GOOGLE_CX_ID=your_cx_id")
        sys.exit(1)
    return api_key, cx_id


def build_params(args, api_key, cx_id):
    lang_code = args.lang.lower()
    lr, gl_default = LANG_MAP.get(lang_code, (f"lang_{lang_code}", lang_code))
    gl = args.gl if args.gl else gl_default

    params = {
        "key": api_key,
        "cx": cx_id,
        "q": args.query,
        "num": min(max(1, args.num), 10),
        "lr": lr,
        "gl": gl,
        "hl": lang_code,
        "filter": "1",
    }

    if args.start and args.start > 1:
        params["start"] = args.start
    if args.date:
        params["dateRestrict"] = args.date
    if args.exact:
        params["exactTerms"] = args.exact
    if args.exclude:
        params["excludeTerms"] = args.exclude
    if args.site:
        params["siteSearch"] = args.site

    return params


def format_results(data, args):
    items = data.get("items", [])
    search_info = data.get("searchInformation", {})
    total = search_info.get("formattedTotalResults", "?")
    query = data.get("queries", {}).get("request", [{}])[0].get("searchTerms", args.query)

    lang_code = args.lang.lower()
    gl = args.gl if args.gl else LANG_MAP.get(lang_code, ("", lang_code))[1]

    conditions = [f"lang:{lang_code}", f"region:{gl}"]
    if args.date:
        conditions.append(f"date:{args.date}")
    if args.site:
        conditions.append(f"site:{args.site}")

    lines = []
    lines.append(f'## Search Results: "{query}" ({len(items)} results / ~{total} total)')
    lines.append(f'> Filters: {" · ".join(conditions)}')
    lines.append("")

    if not items:
        lines.append("No results found. Try adjusting your query or removing filters.")
        return "\n".join(lines)

    for i, item in enumerate(items, 1):
        title = item.get("title", "(no title)")
        url = item.get("link", "")
        snippet = item.get("snippet", "").replace("\n", " ").strip()
        lines.append(f"### {i}. [{title}]({url})")
        if snippet:
            lines.append(snippet)
        lines.append("")

    next_page = data.get("queries", {}).get("nextPage", [])
    if next_page:
        next_start = next_page[0].get("startIndex", "")
        lines.append("---")
        lines.append(f"Next page: use `--start {next_start}`")

    return "\n".join(lines)


def search(args):
    api_key, cx_id = get_env()
    params = build_params(args, api_key, cx_id)

    try:
        resp = requests.get(API_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print("Error: Request timed out (10s)")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Network connection failed")
        sys.exit(1)

    if resp.status_code == 400:
        err = resp.json().get("error", {}).get("message", "")
        print(f"Error: Bad request (400): {err}")
        sys.exit(1)
    elif resp.status_code == 403:
        err = resp.json().get("error", {}).get("message", "")
        if "quota" in err.lower() or "limit" in err.lower():
            print("Error: Daily quota exceeded (100 requests/day). Use duckduckgo-search as fallback.")
        else:
            print(f"Error: Access denied (403). Check your API key or CX ID.")
            print(f"  Details: {err}")
        sys.exit(1)
    elif resp.status_code == 429:
        print("Error: Rate limit exceeded (429). Use duckduckgo-search as fallback.")
        sys.exit(1)
    elif not resp.ok:
        print(f"Error: API error ({resp.status_code}): {resp.text[:200]}")
        sys.exit(1)

    data = resp.json()

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_results(data, args))


def main():
    parser = argparse.ArgumentParser(
        description="Google PSE web search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--num", type=int, default=5, help="Number of results (1-10, default: 5)")
    parser.add_argument("--lang", default="ko", help="Language code (default: ko, e.g. en, ja)")
    parser.add_argument("--gl", default="", help="Region code override (e.g. us, jp)")
    parser.add_argument("--date", default="", help="Date restriction (e.g. d7, m1, y1)")
    parser.add_argument("--exact", default="", help="Phrase that must appear in results")
    parser.add_argument("--exclude", default="", help="Word or phrase to exclude")
    parser.add_argument("--site", default="", help="Restrict search to a specific site")
    parser.add_argument("--start", type=int, default=1, help="Start index for pagination (default: 1)")
    parser.add_argument("--raw", action="store_true", help="Print raw JSON response (debug)")

    args = parser.parse_args()
    search(args)


if __name__ == "__main__":
    main()
