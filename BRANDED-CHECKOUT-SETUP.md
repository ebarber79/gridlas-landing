# Gridlas — Branded Checkout Setup (buy.gridlas.com)

**Paste this whole file to Claude Desktop.** It has the goal, the exact steps, and
direct links to every page. Ask Desktop to open each link and walk you through it.

---

## GOAL
Move Shopify checkout onto **buy.gridlas.com** so buyers never see the raw store
domain `i1ikbs-t6.myshopify.com` when they enter a credit card. This is a trust
fix at the moment of payment — currently all 4 "Buy now" buttons ($99 / $179 /
$349 / $499) hand off to that random-looking store URL.

Two systems, one DNS record, ~15 minutes. The website (gridlas.com on GitHub
Pages) is NOT touched — we only add a new subdomain for the store.

---

## STEP 1 — Shopify: connect the subdomain
**Open:** https://admin.shopify.com/store/i1ikbs-t6/settings/domains
(If that store handle is wrong, go to https://admin.shopify.com → pick the store → Settings → Domains)

1. Click **"Connect existing domain"**
2. Enter:  `buy.gridlas.com`  → **Next**
3. Shopify shows a CNAME to add. Leave this tab OPEN — you return in Step 3.

---

## STEP 2 — Cloudflare: add the CNAME record
**Open:** https://dash.cloudflare.com  → select the **gridlas.com** zone → **DNS → Records**

Click **"Add record"** and enter EXACTLY:

| Field  | Value                |
|--------|----------------------|
| Type   | CNAME                |
| Name   | `buy`                |
| Target | `shops.myshopify.com`|
| Proxy  | **DNS only** (GREY cloud — NOT orange) |
| TTL    | Auto                 |

Click **Save.**

> ⚠️ #1 GOTCHA: the proxy cloud MUST be grey (DNS only). Orange/proxied breaks
> Shopify's SSL and checkout will show a security warning. Grey = mandatory.

---

## STEP 3 — Verify + set primary
Back in the Shopify Domains tab:

1. Click **"Verify connection."** (If not ready, wait 5–10 min and retry.)
2. Wait for SSL to provision — green padlock / "SSL available" (usually <30 min).
3. Click **buy.gridlas.com → "Set as primary domain."**
   This is the step that actually moves the CHECKOUT PAGE onto your brand.
   (Shopify redirects all other store domains to the primary, so without this,
   buyers still get bounced to the myshopify URL at checkout.)
   - This only affects the STORE, not the gridlas.com website.
   - Reversible in one click anytime.

---

## STEP 4 — Tell Eric's terminal agent "done"
Once buy.gridlas.com is connected + primary + has a valid SSL cert, report back.
The agent will then, in the repo `~/gridlas-landing`:
  1. Rewrite all 4 cart links in index.html:
       https://i1ikbs-t6.myshopify.com/cart/<id>:1  →  https://buy.gridlas.com/cart/<id>:1
  2. Commit + push (GitHub Pages auto-deploys)
  3. Verify each of the 4 cart URLs returns HTTP 200 on the new domain

The 4 product cart IDs (for reference):
  - $99  Report           → 54847782846836
  - $179 Report + Dataset → 54847782879604
  - $349 Annual Pass      → 54847782912372
  - $499 Team License     → 54878585258356

---

## QUICK CHECK (optional, before Step 4)
Ask Claude Desktop to open **https://buy.gridlas.com** — if it loads your store
with a padlock (no cert warning), Step 4 is safe to run.

---

## STEP 5 (IMPORTANT) — the SECOND off-brand hop: Shop Pay / shop.app
Branding the domain fixes the *hostname*, but there's a second detour most people
miss. A traced cold-session click on a cart link today goes:

    gridlas.com  →  shop.app  →  i1ikbs-t6.myshopify.com

That middle `shop.app` hop is Shopify's **Shop Pay "accelerated / universal
redirect."** It is NOT controlled by DNS or the primary domain — it's a separate
toggle. Even after buy.gridlas.com is primary, Shop Pay can still bounce buyers
through shop.app before checkout.

Decide which you want:
  - **Shop Pay ON**  — one-tap checkout, higher completion for returning Shop Pay
    users, BUT the buyer briefly sees `shop.app` (off-brand) mid-flow.
  - **Shop Pay OFF** — fully branded checkout on buy.gridlas.com, no shop.app
    detour, slightly more friction (buyer types details).

For a credibility-based research product where the whole pitch is
"independent & unaffiliated," fully-branded (OFF) is usually the stronger call.

**To turn it OFF (fully branded checkout):**
Open: https://admin.shopify.com/store/i1ikbs-t6/settings/payments
  → find **Shop Pay** → uncheck / disable it → Save.
(You can also disable "Shop Pay" under the accelerated-checkout section on the
same page. Leaving Apple Pay / Google Pay on is fine — those don't add a hop.)

---

## FINAL STATE YOU'RE AIMING FOR
A buyer clicks "Buy now" and stays on **buy.gridlas.com** through the entire
card-entry + confirmation flow — no i1ikbs hash, no shop.app. That's both levers:
  1. buy.gridlas.com connected + PRIMARY   (Steps 1–3)
  2. Shop Pay OFF                            (Step 5)

