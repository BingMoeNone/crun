"""首次运行引导：选择搜索模式 + 语言。"""
import questionary

from claude_run.config import Preferences, save_preferences, CONFIG_DIR, ConfigError


def run_wizard(prefs: Preferences) -> Preferences:
    print("欢迎使用 crun — 一个帮你选择 Claude CLI 启动参数的工具。\n")

    search_mode = questionary.select(
        "搜索模式：",
        choices=[
            questionary.Choice("A · 模糊搜索（输入关键字过滤）", value="A"),
            questionary.Choice("B · 按分组浏览", value="B"),
        ],
        default=questionary.Choice("A · 模糊搜索（输入关键字过滤）", value="A"),
    ).ask()

    if search_mode is None:
        return prefs

    lang = questionary.select(
        "界面语言：",
        choices=[
            questionary.Choice("中文", value="zh"),
            questionary.Choice("English", value="en"),
        ],
        default=questionary.Choice("中文", value="zh"),
    ).ask()

    if lang is None:
        return prefs

    prefs.search_mode = search_mode
    prefs.language = lang
    prefs.first_run = False

    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_preferences(prefs)
        print("✓ 配置已保存。\n")
    except ConfigError as e:
        print(f"⚠ 保存配置失败: {e}，本次使用默认设置。\n")

    return prefs
