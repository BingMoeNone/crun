# crun Windows Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adapt crun Python codebase for seamless Windows experience — platform-aware config paths, terminal detection, PowerShell installer, and CI build pipeline.

**Architecture:** Minimal code changes — only the path layer (config.py) and startup (__main__.py) touch Python code. New PowerShell installer (install.ps1) mirrors install.sh experience. New CI workflow builds Windows .exe via PyInstaller. TUI engine (app.py), search, presets, history remain untouched.

**Tech Stack:** Python 3.12, PowerShell 5.1+, PyInstaller, GitHub Actions (windows-latest runner)

---

### Task 1: Platform-aware config directory (`config.py`)

**Files:**
- Modify: `src/claude_run/config.py:1-17`
- Modify: `tests/test_config.py`

- [ ] **Step 1: Write failing tests for _default_config_dir**

```python
def test_platform_config_dir_linux(monkeypatch):
    import platform
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    from claude_run.config import _default_config_dir
    p = _default_config_dir()
    assert p == Path.home() / ".config" / "crun"


def test_platform_config_dir_windows_with_localappdata(monkeypatch):
    import platform, os
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("LOCALAPPDATA", "C:\\Users\\test\\AppData\\Local")
    from claude_run.config import _default_config_dir
    p = _default_config_dir()
    assert p == Path("C:\\Users\\test\\AppData\\Local\\crun")


def test_platform_config_dir_windows_no_localappdata(monkeypatch):
    import platform, os
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    monkeypatch.setattr(Path, "home", lambda: Path("C:\\Users\\test"))
    from claude_run.config import _default_config_dir
    p = _default_config_dir()
    assert p == Path("C:\\Users\\test\\AppData\\Local\\crun")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_config.py::test_platform_config_dir_linux tests/test_config.py::test_platform_config_dir_windows_with_localappdata tests/test_config.py::test_platform_config_dir_windows_no_localappdata -v`
Expected: FAIL with ImportError (function not defined)

- [ ] **Step 3: Implement _default_config_dir and update CONFIG_DIR**

```python
# config.py — replace lines 1-11

"""配置管理：用户偏好读写，带回退默认值。"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import logging
import os
import platform

log = logging.getLogger(__name__)


def _default_config_dir() -> Path:
    """Return the platform-appropriate config directory."""
    if platform.system() == "Windows":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            return Path(localappdata) / "crun"
        return Path.home() / "AppData" / "Local" / "crun"
    return Path.home() / ".config" / "crun"


CONFIG_DIR = _default_config_dir()
OLD_CONFIG_DIR = Path.home() / ".config" / "claude-run"
PREFERENCES_PATH = CONFIG_DIR / "preferences.json"
LAST_CONFIG_PATH = CONFIG_DIR / "last_config.json"
HISTORY_PATH = CONFIG_DIR / "history.json"
HISTORY_MAX = 9
CONFIG_VERSION = 1  # current schema version for all config files
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_config.py::test_platform_config_dir_linux tests/test_config.py::test_platform_config_dir_windows_with_localappdata tests/test_config.py::test_platform_config_dir_windows_no_localappdata -v`
Expected: 3 PASS

- [ ] **Step 5: Run full test suite to check no regressions**

Run: `uv run pytest tests/ -v -m "not integration"`
Expected: 85 passed

- [ ] **Step 6: Commit**

```bash
git add src/claude_run/config.py tests/test_config.py
git commit -m "feat: add _default_config_dir for platform-aware config path (Windows support)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 2: Windows Terminal detection (`__main__.py`)

**Files:**
- Modify: `src/claude_run/__main__.py:60-65`
- Test: `tests/test_app_history.py` (add at bottom)

- [ ] **Step 1: Write failing test for _check_windows_terminal**

```python
def test_check_windows_terminal_not_windows(monkeypatch, capsys):
    """No output on non-Windows platforms."""
    import platform
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    from claude_run.__main__ import _check_windows_terminal
    _check_windows_terminal()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_check_windows_terminal_in_wt(monkeypatch, capsys):
    """No output when running inside Windows Terminal."""
    import platform, os
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("WT_SESSION", "abc123")
    from claude_run.__main__ import _check_windows_terminal
    _check_windows_terminal()
    captured = capsys.readouterr()
    assert captured.out == ""


def test_check_windows_terminal_in_conhost(monkeypatch, capsys):
    """Prints notice when not in Windows Terminal."""
    import platform, os
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.delenv("WT_SESSION", raising=False)
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    from claude_run.__main__ import _check_windows_terminal
    _check_windows_terminal()
    captured = capsys.readouterr()
    assert "Windows Terminal" in captured.out
    assert "aka.ms/terminal" in captured.out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_app_history.py::test_check_windows_terminal_not_windows tests/test_app_history.py::test_check_windows_terminal_in_wt tests/test_app_history.py::test_check_windows_terminal_in_conhost -v`
Expected: FAIL with ImportError

- [ ] **Step 3: Add _check_windows_terminal to __main__.py and call it**

Add after `print_logo()` function definition (after line 64), before `main()`:

```python
def _check_windows_terminal() -> None:
    """On Windows, detect conhost and guide user to Windows Terminal."""
    if platform.system() != "Windows":
        return
    if os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM"):
        return
    print("=" * 60)
    print("  NOTICE: Better experience with Windows Terminal")
    print()
    print("  This tool uses Unicode symbols and color styles that")
    print("  may not display correctly in the classic console host.")
    print()
    print("  Recommended: Install Windows Terminal from Microsoft Store")
    print("  https://aka.ms/terminal")
    print()
    print("  Then run: wt crun")
    print("=" * 60)
    print()
```

Add `import platform` to the imports at the top of `__main__.py` (line 2, after `import os`).

Add call: In `main()`, insert `_check_windows_terminal()` right after `print_logo()` (before the `_validate_upgrade_configs()` call).

- [ ] **Step 4: Run tests to verify they pass**

Run: `uv run pytest tests/test_app_history.py::test_check_windows_terminal_not_windows tests/test_app_history.py::test_check_windows_terminal_in_wt tests/test_app_history.py::test_check_windows_terminal_in_conhost -v`
Expected: 3 PASS

- [ ] **Step 5: Run full test suite**

Run: `uv run pytest tests/ -v -m "not integration"`
Expected: 88 passed

- [ ] **Step 6: Commit**

```bash
git add src/claude_run/__main__.py tests/test_app_history.py
git commit -m "feat: add Windows Terminal detection and conhost guidance

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: PowerShell install script (`install.ps1`)

**Files:**
- Create: `scripts/install.ps1`

This is a single-file creation task. No TDD for shell scripts — manual verification checklist instead.

- [ ] **Step 1: Write scripts/install.ps1**

```powershell
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
function err($msg)   { Write-Host "  ERROR: $msg" -ForegroundColor Red; exit 1 }
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
$existingPath = (Get-Command crun.exe -ErrorAction SilentlyContinue).Source
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
  exit 0
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
  Write-Host "  To add later, run the following in an admin PowerShell:"
  Write-Host "    [Environment]::SetEnvironmentVariable('Path', `$env:Path + ';$InstallDir', 'User')"
  Write-Host ""
}

Write-Host ""

# Cleanup
Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue
```

- [ ] **Step 2: Manual verification checklist**

On a Windows machine (or VM) with PowerShell 5.1+, verify:

1. **Help flag:** `.\install.ps1 -h` — prints usage and exits 0
2. **Fresh install:** Run install.ps1 → downloads .exe, installs to `%LOCALAPPDATA%\Programs\crun\`, configures PATH, prints "crun is ready"
3. **Upgrade (same version):** Run again with `$env:CRUN_VERSION='v0.5.0'` → detects existing version, shows "Version unchanged"
4. **Upgrade (new version):** Change env to newer version → shows "old -> new" upgrade message
5. **Config preservation:** Check `%LOCALAPPDATA%\crun\` still has all files after upgrade
6. **PATH idempotency:** Run install twice → doesn't duplicate PATH entry
7. **Checksum verification:** Corrupt the .exe.sha256 file → install fails with clear error

- [ ] **Step 3: Commit**

```bash
git add scripts/install.ps1
git commit -m "feat: add PowerShell install script (install.ps1) for Windows

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 4: Windows CI build workflow (`release-windows.yml`)

**Files:**
- Create: `.github/workflows/release-windows.yml`

- [ ] **Step 1: Write release-windows.yml**

```yaml
name: release-windows

on:
  push:
    tags:
      - "v*"
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    permissions:
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v4

      - name: Install Python via uv
        run: uv python install 3.12

      - name: Sync dependencies
        run: uv sync --all-groups

      - name: Build binary
        run: |
          uv run pyinstaller --onefile `
            --name crun `
            --paths src `
            --add-data "data/flags_default.json;data" `
            --console `
            src/claude_run/__main__.py

      - name: Rename and checksum
        run: |
          $asset = "crun-windows-amd64.exe"
          Copy-Item dist/crun.exe dist/$asset
          $hash = (Get-FileHash -Algorithm SHA256 dist/$asset).Hash
          "$hash  $asset" | Out-File -Encoding ASCII "dist/$asset.sha256"

      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: crun-windows-amd64
          path: |
            dist/crun-windows-amd64.exe
            dist/crun-windows-amd64.exe.sha256

  release:
    needs: build
    runs-on: ubuntu-24.04
    permissions:
      contents: write
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: dist
          merge-multiple: true

      - name: Publish release assets
        uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/crun-windows-amd64.exe
            dist/crun-windows-amd64.exe.sha256
          generate_release_notes: true
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/release-windows.yml
git commit -m "ci: add Windows release workflow (PyInstaller .exe + SHA256)

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 5: Documentation update (README.md + CLAUDE.md)

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update CLAUDE.md — add Windows dev/bundle commands**

Insert after the existing pack command section in CLAUDE.md:

```markdown
## Windows 开发 / Windows Development

```bash
# Windows 上直接运行 (需 Python 3.12+)
uv pip install -e .
uv run crun

# 运行测试 (Windows runner)
uv run pytest tests/ -v -m "not integration"

# Windows 本地打包
uv sync --all-groups
uv run pyinstaller --onefile --name crun --paths src --add-data "data/flags_default.json;data" --console src/claude_run/__main__.py
# 输出: dist/crun.exe
```

> 注意：Windows 打包时 `--add-data` 分隔符为 `;`（Linux 为 `:`）。
```

- [ ] **Step 2: Update README.md — add Windows install section**

Insert after the Quick Install (binary) section for Linux, before "指定版本安装":

```markdown
### Windows 安装

支持 Windows 10+ `amd64`。推荐使用 Windows Terminal。

```powershell
# 一键安装
irm https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.ps1 | iex
```

指定版本安装：

```powershell
$env:CRUN_VERSION="v0.5.0"
irm https://raw.githubusercontent.com/BingMoeNone/claude-run/main/scripts/install.ps1 | iex
```

可选环境变量：

- `CRUN_REPO`：默认 `BingMoeNone/claude-run`
- `CRUN_VERSION`：默认 `latest`
- `CRUN_INSTALL_DIR`：安装目录（默认 `%LOCALAPPDATA%\Programs\crun`）
- `$env:DEBUG=$true`：启用调试输出

> 注意：`crun` 会调用系统中的 `claude` 命令，请先安装 Claude Code CLI 并确保在 PATH 中。首次运行可能需执行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 允许 PowerShell 脚本。
```

- [ ] **Step 3: Update README.md — add Windows to platform badge and config paths**

In the platform badge section, add Windows:
```markdown
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-blue?style=flat-square&logo=linux&logoColor=white)](https://github.com/BingMoeNone/claude-run)
```

In the config directory section, add Windows path note:
```markdown
> Windows 配置目录：`%LOCALAPPDATA%\crun\`（通常为 `C:\Users\<用户名>\AppData\Local\crun\`）
```

- [ ] **Step 4: Update README.md — add Windows keybinding note**

In the keybinding table section, add after the table:
```markdown
> Windows Terminal 上所有键位正常工作。传统命令提示符 (conhost) 不推荐使用。
```

- [ ] **Step 5: Commit**

```bash
git add README.md CLAUDE.md
git commit -m "docs: add Windows install and dev documentation

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 6: Final integration test pass

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

```bash
uv run pytest tests/ -v -m "not integration" --cov=src/claude_run --cov-report=term-missing
```
Expected: All tests pass, coverage similar or better than baseline (82+ tests).

- [ ] **Step 2: Verify import in simulated Windows environment**

```bash
# Verify platform-agnostic imports work
uv run python -c "import platform; print(platform.system())"
uv run python -c "from claude_run.config import CONFIG_DIR; print(CONFIG_DIR)"
```
Expected: Prints Linux config path (since running on Linux).

- [ ] **Step 3: Run with DEBUG to check no startup errors**

```bash
DEBUG=1 uv run crun --help
DEBUG=1 uv run crun --version
```
Expected: Both exit 0, no tracebacks.

- [ ] **Step 4: Commit (if any fixes needed)**

Only if fixes were applied during integration testing.

---

## Test matrix after all tasks

| Test file | Tests | Focus |
|-----------|-------|-------|
| `test_config.py` | 36 | +3 platform path tests |
| `test_flags.py` | 15 | unchanged |
| `test_search.py` | 15 | unchanged |
| `test_runner.py` | 7 | unchanged |
| `test_app_conflicts.py` | 5 | unchanged |
| `test_app_history.py` | 5 | +3 terminal detection tests |
| `test_integration.py` | 4 | skipped (integration marker) |

**Total: 87 tests (+6 new)**
