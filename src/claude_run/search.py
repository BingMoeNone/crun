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


def fuzzy_match(query: str, target: str) -> int:
    """
    Simple fuzzy matching returning a score > 0 if query matches target.
    Higher score = better match. 0 = no match.
    """
    query = query.lower()
    target = target.lower()

    if query == target:
        return 100
    if target.startswith(query):
        return 80
    if query in target:
        return 60

    # Subsequence match
    qi = 0
    score = 0
    consecutive = 0
    for ch in target:
        if qi < len(query) and ch == query[qi]:
            qi += 1
            consecutive += 1
            score += consecutive * 5
    if qi == len(query):
        return score + 20

    return 0

def search_flags(flags: Sequence, query: str, lang: str = "zh") -> list:
    """
    Search flags by flag name, zh/en description, choice labels/values, and pinyin.
    Returns sorted list of flags by match score (highest first).
    """
    if not query.strip():
        return list(flags)

    alt_lang = "en" if lang == "zh" else "zh"
    results = []
    for flag in flags:
        # 拼音维度
        pinyin_score = 0
        if lang == "zh":
            pinyin_desc = _get_pinyin(flag.label("zh"))
            pinyin_score = fuzzy_match(query.lower(), pinyin_desc)

        choice_score = 0
        if flag.choices:
            for c in flag.choices:
                choice_score = max(
                    choice_score,
                    fuzzy_match(query, c.value),
                    fuzzy_match(query, c.label_str(lang)),
                    fuzzy_match(query, c.label_str(alt_lang)),
                )
                # 拼音匹配 choice label
                if lang == "zh":
                    choice_score = max(
                        choice_score,
                        fuzzy_match(query.lower(), _get_pinyin(c.label_str("zh"))),
                    )

        score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label(alt_lang)),
            choice_score,
            pinyin_score,
        )
        if score > 0:
            results.append((score, flag))

    results.sort(key=lambda x: -x[0])
    return [f for _, f in results]