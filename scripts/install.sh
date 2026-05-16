#!/usr/bin/env bash
set -euo pipefail

# ── crun installer ─────────────────────────────────────────────────────────────
# One-command install:
#   curl -fsSL https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.sh | bash
#
# Environment variables:
#   CRUN_REPO        - GitHub repo (default: BingMoeNone/claude-run)
#   CRUN_VERSION     - version tag or "latest" (default: latest)
#   CRUN_INSTALL_DIR - install directory (default: /usr/local/bin or ~/.local/bin)
# ───────────────────────────────────────────────────────────────────────────────

# ── Helpers ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
BOLD='\033[1m'

info()  { printf "  ${CYAN}→${NC} %s\n" "$*"; }
ok()    { printf "  ${GREEN}✓${NC} %s\n" "$*"; }
warn()  { printf "  ${YELLOW}⚠${NC} %s\n" "$*" >&2; }
err()   { printf "${RED}${BOLD}✗ Error:${NC} %s\n" "$*" >&2; exit 1; }

# ── Parse args ─────────────────────────────────────────────────────────────────
case "${1:-}" in
  -h|--help)
    echo "Usage: curl -fsSL <install-url> | bash"
    echo ""
    echo "Environment variables:"
    echo "  CRUN_REPO         GitHub repo (default: BingMoeNone/claude-run)"
    echo "  CRUN_VERSION      version tag or 'latest' (default: latest)"
    echo "  CRUN_INSTALL_DIR  install path (default: /usr/local/bin or ~/.local/bin)"
    echo ""
    echo "Examples:"
    echo "  curl -fsSL ... | bash                    # latest"
    echo "  CRUN_VERSION=v0.2.0 curl -fsSL ... | bash # specific version"
    exit 0
    ;;
esac

# ── Platform check ─────────────────────────────────────────────────────────────
OS="$(uname -s)"
if [[ "${OS}" != "Linux" ]]; then
  err "only Linux is supported (detected: ${OS})"
fi

arch_raw="$(uname -m)"
case "${arch_raw}" in
  x86_64)       arch="amd64" ;;
  aarch64|arm64) arch="arm64" ;;
  *)            err "unsupported architecture: ${arch_raw}" ;;
esac

# ── Dependency check ───────────────────────────────────────────────────────────
for cmd in curl sha256sum install mktemp; do
  command -v "${cmd}" >/dev/null 2>&1 || err "required command not found: ${cmd}"
done

# ── Banner ─────────────────────────────────────────────────────────────────────
REPO="${CRUN_REPO:-BingMoeNone/claude-run}"
VERSION="${CRUN_VERSION:-latest}"

echo ""
printf "  ${BOLD}crun${NC} installer · ${CYAN}%s${NC} · %s\n" "${VERSION}" "${arch}"
echo ""

# ── Determine install dir ──────────────────────────────────────────────────────
if [[ -z "${CRUN_INSTALL_DIR:-}" ]]; then
  if [[ -w /usr/local/bin ]]; then
    INSTALL_DIR="/usr/local/bin"
  else
    INSTALL_DIR="${HOME}/.local/bin"
  fi
else
  INSTALL_DIR="${CRUN_INSTALL_DIR}"
fi

# ── Check existing installation ────────────────────────────────────────────────
existing_version=""
if [[ -x "${INSTALL_DIR}/crun" ]]; then
  existing_version="$( "${INSTALL_DIR}/crun" --version 2>/dev/null || true )"
  if [[ -n "${existing_version}" ]]; then
    if [[ "${VERSION}" == "latest" ]]; then
      info "已安装 ${existing_version}，检查更新..."
    else
      info "已安装 ${existing_version}，替换为 ${VERSION}..."
    fi
  fi
fi

# ── Download ───────────────────────────────────────────────────────────────────
asset="crun-linux-${arch}"

if [[ "${VERSION}" == "latest" ]]; then
  base_url="https://github.com/${REPO}/releases/latest/download"
else
  base_url="https://github.com/${REPO}/releases/download/${VERSION}"
fi

tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT

info "下载 ${asset} ..."
curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 --retry 3 \
  "${base_url}/${asset}" -o "${tmp_dir}/${asset}" || {
  err "下载失败，请检查网络连接或版本号是否正确: ${VERSION}"
}

info "下载校验和 ..."
curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 --retry 3 \
  "${base_url}/${asset}.sha256" -o "${tmp_dir}/${asset}.sha256" || {
  warn "无法下载校验和，跳过校验"
}

# ── Verify checksum ────────────────────────────────────────────────────────────
if [[ -f "${tmp_dir}/${asset}.sha256" ]]; then
  info "校验 SHA256 ..."
  if (cd "${tmp_dir}" && sha256sum -c "${asset}.sha256" 2>/dev/null); then
    ok "校验通过"
  else
    err "SHA256 校验失败，文件可能已损坏"
  fi
fi

# ── Install ────────────────────────────────────────────────────────────────────
mkdir -p "${INSTALL_DIR}"
install -m 0755 "${tmp_dir}/${asset}" "${INSTALL_DIR}/crun"
ok "已安装到 ${INSTALL_DIR}/crun"

# ── Verify installed binary ────────────────────────────────────────────────────
if [[ -z "${existing_version}" ]]; then
  installed_version="$( "${INSTALL_DIR}/crun" --version 2>/dev/null || true )"
  [[ -n "${installed_version}" ]] && echo "" && "${INSTALL_DIR}/crun" --version 2>/dev/null || true
fi

# ── Post-install checks ────────────────────────────────────────────────────────
echo ""

if ! command -v claude >/dev/null 2>&1; then
  warn "系统中未找到 'claude' 命令，请先安装 Claude Code CLI: https://docs.anthropic.com/en/docs/claude-code/overview"
  echo ""
fi

case ":${PATH}:" in
  *":${INSTALL_DIR}:"*) ;;
  *)
    warn "${INSTALL_DIR} 不在 PATH 中"
    echo ""
    echo "  将以下行添加到 shell 配置文件 (~/.bashrc / ~/.zshrc):"
    printf "    ${BOLD}export PATH=\"%s:\$PATH\"${NC}\n" "${INSTALL_DIR}"
    echo "  然后执行 source ~/.bashrc (或 ~/.zshrc) 使其生效。"
    echo ""
    ;;
esac

echo "  ${BOLD}运行 crun 开始使用。${NC}"
echo ""
