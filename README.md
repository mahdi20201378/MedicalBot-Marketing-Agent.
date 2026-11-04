# MedicalBot Marketing Agent

An on-demand, human-reviewed content delivery bridge for **@MedicalSourcesHelperBot**.

## How content is created and delivered

1. The owner requests a campaign, social post, carousel copy, Reel script, SEO article, or outreach email in ChatGPT.
2. ChatGPT creates the actual content using its available capabilities and, when useful, connected research tools. This repository does not call a paid AI API.
3. After the owner approves the content for Telegram delivery, an authorized request issue titled `SEND TO TELEGRAM: ...` is created in this repository.
4. GitHub Actions sends the issue body to the Telegram chat configured by `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, as a Markdown document.

The workflow runs only for issues opened by the repository owner account `mahdi20201378` whose title begins with `SEND TO TELEGRAM:`. It does not send scheduled daily template reports.

## Important boundaries

- ChatGPT content generation happens in the ChatGPT conversation, not inside GitHub Actions. GitHub Actions is only the delivery bridge.
- No paid AI API or external model API key is required.
- Delivery is to the Telegram chat configured in GitHub Secrets. This workflow does not publish to Instagram, LinkedIn, X, Facebook, Reddit, or send email.
- Instagram graphics or video files need a separate asset-creation and delivery step; text drafts and creative briefs can be delivered through this workflow.
- Publishing, outreach, and community participation remain under the owner's control and require review.

## Telegram setup

The repository must have these GitHub Actions secrets:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Do not put either secret in source code, issues, or ChatGPT messages.

## Product accuracy

The Telegram bot provides structured information for selected drug records based on *The Harriet Lane Handbook, 23rd Edition*. It does **not** cover the entire handbook or every medicine. Never imply publisher endorsement, clinical validation, completeness, or replacement of current clinical references.
