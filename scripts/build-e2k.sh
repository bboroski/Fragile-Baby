#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
BUILD_DIR=${FB_E2K_BUILD_DIR:-"$ROOT_DIR/build-e2k"}
CMAKE=${CMAKE:-cmake}

"$CMAKE" -S "$ROOT_DIR" -B "$BUILD_DIR" \
  -DCMAKE_TOOLCHAIN_FILE="$ROOT_DIR/cmake/toolchains/e2k-linux.cmake" \
  -DE2K_CC="${E2K_CC:-}" \
  -DE2K_SYSROOT="${E2K_SYSROOT:-}" \
  -DE2K_QEMU="${E2K_QEMU:-}" \
  -DFB_E2K_GENERATION="${FB_E2K_GENERATION:-0}" \
  -DFB_E2K_ADDRESS_MODEL="${FB_E2K_ADDRESS_MODEL:-64}" \
  -DCMAKE_BUILD_TYPE="${CMAKE_BUILD_TYPE:-Release}"

"$CMAKE" --build "$BUILD_DIR" --parallel "${JOBS:-2}"

if [ "${FB_RUN_E2K_TESTS:-0}" = "1" ]; then
  "$CMAKE" -E env ctest --test-dir "$BUILD_DIR" --output-on-failure
fi
