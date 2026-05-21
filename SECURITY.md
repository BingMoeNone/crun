# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in crun, please report it via:

1. **GitHub Security Advisory**: Go to [Security → Advisories](https://github.com/BingMoeNone/crun/security/advisories/new) and create a private advisory.
2. **Email**: Send details to the maintainer (see GitHub profile for contact).

Please do NOT open a public issue for security vulnerabilities.

## Scope

- The install scripts (`install.sh`, `install.ps1`) — issues like command injection, insecure downloads
- The crun binary itself — issues like arbitrary code execution through config files
- The TUI — issues like terminal escape injection

## Out of Scope

- The `claude` CLI binary that crun wraps (report those to Anthropic)
- Issues requiring local user access (if you can write to the config dir, you already have user-level access)
