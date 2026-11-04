#!/usr/bin/env python3
"""Free RSS-based marketing draft generator. No paid APIs; never auto-posts."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "agent/config.json").read_text(encoding="utf-8"))
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "MedicalBotMarketingResearch/1.0 (public RSS reader)"}

def clean(s):
    return re.sub(r"\\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as response:
        return ET.fromstring(response.read())

def entries(root):
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

def main():
    keywords=[k.lower() for k in CFG["keywords"]]
    rows=[]
    for feed in CFG["feeds"]:
        try:
            for title,link,desc in entries(fetch(feed))[:CFG["max_items_per_feed"]]:
                text=(title+" "+desc).lower()
                score=sum(1 for k in keywords if k in text)
                if title and score:
                    rows.append((score,title,link,desc))
        except Exception as exc:
            rows.append((0,"FEED ERROR: "+feed,"",str(exc)))
    rows.sort(key=lambda x:x[0], reverse=True)
    stamp=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines=[f"# Daily marketing research — {stamp}","",
      "> Research and draft suggestions only. A human must verify context, platform rules, medical accuracy, and links before publishing.","",
      f"**Product:** {CFG['bot_name']} — {CFG['bot_url']}","",
      f"**Scope:** {CFG['product_scope']}","","## Relevant public discussions and content signals",""]
    count=0
    for score,title,link,desc in rows:
        if title.startswith("FEED ERROR"):
            lines += [f"- {title}: {desc}"]
            continue
        count+=1
        lines += [f"### {count}. {title}",f"- Relevance score: {score}",f"- Source: {link}",f"- Context: {desc[:500]}","- Suggested action: Read the full discussion and, only if relevant and permitted, prepare a helpful non-promotional contribution. Do not post an unsolicited advertisement.",""]
    if count==0:
        lines += ["No relevant items were found in the available public feeds today. Check feed availability and try again later.",""]
    lines += ["## Ready-to-review evergreen message","","Medical Sources Helper Bot provides structured drug information for selected stored records based on *The Harriet Lane Handbook, 23rd Edition*. Coverage is limited to the records currently available in the bot; it does not represent the entire handbook. Explore: "+CFG["bot_url"],"",
      "## Human review checklist","- [ ] Confirm the source and context are relevant.","- [ ] Verify every medical statement and avoid patient-specific advice.","- [ ] Check the community's self-promotion rules.","- [ ] Edit for usefulness; disclose affiliation where appropriate.","- [ ] Publish manually only after approval.",""]
    path=OUT/f"daily-{stamp}.md"
    path.write_text("\n".join(lines),encoding="utf-8")
    print(f"Saved {path.relative_to(ROOT)}")
if __name__=="__main__": main()
