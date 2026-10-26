#!/bin/sh
# Rebuild the free 3-page summary PDF (lead magnet) from sample.html.
# Every figure in sample.html must match the live site (findings.html, homepage, pillars).
set -e
cd "$(dirname "$0")"
chromium --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=raw.pdf "file://$PWD/sample.html"
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -sOutputFile=../../Gridlas-Powering-AI-Sample.pdf raw.pdf
rm -f raw.pdf
ls -la ../../Gridlas-Powering-AI-Sample.pdf
