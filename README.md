# MedicalBot Marketing Agent

A free, human-approved marketing workflow for **@MedicalSourcesHelperBot**.

## What the daily run now prepares
- Platform-specific English drafts for LinkedIn, X, Facebook, and Telegram channels.
- A Reddit/community participation guide that prioritizes genuinely helpful answers and respects self-promotion rules.
- A short-form video storyboard.
- An SEO article outline.
- A relevant outreach email draft and directory/partnership submission checklist.
- Public RSS discussion signals when feeds are reachable.
- A daily Markdown campaign pack delivered to the configured Telegram chat.

## What it does not do
It does not publish posts, send DMs or emails, create accounts, submit directory listings, run paid ads, or guarantee new users. Those actions require account access, platform-specific integrations, and human approval. No paid AI API is used; the daily copy is generated from reviewed templates rather than a generative AI model.

## Product accuracy
The Telegram bot provides structured information for selected drug records based on *The Harriet Lane Handbook, 23rd Edition*. It does **not** cover the entire handbook or every medicine. Never imply endorsement by the publisher, clinical validation, completeness, or replacement of current clinical references.

## Run
GitHub Actions runs daily and can also be started manually from **Actions → Daily marketing drafts → Run workflow**. The resulting campaign pack is sent to Telegram when the repository secrets `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are configured.

All public-facing content must be checked for accuracy, relevance, and platform rules before publishing.
