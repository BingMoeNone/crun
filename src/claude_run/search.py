# src/claude_run/search.py
from typing import Sequence

# ── 拼音缓存 ────────────────────────────────
_pinyin_cache: dict[str, str] = {}


def _get_pinyin(text: str) -> str:
    """返回中文文本的拼音串，带缓存。"""
    if text in _pinyin_cache:
        return _pinyin_cache[text]
    try:
        from pypinyin import lazy_pinyin, Style

        segs = lazy_pinyin(text, style=Style.NORMAL)
        result = "".join(segs)
    except Exception:
        result = text
    _pinyin_cache[text] = result
    return result


def fuzzy_match(query: str, target: str) -> float:
    """
    Fuzzy matching returning a score > 0 if query matches target.
    Higher score = better match. 0 = no match.

    Score tiers (each with a tie-breaking fractional part):
    - 1000-1010: exact match
    - 900-910: prefix match (target starts with query)
    - 800-810: substring match (query in target)
    - 700-720: subsequence match (all query chars in order)
    """
    query = query.lower()
    target = target.lower()

    if query == target:
        # Exact match: shorter target = better
        return 1000.0 + (1.0 / max(len(target), 1)) * 10

    if target.startswith(query):
        # Prefix: higher match ratio = better
        return 900.0 + (len(query) / max(len(target), 1)) * 10

    if query in target:
        # Substring: higher density = query is a larger fraction of target
        density = len(query) / max(len(target), 1)
        return 800.0 + density * 10

    # Subsequence match
    qi = 0
    positions: list[int] = []
    for i, ch in enumerate(target):
        if qi < len(query) and ch == query[qi]:
            positions.append(i)
            qi += 1

    if qi == len(query):
        # Density: how much of target is matched chars
        density = len(query) / max(len(target), 1)
        # Tightness: how concentrated the matched chars are
        if len(positions) >= 2:
            spread = positions[-1] - positions[0] + 1
            tightness = len(query) / spread
        else:
            tightness = 1.0
        return 700.0 + density * 10 + tightness * 10

    return 0.0

def search_flags(flags: Sequence, query: str, lang: str = "zh") -> list:
    """
    Search flags by flag name, zh/en description, choice labels/values, and pinyin.
    Returns sorted list of flags by match score (highest first).

    Dimension weights ensure the priority: flag name > description > choice > pinyin.
    """
    if not query.strip():
        return list(flags)

    alt_lang = "en" if lang == "zh" else "zh"
    results: list[tuple[float, str, object]] = []
    for flag in flags:
        # Pinyin score (lowest priority)
        pinyin_score = 0.0
        if lang == "zh":
            pinyin_desc = _get_pinyin(flag.label("zh"))
            pinyin_score = fuzzy_match(query.lower(), pinyin_desc)

        choice_score = 0.0
        if flag.choices:
            for c in flag.choices:
                choice_score = max(
                    choice_score,
                    fuzzy_match(query, c.value),
                    fuzzy_match(query, c.label_str(lang)),
                    fuzzy_match(query, c.label_str(alt_lang)),
                )
                # Pinyin match for choice labels
                if lang == "zh":
                    choice_score = max(
                        choice_score,
                        fuzzy_match(query.lower(), _get_pinyin(c.label_str("zh"))),
                    )

        flag_name_score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.flag.lstrip('-')),
        )
        desc_primary_score = fuzzy_match(query, flag.label(lang))
        desc_alt_score = fuzzy_match(query, flag.label(alt_lang))

        # Weighted combination: flag name (×100) > description (×10) > choice (×5) > pinyin (×1)
        # The multiplier gap (~10x per tier) guarantees the dimension priority
        combined = (
            flag_name_score * 100.0 +
            max(desc_primary_score, desc_alt_score) * 10.0 +
            choice_score * 5.0 +
            pinyin_score * 1.0
        )
        if combined > 0:
            # Small bonus for shorter flag names (shorter = more focused / core flag)
            name_len = max(len(flag.flag.lstrip('-')), 1)
            combined += 20.0 / name_len
        if combined > 0:
            # secondary sort key: stable by flag name
            results.append((combined, flag.flag, flag))

    results.sort(key=lambda x: (-x[0], x[1]))
    return [f for _, _, f in results]


def highlight_line(
    line: str,
    query: str,
    base_style: str,
    match_style: str,
) -> list[tuple[str, str]]:
    """
    将 line 拆分为带样式的片段列表。
    在 line 中用子序列匹配方式标记 query 的每个字符。

    返回: [(style, text), ...]，相邻同 style 片段已合并
    只有当所有 query 字符都在 line 中找到时才返回高亮片段，否则返回原始样式。
    """
    if not query:
        return [(base_style, line)]

    q = query.lower()
    qi = 0

    # 标记每个字符是否匹配
    chars: list[tuple[str, bool]] = []
    for ch in line:
        matched = False
        if qi < len(q) and ch.lower() == q[qi]:
            matched = True
            qi += 1
        chars.append((ch, matched))

    # 如果没有匹配到所有 query 字符，不显示高亮（避免拼音匹配时的不完整高亮）
    if qi != len(q):
        return [(base_style, line)]

    # 合并相邻同 style 字符
    fragments: list[tuple[str, str]] = []
    for ch, matched in chars:
        style = match_style if matched else base_style
        if fragments and fragments[-1][0] == style:
            fragments[-1] = (style, fragments[-1][1] + ch)
        else:
            fragments.append((style, ch))

    return fragments