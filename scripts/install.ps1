<#
.SYNOPSIS
  crun installer for Windows

.DESCRIPTION
  One-command install:
    irm https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.ps1 | iex

  Or download and run manually:
    .\install.ps1

.ENVIRONMENT VARIABLES
  CRUN_REPO         - GitHub repo (default: BingMoeNone/claude-run)
  CRUN_VERSION      - version tag or "latest" (default: latest)
  CRUN_INSTALL_DIR  - install directory (default: $env:LOCALAPPDATA\Programs\crun)
  DEBUG             - $true for verbose output
#>

param(
  [string]$Arg1
)

# handle -h / --help
if ($Arg1 -eq '-h' -or $Arg1 -eq '--help') {
  Write-Host @"
Usage: irm <install-url> | iex
Environment variables:
  CRUN_REPO          GitHub repo (default: BingMoeNone/claude-run)
  CRUN_VERSION       version tag or 'latest' (default: latest)
  CRUN_INSTALL_DIR   install path (default: `$env:LOCALAPPDATA\Programs\crun)
  `$env:DEBUG=`$true  enable verbose output
Examples:
  irm ... | iex                                     # latest
  `$env:CRUN_VERSION='v0.4.0'; irm ... | iex         # specific version
"@
  exit 0
}

function Main {
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Helpers ───────────────────────────────────────────────────────────────
[string]$GREEN  = "`e[0;32m"
[string]$YELLOW = "`e[1;33m"
[string]$CYAN   = "`e[0;36m"
[string]$NC     = "`e[0m"

$DebugMode = [bool]($env:DEBUG -eq "1" -or $env:DEBUG -eq "true")

function info($msg)  { Write-Host "  ${CYAN}->${NC} $msg" }
function ok($msg)    { Write-Host "  ${GREEN}+${NC} $msg" }
function warn($msg)  { Write-Host "  ${YELLOW}!${NC} $msg" }
function err($msg)   { Write-Host "  ERROR: $msg" -ForegroundColor Red; throw $msg }
function debug($msg) { if ($DebugMode) { Write-Host "  [DEBUG] $msg" -ForegroundColor DarkGray } }

# ── Platform check ─────────────────────────────────────────────────────────
if ($env:OS -ne "Windows_NT") {
  err "crun installer: Windows only"
}

$arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { err "64-bit Windows required" }

# ── Banner ─────────────────────────────────────────────────────────────────
[string]$Repo    = if ($env:CRUN_REPO)    { $env:CRUN_REPO }    else { "BingMoeNone/claude-run" }
[string]$Version = if ($env:CRUN_VERSION) { $env:CRUN_VERSION } else { "latest" }

Write-Host ""
Write-Host "  crun installer · $Version · $arch"
if ($DebugMode) { warn "DEBUG mode enabled" }
Write-Host ""

# ── Determine install dir ──────────────────────────────────────────────────
if ($env:CRUN_INSTALL_DIR) {
  [string]$InstallDir = $env:CRUN_INSTALL_DIR
} else {
  $InstallDir = Join-Path $env:LOCALAPPDATA "Programs\crun"
}

# ── Check existing installation ────────────────────────────────────────────
[string]$existingVersion = ""
$isUpgrade = $false
$cmd = Get-Command crun.exe -ErrorAction SilentlyContinue
$existingPath = if ($cmd) { $cmd.Source } else { $null }
if ($existingPath) {
  try {
    $existingVersion = (& $existingPath --version 2>$null) -join ''
    if ($existingVersion) {
      $isUpgrade = $true
      if ($Version -eq "latest") {
        info "Installed: $existingVersion, checking for updates..."
      } elseif ($existingVersion -like "*$Version*") {
        info "Installed: $existingVersion, re-installing..."
      } else {
        info "Installed: $existingVersion -> upgrade to $Version..."
      }
    }
  } catch { }
}

# ── Download ───────────────────────────────────────────────────────────────
[string]$Asset = "crun-windows-$arch.exe"

if ($Version -eq "latest") {
  [string]$BaseUrl = "https://github.com/$Repo/releases/latest/download"
} else {
  [string]$BaseUrl = "https://github.com/$Repo/releases/download/$Version"
}

[string]$BinaryUrl    = "$BaseUrl/$Asset"
[string]$ChecksumUrl  = "$BaseUrl/$Asset.sha256"

debug "REPO     = $Repo"
debug "VERSION  = $Version"
debug "arch     = $arch"
debug "asset    = $Asset"
debug "binary   = $BinaryUrl"
debug "checksum = $ChecksumUrl"

$TempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item $_ -ItemType Directory -Force }
debug "temp_dir = $TempDir"

# Ensure temp directory is always cleaned up on any exit
try {

$dlPath = Join-Path $TempDir $Asset

info "Downloading $Asset ..."
Write-Host "  URL: $BinaryUrl"
Write-Host "  Size: ~12MB, please wait..."

try {
  Invoke-WebRequest -Uri $BinaryUrl -OutFile $dlPath -UseBasicParsing -MaximumRetryCount 3 -RetryIntervalSec 5
} catch {
  Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue
  err @"
Download failed ($($_.Exception.Message))
Possible causes:
  - Network connectivity issue
  - GitHub Release not found (version=$Version)
  - This version was not built for $arch
  Visit https://github.com/$Repo/releases to confirm release status
"@
}
ok "Download complete ($([math]::Round((Get-Item $dlPath).Length / 1MB, 1)) MB)"

info "Downloading checksum ..."
Write-Host "  URL: $ChecksumUrl"
$csPath = Join-Path $TempDir "$Asset.sha256"
try {
  Invoke-WebRequest -Uri $ChecksumUrl -OutFile $csPath -UseBasicParsing
} catch {
  warn "Could not download checksum ($($_.Exception.Message)), skipping verification"
  $csPath = $null
}

# ── Verify checksum ────────────────────────────────────────────────────────
if ($csPath -and (Test-Path $csPath)) {
  info "Verifying SHA256 ..."
  $expected = (Get-Content $csPath -Raw).Trim() -split '\s+' | Select-Object -First 1
  $actual = (Get-FileHash -Algorithm SHA256 $dlPath).Hash
  if ($expected -eq $actual) {
    ok "Checksum verified"
  } else {
    err "SHA256 checksum mismatch, file may be corrupted"
  }
}

# ── Install (atomic) ───────────────────────────────────────────────────────
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null

# Write to temp file on same filesystem, then Move-Item for atomic replacement
[string]$targetBin = Join-Path $InstallDir "crun.exe"
[string]$tempBin  = Join-Path $InstallDir ".crun.new.$pid"
Copy-Item $dlPath $tempBin -Force
Move-Item $tempBin $targetBin -Force
ok "Installed to $targetBin"

# ── Post-install verification ──────────────────────────────────────────────
try {
  $installedVersion = (& $targetBin --version 2>$null) -join ''
} catch {
  err "Install verification failed: $targetBin --version produced no output"
}

if (-not $installedVersion) {
  err "Install verification failed: binary is not executable"
}

if ($isUpgrade) {
  Write-Host ""
  if ($installedVersion -eq $existingVersion) {
    info "Version unchanged: $installedVersion"
  } else {
    ok "Upgrade complete: $existingVersion -> $installedVersion"
  }
} else {
  Write-Host ""
  & $targetBin --version 2>$null
}

# ── Post-install ───────────────────────────────────────────────────────────
Write-Host ""

# Config preservation notice
$configDir = Join-Path $env:LOCALAPPDATA "crun"
if ($isUpgrade) {
  if (Test-Path $configDir) {
    ok "User config preserved: $configDir"
    Write-Host "  (preferences, history, presets remain unchanged)"
  }
}

# Check claude command
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  warn "'claude' command not found in PATH. Please install Claude Code CLI first"
  Write-Host "  https://docs.anthropic.com/en/docs/claude-code/overview"
  Write-Host ""
}

# Check PATH
if ($env:Path -like "*$InstallDir*") {
  ok "crun is ready, type 'crun' to start"
  Write-Host ""
  return
}

warn "$InstallDir is not in PATH"

# Interactive confirm (only if tty available)
function Confirm-User($prompt) {
  try {
    $choice = Read-Host "$prompt [Y/n]"
    return ($choice -ne 'n' -and $choice -ne 'no')
  } catch {
    Write-Host "  (non-interactive, skipping)"
    return $false
  }
}

if (Confirm-User "Add $InstallDir to user PATH?") {
  Write-Host ""
  $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
  if ($userPath -like "*$InstallDir*") {
    ok "PATH already contains $InstallDir, skipping"
  } else {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$InstallDir", "User")
    ok "Added $InstallDir to user PATH"
  }
  $env:Path += ";$InstallDir"
  ok "Effective in current session"
  Write-Host ""
  Write-Host "  Type 'crun' to start."
} else {
  Write-Host ""
  Write-Host "  To add later, run the following in PowerShell:"
  Write-Host "    [Environment]::SetEnvironmentVariable('Path', `$env:Path + ';$InstallDir', 'User')"
  Write-Host ""
}

Write-Host ""

} finally {
  # Cleanup — guaranteed to run on any exit path (success, error, Ctrl+C)
  Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue
}
}
Main
