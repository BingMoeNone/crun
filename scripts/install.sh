#!/usr/bin/env bash
set -euo pipefail

REPO="${CLAUDE_RUN_REPO:-BingMoeNone/claude-run}"
VERSION="${CLAUDE_RUN_VERSION:-latest}"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Error: only Linux is supported." >&2
  exit 1
fi

arch_raw="$(uname -m)"
case "${arch_raw}" in
  x86_64) arch="amd64" ;;
  aarch64|arm64) arch="arm64" ;;
  *)
    echo "Error: unsupported architecture: ${arch_raw}" >&2
    exit 1
    ;;
esac

for cmd in curl sha256sum install mktemp; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: required command not found: ${cmd}" >&2
    exit 1
  fi
done

if [[ -z "${CLAUDE_RUN_INSTALL_DIR:-}" ]]; then
  if [[ -w /usr/local/bin ]]; then
    INSTALL_DIR="/usr/local/bin"
  else
    INSTALL_DIR="${HOME}/.local/bin"
  fi
else
  INSTALL_DIR="${CLAUDE_RUN_INSTALL_DIR}"
fi

mkdir -p "${INSTALL_DIR}"

asset="claude-run-linux-${arch}"
if [[ "${VERSION}" == "latest" ]]; then
  base_url="https://github.com/${REPO}/releases/latest/download"
else
  base_url="https://github.com/${REPO}/releases/download/${VERSION}"
fi

binary_url="${base_url}/${asset}"
checksum_url="${base_url}/${asset}.sha256"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

echo "Downloading ${asset} from ${binary_url}"
curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 --retry 3 \
  "${binary_url}" -o "${tmp_dir}/${asset}"

curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 --retry 3 \
  "${checksum_url}" -o "${tmp_dir}/${asset}.sha256"

(
  cd "${tmp_dir}"
  sha256sum -c "${asset}.sha256"
)

install -m 0755 "${tmp_dir}/${asset}" "${INSTALL_DIR}/claude-run"

echo "Installed: ${INSTALL_DIR}/claude-run"

if ! command -v claude >/dev/null 2>&1; then
  echo "Warning: 'claude' command is not found in PATH. Please install Claude Code CLI first." >&2
fi

case ":${PATH}:" in
  *":${INSTALL_DIR}:"*) ;;
  *)
    echo "Note: ${INSTALL_DIR} is not in your PATH."
    echo "Add this line to your shell profile:"
    echo "  export PATH=\"${INSTALL_DIR}:\$PATH\""
    ;;
esac

echo "Done. Run: claude-run"