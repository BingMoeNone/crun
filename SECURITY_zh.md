# 安全策略

[English](SECURITY.md)

## 支持的版本

| 版本   | 支持状态           |
| ------ | ------------------ |
| 0.6.x  | :white_check_mark: |
| 0.5.x  | :white_check_mark: |
| < 0.5  | :x:                |

## 报告漏洞

如果你在 crun 中发现了安全漏洞，请通过以下方式报告：

1. **GitHub Security Advisory**：前往 [Security → Advisories](https://github.com/BingMoeNone/crun/security/advisories/new) 创建私有 advisory。
2. **电子邮件**：发送详情至维护者（联系方式见 GitHub 个人资料）。

请**不要**为安全漏洞创建公开 issue。

## 范围

- 安装脚本（`install.sh`、`install.ps1`）— 如命令注入、不安全的下载
- crun 二进制文件本身 — 如通过配置文件执行任意代码
- TUI — 如终端转义注入

## 不在范围内

- crun 所包装的 `claude` CLI 二进制文件（请向 Anthropic 报告）
- 需要本地用户访问权限的问题（如果能够写入配置目录，即已具备用户级访问权限）
