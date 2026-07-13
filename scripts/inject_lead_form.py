#!/usr/bin/env python3
"""Inject the shared lead-capture block + lead-form.css/js includes into every
content subpage that has the paid 'Get the report' CTA. Idempotent."""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

files = [f for f in subprocess.check_output(["git", "ls-files", "*/index.html"], text=True).split()
         if not f.startswith("tools/")]

CTA_END = re.compile(r'(Get the report →</a>\s*</div>)')
summary = 0
for f in files:
    src = open(f, encoding="utf-8").read()
    if "assets/lead-form.js" in src:      # idempotent
        continue
    if "Get the report →</a>" not in src:  # only pages with the paid CTA
        continue
    depthn = f.count("/")                  # a/b/index.html -> 2 ; a/index.html -> 1
    up = "../" * depthn
    slug = os.path.basename(os.path.dirname(f))
    block = (
        '\\1\n\n'
        '  <div class="lead-cta">\n'
        '    <p><b>Prefer the free 3-page summary first?</b> The 8 findings and the chart that explains the AI power crunch — straight to your inbox.</p>\n'
        '    <form class="lead-form" data-source="%s" data-pdf="%sGridlas-Powering-AI-Sample.pdf" novalidate>\n'
        '      <input type="email" placeholder="you@company.com" required aria-label="Email">\n'
        '      <button type="submit">Email me the summary →</button>\n'
        '    </form>\n'
        '    <p class="lead-fine">No spam. Unsubscribe anytime.</p>\n'
        '  </div>' % (slug, up)
    )
    new, n = CTA_END.subn(block, src, count=1)
    if n == 0:
        continue
    # head: lead-form.css before </head>
    new = new.replace("</head>", '<link rel="stylesheet" href="%sassets/lead-form.css">\n</head>' % up, 1)
    # body: lead-form.js before </body>
    new = new.replace("</body>", '<script src="%sassets/lead-form.js" defer></script>\n</body>' % up, 1)
    open(f, "w", encoding="utf-8").write(new)
    summary += 1
print("injected into", summary, "pages")
