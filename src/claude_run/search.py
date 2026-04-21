# src/claude_run/search.py
from typing import Sequence

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
    Search flags by flag name, zh/en description, and choice labels/values.
    Returns sorted list of flags by match score (highest first).
    """
    if not query.strip():
        return list(flags)

    alt_lang = "en" if lang == "zh" else "zh"
    results = []
    for flag in flags:
        choice_score = 0
        if flag.choices:
            for c in flag.choices:
                choice_score = max(
                    choice_score,
                    fuzzy_match(query, c.value),
                    fuzzy_match(query, c.label_str(lang)),
                    fuzzy_match(query, c.label_str(alt_lang)),
                )
        score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label(alt_lang)),
            choice_score,
        )
        if score > 0:
            results.append((score, flag))

    results.sort(key=lambda x: -x[0])
    return [f for _, f in results]