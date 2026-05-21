# crun Changelog

[中文文档](../README_zh.md) | [English README](../README.md)

## v0.6.0 (2026-05-21)

### 跨平台支持 / Cross-Platform

- **Windows 原生支持**：启用 ANSI/VT 处理与 UTF-8，自动检测 Windows Terminal
- **Windows 平台检测**：经典 conhost 拒绝运行并给出明确指引
- **PowerShell 安装脚本** (`install.ps1`)：与 Linux 脚本功能完全对等
- **Windows PyInstaller 打包**：`.exe` 二进制 + SHA256 校验
- **跨平台配置目录**：Linux `~/.config/crun/`，Windows `%LOCALAPPDATA%\crun\`
- **`.cmd`/`.bat` 包装器支持**：解决 Windows 下 npm 安装 Claude Code 的 execvp 问题

### 软件生命周期 / Software Lifecycle

- **安装脚本升级确认**：安装前检测已安装版本，对比 GitHub 最新 release，询问用户是否升级
- **`-y`/`--yes` 非交互模式**：安装和卸载脚本均支持跳过确认
- **原子化安装**：临时文件 + mv 确保中断不损坏现有二进制
- **卸载脚本** (`uninstall.sh` / `uninstall.ps1`)：
  - 软卸载：仅移除二进制，保留所有用户数据
  - 完全卸载：移除二进制 + 所有配置/历史/预设
- **用户数据保护**：安装/升级/卸载过程不触碰 `~/.config/crun/`（除非用户明确选择完全卸载）
- **配置版本迁移**：自动检测旧路径 `~/.config/claude-run/` 并迁移
- **启动配置校验**：自动检测并报告失效的历史记录和预设条目

### 版本管理系统 / Version Management

- **三级版本解析**：PyInstaller bundle pyproject.toml → importlib.metadata → 源码 pyproject.toml
- **GitHub 版本检查** (`version_check.py`)：启动时静默对比本地版本与 GitHub latest release
- **PyInstaller 版本固化**：`pyproject.toml` 打入 bundle，根除二进制版本号过时问题
- **`--version` 增强**：同时显示本地版本和 GitHub 最新版本

### TUI 增强 / TUI Enhancements

- **拼音模糊搜索**：通过 pypinyin 支持中文拼音搜索参数
- **搜索字符级高亮**：匹配字符逐字渲染 `search-match` 样式（黄色加粗）
- **参数提示行**：JSON `tip` 字段优先，回退到元数据自动生成
- **命令历史**：环形缓冲（9 条），A/B 自适应展示方案，数字快速选择
- **参数预设**：保存/加载/删除命名预设方案，加载时自动清洗失效参数
- **自定义快捷键**：用户可配置键位，启动时冲突检测并警告

### 安装脚本同步规则

- `install.sh` 与 `install.ps1` 核心功能完全对等，修改任一时必须同步

### 其他 / Misc

- 全新的 CRUN ASCII art 启动画幅
- 88 个单元测试 + 集成测试（pexpect）
- CI：Linux amd64/arm64 + Windows amd64 自动发布

---

## v0.4.0 (2026-05-16)

- 项目更名为 crun（原 claude-run）
- 配置目录迁移到 `~/.config/crun/`
- 71 个 Claude Code 启动参数（15 个分组）
- 参数互斥逻辑（`conflicts_with`），TUI 自动处理
- Linux curl 安装脚本 + 二进制发布流水线
- 启动画幅展示版本号

---

## v0.1.0 (2026-04-21)

- 初始版本
- TUI 交互式参数选择器（prompt_toolkit + questionary 双层架构）
- 模糊搜索、首次运行向导、偏好管理
- 退出码约定与错误处理体系
- 7 个 Python 源文件，核心功能完整
