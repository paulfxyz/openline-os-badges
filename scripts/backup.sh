#!/usr/bin/env bash
# backup.sh — snapshot this repo independently of GitHub.
#
# Produces two artifacts in ./backups/ , both timestamped (UTC):
#   1. <name>-<UTC>.bundle   — a full git bundle (all branches + complete history).
#                              `git clone <file>.bundle` rebuilds the repo exactly.
#   2. <name>-<UTC>.tar.gz   — a flat tarball of the working tree (images + scripts),
#                              for quick file recovery without git.
#
# Keep these OFF GitHub (local disk / cloud storage) so the repo can be
# rebuilt even if the remote is ever lost.
#
# Usage:
#     bash scripts/backup.sh [output_dir]
#         output_dir defaults to ./backups
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

NAME="$(basename "$ROOT")"
OUT_DIR="${1:-$ROOT/backups}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$OUT_DIR"

BUNDLE="$OUT_DIR/${NAME}-${STAMP}.bundle"
TARBALL="$OUT_DIR/${NAME}-${STAMP}.tar.gz"

echo "→ Repo   : $NAME ($ROOT)"
echo "→ Output : $OUT_DIR"

# 1. Full git bundle (all refs → complete history, offline-clonable).
echo "→ Writing git bundle…"
git bundle create "$BUNDLE" --all

# 2. Flat tarball of tracked + untracked (non-ignored) files, excluding .git and backups.
echo "→ Writing working-tree tarball…"
tar --exclude='./.git' --exclude='./backups' -czf "$TARBALL" .

echo ""
echo "✅ Backup complete:"
ls -lh "$BUNDLE" "$TARBALL" | awk '{print "   " $5 "\t" $9}'
echo ""
echo "Restore with:"
echo "   bash scripts/restore.sh \"$BUNDLE\" ./restored-repo"
