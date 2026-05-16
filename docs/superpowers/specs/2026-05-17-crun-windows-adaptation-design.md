# crun Windows 适配设计文档

> 目标：不改语言栈（Python），最小化代码改动，让 crun 在 Windows 上达到与 Linux 版对齐的体验。

## 决策汇总

| 维度 | 决定 |
|------|------|
| 技术路线 | Python 代码直接适配，不改语言栈 |
| 适配深度 | B — 体验对齐 Linux 版（二进制发布、安装脚本、PATH 配置） |
| 安装方式 | `irm \| iex` 为主，手动下载 `.ps1` 为辅 |
| 配置目录 | `$env:LOCALAPPDATA\crun\`（`C:\Users\<用户名>\AppData\Local\crun\`） |
| 终端支持 | 仅保证 Windows Terminal 体验，conhost 检测到后给出引导提示 |
| 权限策略 | 固定用户级安装（`$env:LOCALAPPDATA\Programs\crun\`），无需管理员 |

---

## 一、架构概览

核心原则：**不改 TUI 引擎，只改路径层、安装层、CI 层。**

```
改造范围：

  scripts/install.ps1                           ← 新建（~150 行，对标 install.sh）
  src/claude_run/config.py                      ← 小改（~10 行，平台路径判断）
  src/claude_run/__main__.py                    ← 小改（~25 行，终端检测 + 引导）
  .github/workflows/release-windows.yml         ← 新建（~60 行，Windows CI 构建）
  README.md / CLAUDE.md                         ← 修改（Windows 安装说明）

不改：
  app.py / flags.py / search.py / runner.py / wizard.py
```

### 平台路径抽象

所有平台差异封装在 `config.py` 的路径常量中，运行时判断一次，其余模块通过 import 使用这些常量，无感知：

```
Linux:   ~/.config/crun/
Windows: %LOCALAPPDATA%\crun\
```

子文件结构完全一致：
```
preferences.json / history.json / presets.json / flags_custom.json
```

### 终端适配

prompt_toolkit 在 Windows Terminal 上原生支持 Unicode、颜色、键盘输入。启动时检测终端类型，若在 conhost（传统命令提示符）中运行则打印引导信息，提示用户安装 Windows Terminal，但不阻断执行。

---

## 二、模块详细设计

### 2.1 config.py — 配置路径平台适配

修改 `CONFIG_DIR` 为工厂函数，根据 `platform.system()` 动态选择：

```python
import os
import platform

def _default_config_dir() -> Path:
    if platform.system() == "Windows":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            return Path(localappdata) / "crun"
        return Path.home() / "AppData" / "Local" / "crun"
    return Path.home() / ".config" / "crun"

CONFIG_DIR = _default_config_dir()
```

`OLD_CONFIG_DIR` 常量删除（Windows 上无历史迁移需求，Linux 的 `claude-run` → `crun` 迁移已在上一版本完成）。保留 `_migrate_old_config()` 函数定义但不新增迁移逻辑。

`ensure_config_dir()` 不变，`pathlib.Path.mkdir(parents=True, exist_ok=True)` 在 Windows 上正常工作。

`LOCALAPPDATA` 路径含空格（`C:\Users\<用户名>\AppData\Local`），Python `pathlib` 和 `json` 均正确处理含空格路径。`os.execvp()` 传参为 `list[str]` 不涉及 shell 转义，安全。

### 2.2 __main__.py — 终端检测与引导

在 `print_logo()` 之后插入 `_check_windows_terminal()`：

```python
def _check_windows_terminal() -> None:
    if platform.system() != "Windows":
        return
    if os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM"):
        return  # Windows Terminal
    print("=" * 60)
    print("  NOTICE: Better experience with Windows Terminal")
    print("  This tool may not display correctly in classic console host.")
    print("  Install Windows Terminal: https://aka.ms/terminal")
    print("  Then run: wt crun")
    print("=" * 60)
    print()
```

- `WT_SESSION` — Windows Terminal 独有环境变量，最可靠
- `TERM_PROGRAM` — 现代终端通常设置，WT 设为 `"Windows Terminal"`
- 不阻断，用户自行决定

### 2.3 install.ps1 — 安装脚本（新建）

对标 Linux `install.sh` 的完整体验：

**流程：**
```
irm | iex → 平台检测 → 依赖检查 → 检查已有安装 → 下载 .exe
→ SHA256 校验 → 原子安装 → 安装后验证 → PATH 配置 → 完成
```

**平台检测：**
```powershell
if ($env:OS -ne "Windows_NT") {
    Write-Error "crun installer: Windows only"
    exit 1
}
```

**安装目录：**
- 默认：`$env:LOCALAPPDATA\Programs\crun\`
- 可被 `$env:CRUN_INSTALL_DIR` 覆盖
- 无需管理员权限（用户目录内）

**原子安装：**
```powershell
$tempBin = Join-Path $InstallDir ".crun.new.$pid"
Copy-Item $dlPath $tempBin -Force
Move-Item $tempBin (Join-Path $InstallDir "crun.exe") -Force
```

**PATH 持久化：**
```powershell
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$InstallDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$InstallDir", "User")
}
$env:Path += ";$InstallDir"  # 当前进程
```

**已有安装检测：**
```powershell
$existing = Get-Command crun.exe -ErrorAction SilentlyContinue
```

**SHA256 校验：** `Get-FileHash` (PowerShell 4.0+)

**下载：** `Invoke-WebRequest` / `Invoke-RestMethod`

**二进制资产名：** `crun-windows-amd64.exe`

### 2.4 CI/CD — release-windows.yml（新建）

```yaml
name: Release Windows
on:
  push:
    tags: ["v*"]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - run: uv sync --all-groups
      - run: uv run pyinstaller --onefile --name crun
              --paths src
              --add-data "data/flags_default.json;data"
              --console
              src/claude_run/__main__.py
      - run: Get-FileHash -Algorithm SHA256 dist/crun.exe > dist/crun.exe.sha256
      - uses: softprops/action-gh-release@v2
        with:
          files: |
            dist/crun.exe
            dist/crun.exe.sha256
```

和 Linux CI 并列，同一 GitHub Release 包含两套架构资产：
- `crun-linux-amd64` / `crun-linux-arm64`
- `crun-windows-amd64.exe` / `crun-windows-amd64.exe.sha256`

### 2.5 测试策略

| 层级 | 做法 |
|------|------|
| 单元测试 | CI 矩阵加 `windows-latest` runner，同套 pytest（82 个），代码零改动 |
| 集成测试 | Windows 无 pexpect，暂不加。用 `test_crun_version` + 安装后手动冒烟 |
| install.ps1 测试 | 手动验证清单：首次安装 / 覆盖升级 / PATH 配置 / 配置保留 |

### 2.6 runner.py — os.execvp 行为差异

Linux 上 `os.execvp()` 替换当前进程。Windows 上没有真正的 `exec`，Python 退化为 `subprocess` 式 spawn（启动子进程后退出当前进程）。对用户无感知，但退出码传播可能不完全一致。标记为已知差异，不做特殊处理。

---

## 三、明确排除

| 项 | 原因 |
|----|------|
| `app.py` TUI 改动 | prompt_toolkit 跨平台，WT 下完美运行 |
| `flags.py` / `search.py` | 纯逻辑，无平台依赖 |
| `wizard.py` | questionary 支持 Windows |
| pypinyin 拼音数据 | pypinyin 纯 Python，无 C 扩展，Windows 正常 |
| winget 分发 | 本次不上，后续评估 |
| MSIX 打包 | 本次不上，PyInstaller 单 exe 足够 |

---

## 四、文件改动清单

| 文件 | 操作 | 改动量 |
|------|------|--------|
| `src/claude_run/config.py` | 修改 | `CONFIG_DIR` 工厂化，~10 行 |
| `src/claude_run/__main__.py` | 修改 | `_check_windows_terminal()`，~25 行 |
| `scripts/install.ps1` | 新建 | ~150 行 |
| `.github/workflows/release-windows.yml` | 新建 | ~60 行 |
| `README.md` | 修改 | Windows 安装/使用说明 |
| `CLAUDE.md` | 修改 | Windows 开发/打包命令 |

总计：新建 ~210 行，修改 ~50 行。
