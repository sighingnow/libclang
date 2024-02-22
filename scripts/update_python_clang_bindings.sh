#! /bin/bash
set -euo pipefail

TOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"

LLVM_VERSION="${LLVM_VERSION:-17.0.6}"
LLVM_URL_PREFIX="https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-${LLVM_VERSION}/clang/bindings/python"

LISTING=(
  "clang/__init__.py"
  "clang/cindex.py"
  "clang/enumerations.py"
)

function run() {
  echo >&2 "$*"
  "$@"
}

BINDINGS_DIR="${TOP_DIR}/python"

for clang_py_file in "${LISTING[@]}"; do
  run curl --insecure -fsSL "${LLVM_URL_PREFIX}/${clang_py_file}" -o "${BINDINGS_DIR}/${clang_py_file}"
done

pushd "${TOP_DIR}" > /dev/null
run patch -p1 < "${TOP_DIR}/scripts/data/clang_bindings.patch"
popd > /dev/null
