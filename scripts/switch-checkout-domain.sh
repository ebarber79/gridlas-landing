#!/usr/bin/env bash
# Switch checkout host between the raw myshopify store and the branded buy.gridlas.com.
# Preserves cart IDs and UTM params — only the hostname changes.
#
# Usage:
#   scripts/switch-checkout-domain.sh brand     # myshopify -> buy.gridlas.com
#   scripts/switch-checkout-domain.sh revert     # buy.gridlas.com -> myshopify
#   scripts/switch-checkout-domain.sh check      # show current cart links, no changes
#
# Run from repo root. Does NOT commit/push — review the diff first.

set -euo pipefail
cd "$(dirname "$0")/.."

RAW="i1ikbs-t6.myshopify.com"
BRAND="buy.gridlas.com"
FILE="index.html"

case "${1:-}" in
  brand)
    before=$(grep -c "$RAW/cart" "$FILE" || true)
    sed -i "s#https://$RAW/cart#https://$BRAND/cart#g" "$FILE"
    after=$(grep -c "$BRAND/cart" "$FILE" || true)
    echo "Rewrote $before cart link(s) -> $BRAND (now $after present)."
    ;;
  revert)
    before=$(grep -c "$BRAND/cart" "$FILE" || true)
    sed -i "s#https://$BRAND/cart#https://$RAW/cart#g" "$FILE"
    after=$(grep -c "$RAW/cart" "$FILE" || true)
    echo "Reverted $before cart link(s) -> $RAW (now $after present)."
    ;;
  check)
    echo "Current cart links in $FILE:"
    grep -oE 'https://[^"]*/cart/[^"]*' "$FILE" || echo "  (none found)"
    ;;
  *)
    echo "Usage: $0 {brand|revert|check}"; exit 1 ;;
esac

echo "Review with: git diff $FILE   (nothing was committed)"
