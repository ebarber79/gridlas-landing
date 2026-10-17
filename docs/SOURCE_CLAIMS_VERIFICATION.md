# Source-claim consistency checks

This change distinguishes generation/storage interconnection statistics from data-center load connection timing. It does not certify retained research figures or source-link availability. The tests require Python 3.12+ and Node.js 22+, use only their standard libraries, and do not submit forms or call paid services.

## Run locally

From the repository root, ensure the base branch is available, then run:

```sh
export GRIDLAS_BASE_REF=origin/main
python -B -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/test_estimator_scope.cjs
git diff --check
```

The default comparison ref is `origin/main`; use `GRIDLAS_BASE_REF` to select a different fetched base commit if appropriate. Do not substitute the changed HEAD as a baseline: that can turn preservation tests into self-comparisons. A missing base ref fails tests rather than silently removing preservation coverage.

The Python tests check source-population wording, visible/structured FAQ and glossary parity, metadata, JSON-LD parsing and preservation of forms, executable article scripts and styles. The Node tests execute the actual calculator script in an offline DOM fixture whose IDs come from the real HTML. They compare numerical output against the base over 104 market/cooling/size combinations, check real input handlers and reject connection-time forecasts and guaranteed on-site bypass claims. The lead-capture implementation is compared with the base; delivery itself is not exercised.

## CI boundary

`.github/workflows/source-claims.yml` runs only for pull requests or manual dispatch. It has read-only repository permission, does not persist checkout credentials, fetches history for the comparison baseline and performs no deployment. It does not merge, publish ads, contact leads, or change GitHub Pages configuration.

CI checks committed whitespace across the base-to-HEAD change range. Local `git diff --check` is useful while editing; on a clean CI checkout it would check no uncommitted changes, so CI uses an explicit range instead.

No hosted CI pass is claimed until a pull request is published and checks complete at its exact head. GitHub Pages still publishes from main; merging to main may deploy the site and requires separate approval.

## Verification limits and follow-up

The primary Queued Up PDF could not be downloaded directly during preparation (HTTP 403). Search-indexed primary text establishes the generation/storage-versus-load scope warning, but full-document review, page references and source-link accessibility remain open. Existing demand, market capacity, queue share, nuclear/gas milestones, power/water coefficients, downloadable PDFs, raster social images and video are not independently certified by these contracts.

The workaround chart retains historical illustrative bars, now explicitly labeled as different clocks that are not directly comparable. Calculator preservation is not engineering validation: units, water accounting and coefficient provenance need their own review before claiming site-specific feasibility.

Before publication, review those source limitations, confirm that graphical/PDF/video assets do not reintroduce an unqualified national load-connection wait, and exercise lead delivery and purchase attribution only with appropriate approval.
