# MedicalBot Marketing Agent

An on-demand, human-reviewed content delivery bridge for **@MedicalSourcesHelperBot**.

## How content is created and delivered

1. The owner requests a campaign, Telegram post, Instagram caption/carousel, Reel script, SEO article, or outreach email in ChatGPT.
2. ChatGPT creates the actual content in the conversation using its own model and, when useful, connected research tools. This repository does not call a paid AI API.
3. After the owner approves content for Telegram delivery, ChatGPT commits a Markdown file to the `outbox/` folder through the connected GitHub integration.
4. A GitHub Actions workflow starts automatically on that commit and sends the file to the Telegram chat configured by `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

The owner should not need to create GitHub issues or manually copy/paste the content. Each delivery uses a new Markdown file under `outbox/`.

## Important boundaries

- ChatGPT content generation happens in the ChatGPT conversation, not inside GitHub Actions. GitHub Actions is only the delivery bridge.
- No paid AI API or external model API key is required.
- The workflow sends files only to the configured Telegram chat. It does not publish directly to Instagram, LinkedIn, X, Facebook, Reddit, or send emails.
- Instagram graphics and video files need a separate asset-creation and delivery step; text drafts, captions, scripts, and creative briefs can be delivered as Markdown.
- Publishing, outreach, and community participation remain under the owner's control and require review.
- Do not send confidential user data, credentials, or patient information through the marketing outbox.

## Telegram setup

The repository must have these GitHub Actions secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Do not put either secret in source code, outbox files, or ChatGPT messages.

## Product accuracy

The Telegram bot provides structured information for selected drug records based on *The Harriet Lane Handbook, 23rd Edition*. It does **not** cover the entire handbook or every medicine. Never imply publisher endorsement, clinical validation, completeness, or replacement of current clinical references.
