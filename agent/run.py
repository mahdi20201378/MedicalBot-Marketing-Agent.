#!/usr/bin/env python3
"""Free, human-approved multi-channel marketing pack generator."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "agent/config.json").read_text(encoding="utf-8"))
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

def fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": "MedicalBotMarketingResearch/1.0"})
    with urllib.request.urlopen(req, timeout=10) as response:
        return ET.fromstring(response.read())

def get_entries(root):
    found=[]
    for item in root.findall(".//item"):
        found.append((clean(item.findtext("title")), clean(item.findtext("link")), clean(item.findtext("description"))))
    ns={"a":"http://www.w3.org/2005/Atom"}
    for item in root.findall(".//a:entry",ns):
        link=item.find("a:link",ns)
        found.append((clean(item.findtext("a:title",default="",namespaces=ns)),
                      link.attrib.get("href","") if link is not None else "",
                      clean(item.findtext("a:summary",default="",namespaces=ns))))
    return found

def get_signals():
    keywords=[k.lower() for k in CFG["keywords"]]
    matches=[]; errors=[]
    for feed in CFG["feeds"]:
        try:
            for title,link,desc in get_entries(fetch_feed(feed))[:CFG["max_items_per_feed"]]:
                score=sum(1 for k in keywords if k in (title+" "+desc).lower())
                if title and score: matches.append((score,title,link,desc))
        except Exception as exc:
            errors.append(f"- {feed}: {exc}")
    matches.sort(key=lambda x:x[0],reverse=True)
    return matches[:8],errors

def main():
    stamp=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    bot=CFG["bot_name"]; url=CFG["bot_url"]; scope=CFG["product_scope"]
    themes=[
      "A quick way to look up stored pediatric drug information",
      "Why checking the exact medicine record matters",
      "Pregnancy and breastfeeding information: check what is actually available",
      "A practical reference workflow for trainees",
      "What a focused drug database can—and cannot—tell you",
      "How to make medication-reference work more organized",
      "Why drug information must always be verified"
    ]
    theme=themes[datetime.now(timezone.utc).weekday()]
    matches,errors=get_signals()
    lines=[
      f"# Daily marketing action pack — {stamp}","",
      "> Ready-to-review marketing materials. Publish only after checking accuracy and platform rules.","",
      f"**Product:** {bot}",f"**Link:** {url}",f"**Accurate scope:** {scope}","",
      "## 1. Today's campaign focus",f"**Theme:** {theme}",
      "Today’s goal: publish one useful educational post, improve one discovery surface, and make one relevant community contribution only where permitted. Do not mass-post identical copy.","",
      "## 2. LinkedIn post — ready to use",
      f"""A practical medication-reference workflow starts with knowing exactly what a tool covers.

{bot} provides structured information for selected drug records, including available dosing and indication details, plus pregnancy or breastfeeding information when those fields are present.

Its database is based on selected records from The Harriet Lane Handbook, 23rd Edition—not the entire handbook.

It may be a useful starting point for healthcare professionals and learners, but important decisions still require checking current authoritative references and the patient's clinical context.

Explore the Telegram tool: {url}

#Pediatrics #MedicationSafety #MedicalEducation #ClinicalReference""","",
      "## 3. X post",
      f"""Need a structured starting point for selected pediatric drug records? {bot} organizes available drug information in Telegram. Coverage is limited to stored records—not the full Harriet Lane Handbook. Always verify clinically. {url}""","",
      "## 4. Facebook / Telegram channel post",
      f"""**A focused drug-information reference in Telegram**

{bot} organizes information for selected stored drug records, with available dosing, indications, and pregnancy or breastfeeding details where recorded.

The database is based on selected records from The Harriet Lane Handbook, 23rd Edition. It does not cover the entire handbook.

Use it as a reference starting point—not as a replacement for current guidelines or clinical judgment.

Open: {url}""","",
      "## 5. Reddit and professional communities",
      "Do not paste an advertisement into a thread. First find a current discussion where the tool genuinely adds relevant context. Give a complete, useful answer without requiring anyone to click. If community rules permit disclosure, use this optional note:",
      f"""Disclosure: I built {bot}, a Telegram tool that organizes information for selected stored drug records based on The Harriet Lane Handbook, 23rd Edition. It does not cover the whole handbook: {url}""",
      "If self-promotion is prohibited or the tool is not directly relevant, do not mention it.","",
      "## 6. Short video / reel storyboard (20–25 seconds)",
      "- 0–4 sec: On-screen text: Looking for a structured starting point for drug information?",
      "- 4–10 sec: Record the real bot search flow using a non-patient example. Do not fabricate results.",
      "- 10–16 sec: Show only fields genuinely present in the displayed record.",
      "- 16–21 sec: Scope note: Selected stored records; not the entire Harriet Lane Handbook.",
      f"- 21–25 sec: Explore the Telegram bot: {url}",
      "Add captions. Do not show patient information or imply clinical validation.","",
      "## 7. SEO article outline",
      "**Suggested title:** A practical way to organize selected pediatric drug information",
      "- Explain why clinicians cross-check drug information across authoritative sources.",
      "- Describe how structured fields can be easier to scan.",
      "- Explain the limited scope of this bot's stored records.",
      "- Include a generic lookup example only after verifying it in the live bot.",
      "- Explain why current references, local protocols, and clinical judgment remain essential.",
      f"- Closing link: {url}","",
      "## 8. Outreach email — for relevant organizations only",
      "**Subject:** Resource suggestion: Telegram tool for selected pediatric drug records",
      f"""Hello,

I would like to share {bot}, a Telegram-based tool that organizes information for selected stored drug records, including available dosing, indications, and pregnancy or breastfeeding details where recorded.

The database is based on selected records from The Harriet Lane Handbook, 23rd Edition and does not represent the entire handbook. It is intended as a supplementary reference starting point, not a substitute for current authoritative sources or clinical judgment.

If your resource directory or educational community accepts relevant tools, you can review it here: {url}

Thank you for considering it.""","",
      "## 9. Directory and partnership pipeline",
      "- Identify one pediatric education, pharmacy, or clinician-resource directory that accepts external submissions.",
      "- Read its current submission rules before applying.",
      "- Submit an accurate description; never imply endorsement by the handbook publisher.",
      "- Record the directory, submission URL, date, and response in the campaign tracker.",
      "- Contact only organizations with a clear, relevant partnership or submission route; no unsolicited bulk email.","",
      "## 10. Today's action checklist",
      "- [ ] Check the live bot and confirm every feature mentioned above is available.",
      "- [ ] Publish one suitable post on a platform where you have an account and promotion is allowed.",
      "- [ ] Find one relevant professional discussion and contribute helpfully without spamming.",
      "- [ ] Submit to one relevant directory only if its rules permit it.",
      "- [ ] Track clicks, bot starts, trial starts, and paid conversions where available.",
      "- [ ] Reply to genuine comments; do not send unsolicited DMs.","",
      "## 11. Public discussion signals"
    ]
    if matches:
        for i,(score,title,link,desc) in enumerate(matches,1):
            lines += [f"{i}. **{title}**",f"   - Source: {link}",f"   - Context: {desc[:350]}",f"   - Relevance score: {score}","   - Inspect manually; participate only if genuinely relevant and permitted.",""]
    else:
        lines += ["No matching public-feed items were retrieved today. The campaign pack above is still usable.",""]
    if errors:
        lines += ["**Feed retrieval errors:**"]+errors+[""]
    lines += [
      "## 12. Automation boundaries",
      "- Automated: scheduled research attempt, platform-specific draft generation, daily report, and Telegram delivery.",
      "- Human approval remains necessary for posting, community participation, directory submissions, and outreach.",
      "- Not automated: posting to social accounts, DMs, emails, paid ads, account creation, or verified conversion attribution.",
      "- No paid AI API is used. Copy is template-generated, not deeply AI-researched or personalized.",""
    ]
    out=OUT/f"daily-{stamp}.md"
    out.write_text("\n".join(lines),encoding="utf-8")
    print(f"Saved {out.relative_to(ROOT)}")

if __name__=="__main__":
    main()
