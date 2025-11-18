#!/usr/bin/env bash
set -euo pipefail

if ! make -n >/dev/null 2>&1; then
  echo "Makefile syntax error detected"
  exit 1
fi

echo "Makefile syntax OK"
