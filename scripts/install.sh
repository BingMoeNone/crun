#!/usr/bin/env bash
set -euo pipefail

# ── crun installer ─────────────────────────────────────────────────────────────
# One-command install:
#   curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/install.sh | bash
#
# Environment variables:
#   CRUN_REPO        - GitHub repo (default: BingMoeNone/crun)
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

# Interactive confirmation: reads from /dev/tty to bypass curl pipe
read_confirm() {
  local prompt="$1"
  local answer
  if [[ -t 0 ]]; then
    read -r -p "$(printf "  ${CYAN}?${NC} ${prompt} [Y/n]: ")" answer
  elif [[ -e /dev/tty ]]; then
    read -r -p "$(printf "  ${CYAN}?${NC} ${prompt} [Y/n]: ")" answer < /dev/tty
  else
    echo "  (non-interactive, skipping)"
    return 1
  fi
  [[ "${answer,,}" != "n" && "${answer,,}" != "no" ]]
}

# ── Parse args ─────────────────────────────────────────────────────────────────
YES=false
case "${1:-}" in
  -h|--help)
    echo "Usage: curl -fsSL <install-url> | bash"
    echo ""
    echo "Environment variables:"
    echo "  CRUN_REPO         GitHub repo (default: BingMoeNone/crun)"
    echo "  CRUN_VERSION      version tag or 'latest' (default: latest)"
    echo "  CRUN_INSTALL_DIR  install path (default: /usr/local/bin or ~/.local/bin)"
    echo "  DEBUG=1           enable verbose output"
    echo ""
    echo "Options:"
    echo "  -y, --yes         skip confirmation prompts"
    echo ""
    echo "Examples:"
    echo "  curl -fsSL ... | bash                                # latest"
    echo "  curl -fsSL ... | bash -s -- -y                       # latest, no prompts"
    echo "  CRUN_VERSION=v0.4.0 curl -fsSL ... | bash             # specific version"
    echo "  DEBUG=1 curl -fsSL ... | bash                         # debug mode"
    exit 0
    ;;
  -y|--yes)
    YES=true
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
REPO="${CRUN_REPO:-BingMoeNone/crun}"
VERSION="${CRUN_VERSION:-latest}"

# Fetch the latest release tag from GitHub API (for version comparison).
# Returns empty string on failure.
fetch_latest_tag() {
  local tag
  tag="$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null \
    | grep -o '"tag_name": *"[^"]*"' | head -1 | cut -d'"' -f4)" || true
  echo "${tag}"
}

# Strip leading 'v' from a version string for comparison.
strip_v() { echo "${1#v}"; }

# Compare two version strings (semver). Returns 0 if $1 > $2.
ver_gt() {
  local a b i av bv
  IFS=. read -ra a <<< "$1"
  IFS=. read -ra b <<< "$2"
  for ((i=0; i<${#a[@]} || i<${#b[@]}; i++)); do
    av="${a[$i]:-0}"; bv="${b[$i]:-0}"
    if (( av > bv )); then return 0; fi
    if (( av < bv )); then return 1; fi
  done
  return 1  # equal
}

echo ""
printf "  ${BOLD}crun${NC} installer · ${CYAN}%s${NC} · %s\n" "${VERSION}" "${arch}"
[[ "${DEBUG}" != "0" ]] && warn "DEBUG mode enabled"
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
existing_ver_num=""
is_upgrade=false
if [[ -x "${INSTALL_DIR}/crun" ]]; then
  existing_version="$( "${INSTALL_DIR}/crun" --version 2>/dev/null || true )"
  # Extract version number: "crun 0.5.4" → "0.5.4"
  existing_ver_num="$(echo "${existing_version}" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)" || true
  if [[ -n "${existing_ver_num}" ]]; then
    is_upgrade=true
  fi
fi

# Determine target version for comparison
target_ver_num=""
if [[ "${VERSION}" != "latest" ]]; then
  target_ver_num="$(strip_v "${VERSION}")"
else
  info "Checking latest version..."
  latest_tag="$(fetch_latest_tag)"
  if [[ -n "${latest_tag}" ]]; then
    target_ver_num="$(strip_v "${latest_tag}")"
    debug "latest tag = ${latest_tag}, target_ver_num = ${target_ver_num}"
  fi
fi

# ── Upgrade prompt ─────────────────────────────────────────────────────────────
if ${is_upgrade}; then
  if [[ -n "${target_ver_num}" && -n "${existing_ver_num}" ]]; then
    if [[ "${existing_ver_num}" == "${target_ver_num}" ]]; then
      ok "Already up to date (v${existing_ver_num})"
      if ! ${YES}; then
        if ! read_confirm "Reinstall anyway?"; then
          echo ""
          info "Cancelled, nothing changed."
          exit 0
        fi
      fi
      echo ""
    elif ver_gt "${target_ver_num}" "${existing_ver_num}"; then
      info "New version available: v${existing_ver_num} → v${target_ver_num}"
      if ! ${YES}; then
        if ! read_confirm "Upgrade now?"; then
          echo ""
          info "Cancelled, current version kept (v${existing_ver_num})"
          exit 0
        fi
      fi
      echo ""
    else
      warn "Installed version (v${existing_ver_num}) is newer than latest release (v${target_ver_num})"
      info "You are using a pre-release or local build"
      if ! ${YES}; then
        if ! read_confirm "Overwrite with release v${target_ver_num}?"; then
          echo ""
          info "Cancelled, current version kept (v${existing_ver_num})"
          exit 0
        fi
      fi
      echo ""
    fi
  else
    info "Installed: ${existing_version:-unknown version}"
    if ! ${YES}; then
      if ! read_confirm "Overwrite existing installation?"; then
        echo ""
        info "Cancelled, nothing changed."
        exit 0
      fi
    fi
    echo ""
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
  --show-error
  --proto '=https'
  --tlsv1.2
  --retry 3
  --retry-delay 5
  --connect-timeout 30
  --max-time 600
)

if [[ "${DEBUG}" != "0" ]]; then
  CURL_ARGS+=(--verbose)
fi

info "Downloading ${asset} ..."
echo "  URL: ${binary_url}"
if ! curl "${CURL_ARGS[@]}" "${binary_url}" -o "${tmp_dir}/${asset}"; then
  echo ""
  err "Download failed (exit code: $?)
  Possible reasons:
  - Network connectivity issue
  - GitHub Release does not exist (version=${VERSION})
  - No ${arch} binary built for this version
  Visit https://github.com/${REPO}/releases to confirm release status"
fi
ok "Download complete ($(du -h "${tmp_dir}/${asset}" | cut -f1))"

info "Downloading checksum ..."
echo "  URL: ${checksum_url}"
if ! curl "${CURL_ARGS[@]}" "${checksum_url}" -o "${tmp_dir}/${asset}.sha256"; then
  warn "Could not download checksum (exit code: $?), skipping verification"
fi

# ── Verify checksum ────────────────────────────────────────────────────────────
if [[ -f "${tmp_dir}/${asset}.sha256" ]]; then
  info "Verifying SHA256 ..."
  if (cd "${tmp_dir}" && sha256sum -c "${asset}.sha256" 2>/dev/null); then
    ok "Checksum verified"
  else
    err "SHA256 checksum mismatch, file may be corrupted"
  fi
fi

# ── Install (atomic) ───────────────────────────────────────────────────────────
mkdir -p "${INSTALL_DIR}"

# Write to temp file on same filesystem, then mv for atomic replacement.
# This ensures no partial binary if interrupted mid-write.
tmp_bin="${INSTALL_DIR}/.crun.new.$$"
chmod 0755 "${tmp_dir}/${asset}"
cp "${tmp_dir}/${asset}" "${tmp_bin}"
# fsync the file and its directory to ensure durability
sync -f "${tmp_bin}" 2>/dev/null || true
mv -f "${tmp_bin}" "${INSTALL_DIR}/crun"
ok "Installed to ${INSTALL_DIR}/crun"

# ── Post-install verification ──────────────────────────────────────────────────
installed_version="$( "${INSTALL_DIR}/crun" --version 2>/dev/null || true )"
if [[ -z "${installed_version}" ]]; then
  err "Install verification failed: binary is not executable (${INSTALL_DIR}/crun --version produced no output)"
fi

# Extract new version number
new_ver_num="$(echo "${installed_version}" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)" || true

if ${is_upgrade}; then
  echo ""
  if [[ -n "${new_ver_num}" && -n "${existing_ver_num}" ]]; then
    if [[ "${new_ver_num}" == "${existing_ver_num}" ]]; then
      ok "Reinstalled: v${new_ver_num}"
    else
      ok "Upgrade complete: v${existing_ver_num} → v${new_ver_num}"
    fi
  else
    ok "Install complete: ${installed_version}"
  fi
else
  echo ""
  "${INSTALL_DIR}/crun" --version 2>/dev/null || true
fi

# ── Post-install ───────────────────────────────────────────────────────────────
echo ""

# Config preservation — installer only touches the binary, never ~/.config/crun/
CONFIG_DIR="${HOME}/.config/crun"
if ${is_upgrade}; then
  if [[ -d "${CONFIG_DIR}" ]]; then
    ok "User data preserved: ${CONFIG_DIR}"
    echo "  (preferences, history, presets, custom flags unchanged)"
  fi
else
  if [[ -d "${CONFIG_DIR}" ]]; then
    info "Existing user config found: ${CONFIG_DIR}"
    echo "  Installer will not overwrite any config files."
  fi
fi

# Detect shell rc file
detect_shell_rc() {
  local shell_name
  shell_name="$(basename "${SHELL:-/bin/bash}")"
  case "${shell_name}" in
    zsh)  echo "${HOME}/.zshrc" ;;
    bash) echo "${HOME}/.bashrc" ;;
    *)    echo "${HOME}/.profile" ;;
  esac
}

SHELL_RC="$(detect_shell_rc)"

# Check for claude command
if ! command -v claude >/dev/null 2>&1; then
  warn "'claude' command not found in PATH. Please install Claude Code CLI first"
  echo "  https://docs.anthropic.com/en/docs/claude-code/overview"
  echo ""
fi

# Check PATH
if [[ ":${PATH}:" == *":${INSTALL_DIR}:"* ]]; then
  ok "crun is ready, type 'crun' to start"
  printf "  ${BOLD}Run 'crun' to get started.${NC}\n"
  echo ""
  exit 0
fi

warn "${INSTALL_DIR} is not in PATH"

if read_confirm "Add ${INSTALL_DIR} to PATH (${SHELL_RC})?"; then
  echo ""

  # Check if already configured
  if grep -q "export PATH=\"${INSTALL_DIR}:\$PATH\"" "${SHELL_RC}" 2>/dev/null; then
    ok "PATH entry already exists in ${SHELL_RC}, skipping"
  else
    echo "" >> "${SHELL_RC}"
    echo "# crun" >> "${SHELL_RC}"
    echo "export PATH=\"${INSTALL_DIR}:\$PATH\"" >> "${SHELL_RC}"
    ok "Added PATH configuration to ${SHELL_RC}"
  fi

  # Apply to current shell
  export PATH="${INSTALL_DIR}:${PATH}"
  ok "Effective in current session"

  echo ""
  printf "  ${BOLD}Run 'crun' to get started.${NC}\n"
else
  echo ""
  echo "  To add later, append the following line to ${SHELL_RC}:"
  printf "    ${BOLD}export PATH=\"%s:\$PATH\"${NC}\n" "${INSTALL_DIR}"
  echo "  Then run: source ${SHELL_RC}"
  echo ""
fi

echo ""
