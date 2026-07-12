#!/usr/bin/env python3
"""Wave-1 mechanical transforms across gridlas subpages.
Idempotent. Run from repo root. Review with `git diff` after.
Applies: Article schema dates, CTA -> /#pricing +UTM, WebP <picture> wraps,
visible 'Updated' byline stamp."""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TODAY = "2026-07-12"

# git-tracked subpage index.html files (exclude tools estimator; handled separately)
files = subprocess.check_output(
    ["git", "ls-files", "*/index.html"], text=True).split()
files = [f for f in files if not f.startswith("tools/")]

def pubdate(f):
    out = subprocess.check_output(
        ["git", "log", "--diff-filter=A", "--format=%as", "--", f], text=True).split()
    return out[-1] if out else TODAY

ART_RE   = re.compile(r'("@type"\s*:\s*"Article"\s*,)')
CTA_RE   = re.compile(r'href="(?:\.\./)+index\.html"(\s*>\s*Get the report)')
IMG_RE   = re.compile(r'<img\s+src="([^"]+)\.png"([^>]*)>')
BYLINE_RE= re.compile(r'(<p class="byline">)(.*?)(</p>)')

summary = {"dates":0, "cta":0, "pics":0, "byline":0}
for f in files:
    slug = os.path.basename(os.path.dirname(f))
    src = open(f, encoding="utf-8").read()
    orig = src

    # 1) Article schema dates (skip if already present or no Article node)
    if "datePublished" not in src and ART_RE.search(src):
        pub = pubdate(f)
        src, n = ART_RE.subn(
            r'\1"datePublished":"%s","dateModified":"%s",' % (pub, TODAY), src, count=1)
        summary["dates"] += n

    # 2) CTA -> absolute /#pricing with per-page UTM (idempotent: only matches ../index.html forms)
    def cta_sub(m):
        return ('href="/?utm_source=gridlas&utm_medium=content&utm_content=%s#pricing"%s'
                % (slug, m.group(1)))
    src, n = CTA_RE.subn(cta_sub, src)
    summary["cta"] += n

    # 3) WebP <picture> wrap for rendered figures (skips <meta>/JSON; only real <img> tags)
    def pic_sub(m):
        base, rest = m.group(1), m.group(2)
        return ('<picture><source srcset="%s.webp" type="image/webp">'
                '<img src="%s.png"%s></picture>' % (base, base, rest))
    # avoid double-wrapping
    def pic_guard(m):
        return m.group(0) if 'srcset="%s.webp"' % m.group(1) in src else pic_sub(m)
    src, n = IMG_RE.subn(pic_guard, src)
    summary["pics"] += n

    # 4) visible 'Updated' stamp in byline (idempotent)
    if "Updated Jul 2026" not in src:
        def by_sub(m):
            return m.group(1) + m.group(2) + " · Updated Jul 2026" + m.group(3)
        src, n = BYLINE_RE.subn(by_sub, src, count=1)
        summary["byline"] += n

    if src != orig:
        open(f, "w", encoding="utf-8").write(src)

print("files:", len(files), "| changes:", summary)
