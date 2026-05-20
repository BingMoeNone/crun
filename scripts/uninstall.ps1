<#
.SYNOPSIS
  crun uninstaller for Windows

.DESCRIPTION
  One-command uninstall:
    irm https://raw.githubusercontent.com/BingMoeNone/crun/main/scripts/uninstall.ps1 | iex

  Or download and run manually:
    .\uninstall.ps1

.PARAMETER Mode
  -y, --yes    skip confirmation prompts (full uninstall)
#>

param(
  [string]$Arg1
)

$YesMode = $false

if ($Arg1 -eq '-h' -or $Arg1 -eq '--help') {
  Write-Host @"
Usage: irm <uninstall-url> | iex

Options:
  -y, --yes    skip confirmation prompts (full uninstall)

Modes:
  1) Soft uninstall — remove binary only, keep user config
  2) Full uninstall — remove binary + all user data
"@
  exit 0
}

if ($Arg1 -eq '-y' -or $Arg1 -eq '--yes') {
  $YesMode = $true
}

function Main {
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Helpers ───────────────────────────────────────────────────────────────
$esc = [char]27
[string]$GREEN  = "$esc[0;32m"
[string]$YELLOW = "$esc[1;33m"
[string]$CYAN   = "$esc[0;36m"
[string]$NC     = "$esc[0m"

function info($msg)  { Write-Host "  ${CYAN}->${NC} $msg" }
function ok($msg)    { Write-Host "  ${GREEN}+${NC} $msg" }
function warn($msg)  { Write-Host "  ${YELLOW}!${NC} $msg" }
function err($msg)   { Write-Host "  ERROR: $msg" -ForegroundColor Red; throw "Uninstall failed" }

function Confirm-User($prompt) {
  if ($YesMode) { return $true }
  try {
    $choice = Read-Host "$prompt [y/N]"
    return ($choice -eq 'y' -or $choice -eq 'yes')
  } catch {
    Write-Host "  (non-interactive, skipping)"
    return $false
  }
}

# ── Banner ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  crun uninstaller"
Write-Host ""

# ── Find installed binary ──────────────────────────────────────────────────
[string]$binaryPath = ""
[string]$version = ""

# Check Get-Command first
$cmd = Get-Command crun.exe -ErrorAction SilentlyContinue
if ($cmd) {
  $binaryPath = $cmd.Source
}

# Also check standard install location
$stdPath = Join-Path $env:LOCALAPPDATA "Programs\crun\crun.exe"
if ((-not $binaryPath) -and (Test-Path $stdPath)) {
  $binaryPath = $stdPath
}

if ($binaryPath) {
  try {
    $version = (& $binaryPath --version 2>$null) -join ''
  } catch { }
}

# Config directories
$configDir = Join-Path $env:LOCALAPPDATA "crun"

# ── Status ─────────────────────────────────────────────────────────────────
if ($binaryPath) {
  info "Found: $binaryPath  ($(if ($version) { $version } else { 'unknown version' }))"
} else {
  warn "Binary not found in standard locations."
}

$hasConfig = $false
if (Test-Path $configDir) {
  info "Config found: $configDir"
  $hasConfig = $true
}

if ((-not $binaryPath) -and (-not $hasConfig)) {
  ok "Nothing to uninstall — crun is not installed on this system."
  return
}

Write-Host ""

# ── Choose mode ────────────────────────────────────────────────────────────
[string]$Mode = ""
if ($YesMode) {
  $Mode = "full"
} else {
  Write-Host "  Uninstall mode:"
  Write-Host "    1) Soft uninstall — remove binary only, keep all user data"
  Write-Host "    2) Full uninstall — remove binary + all config / preferences / history"
  Write-Host "    q) Cancel"
  Write-Host ""

  try {
    $choice = Read-Host "Choice [1/2/q]"
  } catch {
    Write-Host ""
    info "Cancelled, nothing removed."
    return
  }

  switch ($choice) {
    "1" { $Mode = "soft" }
    "2" { $Mode = "full" }
    "q" { Write-Host ""; info "Cancelled, nothing removed."; return }
    default { Write-Host ""; info "Invalid choice, cancelled."; return }
  }
  Write-Host ""
}

# ── Confirm ────────────────────────────────────────────────────────────────
if ($Mode -eq "full") {
  Write-Host "  Full uninstall will remove:"
  if ($binaryPath) { Write-Host "    — Binary: $binaryPath" }
  if (Test-Path $configDir) { Write-Host "    — Config: $configDir" }
  Write-Host ""
  if (-not (Confirm-User "This will delete ALL crun data. Proceed?")) {
    info "Cancelled, nothing removed."
    return
  }
} else {
  if ($binaryPath) { Write-Host "  Will remove: $binaryPath" }
  if ($hasConfig) { Write-Host "  Config will be preserved." }
  Write-Host ""
  if (-not (Confirm-User "Remove the crun binary?")) {
    info "Cancelled, nothing removed."
    return
  }
}

Write-Host ""

# ── Execute ────────────────────────────────────────────────────────────────
$removedAny = $false

if ($binaryPath -and (Test-Path $binaryPath)) {
  Remove-Item $binaryPath -Force
  ok "Removed: $binaryPath"
  $removedAny = $true
}

if ($Mode -eq "full") {
  if (Test-Path $configDir) {
    Remove-Item $configDir -Recurse -Force
    ok "Removed: $configDir"
    $removedAny = $true
  }
} else {
  if (Test-Path $configDir) {
    ok "Preserved: $configDir"
  }
}

if ($removedAny) {
  Write-Host ""
  ok "Uninstall complete."
} else {
  Write-Host ""
  warn "Nothing was removed."
}

Write-Host ""
}
Main
