#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOTSTRAP_SH="$REPO_ROOT/scripts/bootstrap_and_demo.sh"
BOOTSTRAP_PS1="$REPO_ROOT/scripts/bootstrap_and_demo.ps1"
STAGING_DIR="$REPO_ROOT/dist/bootstrap"
GH_TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
export GH_TOKEN

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. Install it from https://cli.github.com/ and ensure GH_TOKEN/GITHUB_TOKEN is set." >&2
  exit 1
fi

if [[ -z "$GH_TOKEN" ]]; then
  echo "GH_TOKEN or GITHUB_TOKEN must be set for non-interactive uploads." >&2
  exit 1
fi

for file in "$BOOTSTRAP_SH" "$BOOTSTRAP_PS1"; do
  if [ ! -f "$file" ]; then
    echo "Missing required script: $file" >&2
    exit 1
  fi
done

mkdir -p "$STAGING_DIR"
cp "$BOOTSTRAP_SH" "$STAGING_DIR/"
cp "$BOOTSTRAP_PS1" "$STAGING_DIR/"

RELEASE_TAG=$(gh release list --limit 1 --json tagName --jq '.[0].tagName' 2>/dev/null || true)
if [ -z "$RELEASE_TAG" ]; then
  echo "No release found. Create a release (e.g., v0.1.0) before uploading bootstrap assets." >&2
  exit 1
fi

STAGED_SH="$STAGING_DIR/$(basename "$BOOTSTRAP_SH")"
STAGED_PS1="$STAGING_DIR/$(basename "$BOOTSTRAP_PS1")"

gh release upload "$RELEASE_TAG" "$STAGED_SH" "$STAGED_PS1" --clobber

echo "Bootstrap distribution updated:"
echo "- $(basename "$BOOTSTRAP_SH")"
echo "- $(basename "$BOOTSTRAP_PS1")"
