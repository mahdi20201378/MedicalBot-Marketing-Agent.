# MedicalBot Marketing Agent

A free, human-approved marketing assistant for **@MedicalSourcesHelperBot**.

It prepares ethical, source-aware marketing drafts and a daily opportunity report. It does not auto-post, send unsolicited DMs, scrape private communities, or modify the Telegram bot or its Supabase database.

## What it does
- Collects public RSS feeds and scores items for relevance.
- Creates draft posts and outreach ideas for a human to review.
- Runs daily with GitHub Actions (no paid AI API or server required).
- Publishes a simple English landing page through GitHub Pages.

## Important product scope
The Telegram bot provides structured information for selected drug records based on *The Harriet Lane Handbook, 23rd Edition*. It does **not** claim to cover the entire handbook or every medicine.

## Quick start
1. In GitHub, open **Settings → Pages** and publish from the `main` branch, `/docs` folder.
2. In **Settings → Actions → General → Workflow permissions**, enable read/write access if you want the workflow to open approval issues.
3. Edit `agent/config.json` to tune keywords and public RSS feeds.
4. Run **Actions → Daily marketing drafts → Run workflow**.

## Review before publishing
All generated content is a draft. Verify platform rules, medical claims, and links before posting. Never present the bot as a substitute for clinical judgment or an authoritative full-text medical reference.

## Local run
Requires Python 3.10+:
```bash
python agent/run.py
```
