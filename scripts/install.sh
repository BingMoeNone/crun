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

DEBUG="${DEBUG:-0}"

info()  { printf "  ${CYAN}→${NC} %s\n" "$*"; }
ok()    { printf "  ${GREEN}✓${NC} %s\n" "$*"; }
warn()  { printf "  ${YELLOW}⚠${NC} %s\n" "$*" >&2; }
err()   { printf "${RED}${BOLD}✗ Error:${NC} %s\n" "$*" >&2; exit 1; }
debug() { if [[ "${DEBUG}" != "0" ]]; then printf "  ${CYAN}[DEBUG]${NC} %s\n" "$*"; fi }

# ── Parse args ─────────────────────────────────────────────────────────────────
case "${1:-}" in
  -h|--help)
    echo "Usage: curl -fsSL <install-url> | bash"
    echo ""
    echo "Environment variables:"
    echo "  CRUN_REPO         GitHub repo (default: BingMoeNone/claude-run)"
    echo "  CRUN_VERSION      version tag or 'latest' (default: latest)"
    echo "  CRUN_INSTALL_DIR  install path (default: /usr/local/bin or ~/.local/bin)"
    echo "  DEBUG=1           enable verbose output"
    echo ""
    echo "Examples:"
    echo "  curl -fsSL ... | bash                                # latest"
    echo "  CRUN_VERSION=v0.4.0 curl -fsSL ... | bash             # specific version"
    echo "  DEBUG=1 curl -fsSL ... | bash                         # debug mode"
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
[[ "${DEBUG}" != "0" ]] && warn "DEBUG 模式已开启"
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

binary_url="${base_url}/${asset}"
checksum_url="${base_url}/${asset}.sha256"

debug "REPO      = ${REPO}"
debug "VERSION   = ${VERSION}"
debug "arch      = ${arch}"
debug "asset     = ${asset}"
debug "binary    = ${binary_url}"
debug "checksum  = ${checksum_url}"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "${tmp_dir}"' EXIT
debug "tmp_dir   = ${tmp_dir}"

CURL_ARGS=(
  --fail
  --location
  --progress-bar
  --show-error
  --proto '=https'
  --tlsv1.2
  --retry 3
  --connect-timeout 30
  --max-time 600
)

if [[ "${DEBUG}" != "0" ]]; then
  CURL_ARGS+=(--verbose)
fi

info "下载 ${asset} ..."
echo "  URL: ${binary_url}"
if ! curl "${CURL_ARGS[@]}" "${binary_url}" -o "${tmp_dir}/${asset}"; then
  echo ""
  err "下载失败 (exit code: $?)
  可能的原因:
  - 网络连接问题
  - GitHub Release 不存在 (version=${VERSION})
  - 该版本未构建 ${arch} 架构产物
  请访问 https://github.com/${REPO}/releases 确认 Release 状态"
fi
ok "下载完成 ($(du -h "${tmp_dir}/${asset}" | cut -f1))"

info "下载校验和 ..."
echo "  URL: ${checksum_url}"
if ! curl "${CURL_ARGS[@]}" "${checksum_url}" -o "${tmp_dir}/${asset}.sha256"; then
  warn "无法下载校验和 (exit code: $?)，跳过校验"
fi

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
