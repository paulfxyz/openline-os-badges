#!/usr/bin/env bash
# sync-mirror.sh — mirror the primary badge repo to its public twin.
#
# The Openline OS badge system lives in the PRIMARY repo:
#     paulfxyz/openline-os-badges
# and is mirrored byte-for-byte into the PUBLIC MIRROR:
#     paulfxyz/openline-audit-shots   (the repo's former name)
#
# The mirror exists only so historical raw.githubusercontent.com URLs that
# still point at "openline-audit-shots" keep resolving (raw GitHub does NOT
# follow repo-rename redirects). NEVER edit the mirror directly — only push
# into it what the primary already has.
#
# Usage:
#     bash scripts/sync-mirror.sh
#
# Requires: a git remote named "origin" pointing at the primary repo, and
# push access to the mirror. Run from anywhere inside the repo.
set -euo pipefail

PRIMARY_SLUG="paulfxyz/openline-os-badges"
MIRROR_SLUG="paulfxyz/openline-audit-shots"
BRANCH="main"

# Resolve repo root regardless of where the script is called from.
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

# Derive the mirror URL from origin so it works through the git proxy too.
ORIGIN_URL="$(git remote get-url origin)"
MIRROR_URL="${ORIGIN_URL/openline-os-badges/openline-audit-shots}"

echo "→ Primary : $ORIGIN_URL"
echo "→ Mirror  : $MIRROR_URL"

# Make sure we have the latest primary state locally.
git fetch origin "$BRANCH"

# Add/refresh the mirror remote.
if git remote | grep -qx "mirror"; then
  git remote set-url mirror "$MIRROR_URL"
else
  git remote add mirror "$MIRROR_URL"
fi

# Force the mirror to match the primary branch exactly.
echo "→ Pushing $BRANCH to mirror (force, exact match)…"
git push --force mirror "origin/$BRANCH:refs/heads/$BRANCH"

echo "✅ Mirror synced. Both repos now serve identical bytes on '$BRANCH'."
echo "   Verify a raw URL if you like:"
echo "   curl -sI https://raw.githubusercontent.com/$MIRROR_SLUG/$BRANCH/os-nav/badge-hr-resources.png | head -1"
