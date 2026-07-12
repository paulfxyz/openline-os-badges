#!/usr/bin/env bash
# restore.sh — rebuild the repo from a backup made by backup.sh.
#
# Works with either artifact:
#   • a .bundle  → full git clone (history preserved)
#   • a .tar.gz  → flat file extraction (no git history)
#
# Usage:
#     bash scripts/restore.sh <backup-file> <destination-dir>
#
# Examples:
#     bash scripts/restore.sh backups/openline-os-badges-20260712T053000Z.bundle ./restored
#     bash scripts/restore.sh backups/openline-os-badges-20260712T053000Z.tar.gz  ./restored
set -euo pipefail

SRC="${1:-}"
DEST="${2:-}"

if [[ -z "$SRC" || -z "$DEST" ]]; then
  echo "Usage: bash scripts/restore.sh <backup-file(.bundle|.tar.gz)> <destination-dir>" >&2
  exit 1
fi
if [[ ! -f "$SRC" ]]; then
  echo "❌ Backup file not found: $SRC" >&2
  exit 1
fi
if [[ -e "$DEST" ]]; then
  echo "❌ Destination already exists: $DEST (choose an empty path)" >&2
  exit 1
fi

case "$SRC" in
  *.bundle)
    echo "→ Restoring from git bundle (full history)…"
    git clone "$SRC" "$DEST"
    echo "✅ Restored to $DEST"
    echo "   Re-point origin at the live remote when ready:"
    echo "     git -C \"$DEST\" remote set-url origin <primary-repo-url>"
    ;;
  *.tar.gz|*.tgz)
    echo "→ Restoring from tarball (files only, no git history)…"
    mkdir -p "$DEST"
    tar -xzf "$SRC" -C "$DEST"
    echo "✅ Restored files to $DEST"
    ;;
  *)
    echo "❌ Unrecognized backup type: $SRC (expected .bundle or .tar.gz)" >&2
    exit 1
    ;;
esac
