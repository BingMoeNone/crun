#!/usr/bin/env bash
set -euo pipefail

# ── crun uninstaller ────────────────────────────────────────────────────────────
# One-command uninstall:
#   curl -fsSL https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/uninstall.sh | bash
#
# Or download and run manually:
#   bash uninstall.sh
# ─────────────────────────────────────────────────────────────────────────────────

# ── Helpers ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
BOLD='\033[1m'

info()  { printf "  ${CYAN}→${NC} %s\n" "$*"; }
ok()    { printf "  ${GREEN}✓${NC} %s\n" "$*"; }
warn()  { printf "  ${YELLOW}⚠${NC} %s\n" "$*" >&2; }
err()   { printf "${RED}${BOLD}✗ Error:${NC} %s\n" "$*" >&2; exit 1; }

YES=false
case "${1:-}" in
  -h|--help)
    echo "Usage: curl -fsSL <uninstall-url> | bash"
    echo ""
    echo "Options:"
    echo "  -y, --yes    skip confirmation prompts (full uninstall)"
    echo ""
    echo "Modes:"
    echo "  1) Soft uninstall  — remove binary only, keep user config"
    echo "  2) Full uninstall  — remove binary + all user data"
    exit 0
    ;;
  -y|--yes)
    YES=true
    ;;
esac

# 交互式询问
read_confirm() {
  local prompt="$1"
  local answer
  if [[ "${YES}" == "true" ]]; then
    return 0
  fi
  if [[ -t 0 ]]; then
    read -r -p "$(printf "  ${CYAN}?${NC} ${prompt} [y/N]: ")" answer
  elif [[ -e /dev/tty ]]; then
    read -r -p "$(printf "  ${CYAN}?${NC} ${prompt} [y/N]: ")" answer < /dev/tty
  else
    echo "  (非交互模式，跳过)"
    return 1
  fi
  [[ "${answer,,}" == "y" || "${answer,,}" == "yes" ]]
}

# ── Find installed binary ───────────────────────────────────────────────────────
echo ""
printf "  ${BOLD}crun${NC} uninstaller\n"
echo ""

BINARY=""
BINARY_PATH=""

# Check common install locations
for loc in "/usr/local/bin/crun" "${HOME}/.local/bin/crun"; do
  if [[ -x "${loc}" ]]; then
    BINARY="${loc}"
    BINARY_PATH="${loc}"
    break
  fi
done

# Fallback: check PATH
if [[ -z "${BINARY}" ]]; then
  BINARY_PATH="$(command -v crun 2>/dev/null || true)"
  if [[ -n "${BINARY_PATH}" && -x "${BINARY_PATH}" ]]; then
    BINARY="${BINARY_PATH}"
  fi
fi

# Get version
VERSION=""
if [[ -n "${BINARY}" ]]; then
  VERSION="$("${BINARY}" --version 2>/dev/null || true)"
fi

# Config directories
CONFIG_DIR="${HOME}/.config/crun"
OLD_CONFIG_DIR="${HOME}/.config/claude-run"

# ── Status ──────────────────────────────────────────────────────────────────────
if [[ -n "${BINARY}" ]]; then
  info "Found: ${BINARY}  (${VERSION:-unknown version})"
else
  warn "Binary not found in standard locations."
fi

has_config=false
if [[ -d "${CONFIG_DIR}" ]]; then
  info "Config found: ${CONFIG_DIR}"
  has_config=true
fi
if [[ -d "${OLD_CONFIG_DIR}" ]]; then
  info "Legacy config found: ${OLD_CONFIG_DIR}"
  has_config=true
fi

if [[ -z "${BINARY}" && "${has_config}" == "false" ]]; then
  ok "Nothing to uninstall — crun is not installed on this system."
  exit 0
fi

echo ""

# ── Choose mode ─────────────────────────────────────────────────────────────────
if ${YES}; then
  MODE="full"
else
  echo "  Uninstall mode:"
  echo "    1) Soft uninstall — remove binary only, keep all user data"
  echo "    2) Full uninstall — remove binary + all config / preferences / history"
  echo "    q) Cancel"
  echo ""

  read -r -p "$(printf "  ${CYAN}?${NC} Choice [1/2/q]: ")" choice
  case "${choice}" in
    1) MODE="soft" ;;
    2) MODE="full" ;;
    q|Q|"") echo ""; info "Cancelled, nothing removed."; exit 0 ;;
    *) echo ""; info "Invalid choice, cancelled."; exit 0 ;;
  esac
  echo ""
fi

# ── Confirm ─────────────────────────────────────────────────────────────────────
if [[ "${MODE}" == "full" ]]; then
  echo "  Full uninstall will remove:"
  [[ -n "${BINARY}" ]] && echo "    — Binary: ${BINARY}"
  [[ -d "${CONFIG_DIR}" ]] && echo "    — Config: ${CONFIG_DIR}"
  [[ -d "${OLD_CONFIG_DIR}" ]] && echo "    — Legacy: ${OLD_CONFIG_DIR}"
  echo ""
  if ! read_confirm "This will delete ALL crun data. Proceed?"; then
    info "Cancelled, nothing removed."
    exit 0
  fi
else
  [[ -n "${BINARY}" ]] && echo "  Will remove: ${BINARY}"
  [[ "${has_config}" == "true" ]] && echo "  Config will be preserved."
  echo ""
  if ! read_confirm "Remove the crun binary?"; then
    info "Cancelled, nothing removed."
    exit 0
  fi
fi

echo ""

# ── Execute ─────────────────────────────────────────────────────────────────────
removed_any=false

if [[ -n "${BINARY}" && -f "${BINARY}" ]]; then
  rm -f "${BINARY}"
  ok "Removed: ${BINARY}"
  removed_any=true
fi

if [[ "${MODE}" == "full" ]]; then
  if [[ -d "${CONFIG_DIR}" ]]; then
    rm -rf "${CONFIG_DIR}"
    ok "Removed: ${CONFIG_DIR}"
    removed_any=true
  fi
  if [[ -d "${OLD_CONFIG_DIR}" ]]; then
    rm -rf "${OLD_CONFIG_DIR}"
    ok "Removed: ${OLD_CONFIG_DIR}"
    removed_any=true
  fi
else
  if [[ -d "${CONFIG_DIR}" ]]; then
    ok "Preserved: ${CONFIG_DIR}"
  fi
  if [[ -d "${OLD_CONFIG_DIR}" ]]; then
    ok "Preserved: ${OLD_CONFIG_DIR}"
  fi
fi

if ${removed_any}; then
  echo ""
  ok "Uninstall complete."
else
  echo ""
  warn "Nothing was removed."
fi

echo ""
