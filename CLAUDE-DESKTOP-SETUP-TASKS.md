# Gridlas — Setup Tasks for Claude Desktop

**How to use this file:** Paste the whole file into Claude Desktop. Ask it to open each
link and walk you through the steps one at a time. Claude Desktop can open pages and guide
you; it does NOT edit the website code — that part is done by the terminal agent (Eric's
Hermes/Claude Code assistant on the Raspberry Pi). Your job here is to complete the
dashboard steps and bring back TWO things:

  OUTPUT 1 — confirmation that **buy.gridlas.com** loads with a padlock (Task A)
  OUTPUT 2 — the **Cloudflare Web Analytics token** string (Task B)

When you have either output, return to the terminal agent and say so. It finishes the rest.

Context you may need:
  - Website gridlas.com is hosted on GitHub Pages, DNS managed at Cloudflare.
  - Shopify store handle is **i1ikbs-t6** (store sells the $99/$179/$349/$499 reports).
  - Both tasks are independent — do them in either order.

═══════════════════════════════════════════════════════════════════════
TASK A — Branded checkout (buy.gridlas.com)  ·  ~15 min + SSL wait
═══════════════════════════════════════════════════════════════════════
GOAL: Move Shopify checkout onto buy.gridlas.com so buyers never see the raw
"i1ikbs-t6.myshopify.com" address when they type in a credit card. This does NOT
touch the gridlas.com website — it only adds a new subdomain for the store.

─── Step A1 — Shopify: connect the subdomain ───
Open: https://admin.shopify.com/store/i1ikbs-t6/settings/domains
(If that lands on the wrong store: go to https://admin.shopify.com , pick the store,
 then Settings → Domains.)

  1. Click "Connect existing domain".
  2. Type exactly:  buy.gridlas.com   then click Next.
  3. Shopify will show a CNAME record to add. Leave this browser tab OPEN — you come
     back to it in Step A3.

─── Step A2 — Cloudflare: add the CNAME record ───
Open: https://dash.cloudflare.com  →  click the **gridlas.com** zone  →  DNS  →  Records.

  1. Click "Add record".
  2. Enter these values EXACTLY:
        Type:    CNAME
        Name:    buy
        Target:  shops.myshopify.com
        Proxy status:  DNS only   ← the cloud icon must be GREY, not orange
        TTL:     Auto
  3. Click Save.

  ⚠️ CRITICAL: The proxy cloud MUST be grey ("DNS only"). If it is orange
     ("Proxied"), Shopify's SSL certificate will fail and checkout will show a
     security warning. Grey cloud is mandatory here.

─── Step A3 — Shopify: verify + set primary ───
Return to the Shopify Domains tab from Step A1.

  1. Click "Verify connection". If it says not ready, wait 5–10 minutes and click again.
  2. Wait for SSL to finish provisioning — you'll see a green padlock / "SSL available".
     This is usually under 30 minutes.
  3. Click on buy.gridlas.com → "Set as primary domain".
     ⭐ This step is what actually moves the checkout PAGE onto your brand. Shopify
        redirects all non-primary domains to the primary one, so without this the
        buyer still gets bounced to the myshopify address at payment.
     - This affects only the STORE, never the gridlas.com website.
     - It is reversible in one click at any time.

─── Step A4 — Confirm, then report back ───
Open: https://buy.gridlas.com
  - It should load your store WITH a padlock and NO certificate warning.
  - If it does: TASK A is done. Tell the terminal agent "buy.gridlas.com is live and
    primary." It will then rewrite the 4 "Buy now" links on the site to use
    buy.gridlas.com and verify each returns HTTP 200.
  - If you see a certificate/SSL warning: wait 15–30 more minutes (SSL still
    provisioning) and reload before reporting.

═══════════════════════════════════════════════════════════════════════
TASK B — Free website analytics (Cloudflare Web Analytics)  ·  ~5 min
═══════════════════════════════════════════════════════════════════════
GOAL: Get a free, privacy-friendly analytics token (no cookie banner needed) so we can
see traffic and which pages drive report sales. You just need to COPY ONE TOKEN and
bring it back — the terminal agent installs it across all 28 pages.

  Why this method: gridlas.com runs on GitHub Pages (not proxied through Cloudflare),
  so we use Cloudflare's manual JavaScript-snippet analytics, which works on any host.

─── Step B1 — Open Cloudflare Web Analytics ───
Open: https://dash.cloudflare.com  →  in the left sidebar click "Analytics & Logs"
      →  "Web Analytics".
(Direct attempt: https://dash.cloudflare.com/?to=/:account/web-analytics )

─── Step B2 — Add the site ───
  1. Click "Add a site" (or "Manage site" if gridlas.com is already listed).
  2. Enter the hostname:  gridlas.com
  3. Click Done / Continue.

─── Step B3 — Copy the token (this is the deliverable) ───
Cloudflare shows a JavaScript snippet that looks like this:

    <script defer src='https://static.cloudflareinsights.com/beacon.min.js'
      data-cf-beacon='{"token": "abc123def456......"}'></script>

  - Copy the TOKEN — the long string inside  "token": "……"  (just the string between
    the quotes, e.g.  abc123def456......  ).
  - You do NOT need to paste the snippet anywhere yourself. Only the token string is needed.

─── Step B4 — Report back ───
Give the token string to the terminal agent: "Cloudflare Web Analytics token is: <token>".
It will insert the beacon into all 28 pages, deploy, and verify analytics is live.

═══════════════════════════════════════════════════════════════════════
QUICK SUMMARY — what to bring back to the terminal agent
═══════════════════════════════════════════════════════════════════════
  [ ] Task A: "buy.gridlas.com is live and primary" (loads with a padlock)
  [ ] Task B: "Cloudflare Web Analytics token is: __________"

Either one can be delivered on its own; you don't have to finish both before reporting.
