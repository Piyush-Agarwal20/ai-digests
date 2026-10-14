# AI Digests

Daily reports built from 11 private Google Alerts RSS feeds.

- [Latest report](latest.html)
- [Groq test report for 2026-10-14](reports/2026-10-14.html)
- [Earlier RSS demo](reports/2026-10-13.html)

## Current test pipeline

1. Select articles from the last 24 hours.
2. Deduplicate overlapping alerts.
3. Fetch readable article text, falling back to the RSS description when blocked.
4. Summarize batches in parallel with four Groq API keys.
5. Retry temporary failures and generate one HTML page with a short summary, lessons, crux, and source link per article.

The RSS feed URLs and API keys are private and are intentionally not stored in this public repository. The current local test loads the four Groq keys from the existing Reddit agent environment; production scheduling and GitHub Secrets configuration are still pending.
