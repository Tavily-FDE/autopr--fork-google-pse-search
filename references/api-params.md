# Google PSE API Parameter Reference

Source: https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list

## Endpoint

```
GET https://customsearch.googleapis.com/customsearch/v1
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `key` | string | ✅ | API Key (`GOOGLE_PSE_KEY`) |
| `cx` | string | ✅ | PSE ID (`GOOGLE_CX_ID`) |
| `q` | string | ✅ | Search query |
| `num` | integer | — | Number of results (1–10, default 10) |
| `start` | integer | — | Start index for pagination (default 1) |
| `lr` | string | — | Language restriction for documents |
| `gl` | string | — | Geolocation / region boost |
| `hl` | string | — | UI language |
| `dateRestrict` | string | — | Date restriction |
| `exactTerms` | string | — | Phrase that must appear in results |
| `excludeTerms` | string | — | Word/phrase to exclude from results |
| `siteSearch` | string | — | Restrict search to a specific site |
| `fileType` | string | — | Restrict results by file extension |
| `filter` | string | — | Duplicate content filter (0=off, 1=on) |
| `cr` | string | — | Country restriction for documents |
| `hq` | string | — | Additional AND query terms |

## lr (Language Restriction) Values

| Value | Language |
|-------|----------|
| `lang_ko` | Korean |
| `lang_en` | English |
| `lang_ja` | Japanese |
| `lang_zh-CN` | Chinese (Simplified) |
| `lang_zh-TW` | Chinese (Traditional) |
| `lang_de` | German |
| `lang_fr` | French |

## gl (Region Code) Values

| Value | Region |
|-------|--------|
| `kr` | South Korea |
| `us` | United States |
| `jp` | Japan |
| `gb` | United Kingdom |
| `cn` | China |

## dateRestrict Format

| Value | Meaning |
|-------|---------|
| `d1` | Past 1 day |
| `d7` | Past 7 days |
| `w1` | Past 1 week |
| `m1` | Past 1 month |
| `m3` | Past 3 months |
| `y1` | Past 1 year |

## Pagination

- `num` max is 10; `start` max is 91 (up to 100 total results retrievable)
- Page 2: `--start 11`, Page 3: `--start 21`

## Quota

- Free tier: 100 queries/day
- Paid: $5 per 1,000 queries (max 10,000/day)
- HTTP 403 or 429 returned on quota exceeded
- **Service discontinued for new customers after January 1, 2027** (existing customers unaffected)
