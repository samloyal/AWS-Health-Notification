#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
OUT="$PWD/function/requests-layer-python314.zip"
PLATFORM="${LAMBDA_PLATFORM:-x86_64-manylinux2014}"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT

uv export --frozen --no-hashes --no-emit-project --only-group lambda --output-file "$BUILD/requirements.txt"
uv pip install --quiet --target "$BUILD/python" \
  --python-platform "$PLATFORM" --python-version 3.14 \
  --only-binary :all: -r "$BUILD/requirements.txt"

rm -f "$OUT"
(cd "$BUILD" && zip -qr "$OUT" python)
echo "built $OUT for $PLATFORM"
