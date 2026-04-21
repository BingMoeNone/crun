# tests/test_search.py

def fuzzy_match(query: str, target: str) -> int:
    """Returns score > 0 if query matches target. Higher = better. 0 = no match."""
    query = query.lower()
    target = target.lower()

    if query == target:
        return 100
    if target.startswith(query):
        return 80
    if query in target:
        return 60

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

def search_flags(flags, query: str, lang: str = "zh") -> list:
    """Search flags by flag name, zh description, or en description."""
    if not query.strip():
        return list(flags)

    results = []
    for flag in flags:
        score = max(
            fuzzy_match(query, flag.flag),
            fuzzy_match(query, flag.label(lang)),
            fuzzy_match(query, flag.label("en" if lang == "zh" else "zh")),
        )
        if score > 0:
            results.append((score, flag))

    results.sort(key=lambda x: -x[0])
    return [f for _, f in results]

# Mock flag for testing
class MockFlag:
    def __init__(self, flag, label_zh, label_en):
        self.flag = flag
        self._label_zh = label_zh
        self._label_en = label_en
        self.description = {"zh": label_zh, "en": label_en}

    def label(self, lang):
        return self._label_zh if lang == "zh" else self._label_en

FLAGS = [
    MockFlag("--model", "当前会话使用的模型", "Model for the current session"),
    MockFlag("--mcp-config", "从 JSON 文件加载 MCP 服务器配置", "Load MCP servers from JSON files"),
    MockFlag("-d", "启用调试模式", "Enable debug mode"),
    MockFlag("--debug-file", "将调试日志写入指定文件", "Write debug logs to a specific file path"),
]

def test_fuzzy_match_exact():
    assert fuzzy_match("model", "model") > 0
    assert fuzzy_match("mcp", "mcp-config") > 0
    assert fuzzy_match("debug", "debug") > 0

def test_fuzzy_match_zh():
    assert fuzzy_match("调试", "调试模式") > 0
    assert fuzzy_match("模型", "当前会话使用的模型") > 0

def test_fuzzy_match_no_match():
    assert fuzzy_match("xyz", "model") == 0

def test_search_flags_by_flag_name():
    results = search_flags(FLAGS, "mcp", lang="en")
    assert len(results) > 0
    assert any(r.flag == "--mcp-config" for r in results)

def test_search_flags_by_zh_description():
    results = search_flags(FLAGS, "调试", lang="zh")
    assert len(results) >= 2  # -d and --debug-file

def test_search_flags_by_en_description():
    results = search_flags(FLAGS, "debug", lang="en")
    assert len(results) >= 2

def test_search_flags_case_insensitive():
    results = search_flags(FLAGS, "MODEL", lang="en")
    assert any(r.flag == "--model" for r in results)

def test_search_flags_empty_query_returns_all():
    results = search_flags(FLAGS, "", lang="zh")
    assert len(results) == len(FLAGS)

def test_search_flags_no_match():
    results = search_flags(FLAGS, "foobar", lang="zh")
    assert len(results) == 0