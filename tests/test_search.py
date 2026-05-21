# tests/test_search.py
from claude_run.search import fuzzy_match, search_flags, highlight_line

# Mock flag for testing
class MockFlag:
    def __init__(self, flag, label_zh, label_en, choices=None):
        self.flag = flag
        self._label_zh = label_zh
        self._label_en = label_en
        self.description = {"zh": label_zh, "en": label_en}
        self.choices = choices or []

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
    assert results[0].flag == "--mcp-config", \
        f"flag name match should rank first, got {results[0].flag}"


def test_search_flags_ranking_flag_name_over_description():
    """Flag name match should outrank description-only match."""
    # A flag with "model" in description but not in flag name
    flags = [
        MockFlag("--other", "包含模型关键词", "Contains model keyword"),
        MockFlag("--model", "当前会话使用的模型", "Model for the current session"),
    ]
    results = search_flags(flags, "model", lang="en")
    assert results[0].flag == "--model", \
        f"--model should rank first (flag name match), got {results[0].flag}"


def test_search_flags_ranking_exact_over_contains():
    """Exact match should outrank contains match within same dimension."""
    results = search_flags(FLAGS, "debug", lang="en")
    # -d has "Enable debug mode", --debug-file has "Write debug logs..."
    # Both contain "debug" in description, -d's description starts with "Enable"
    # but --debug-file flag name contains "debug"
    debug_flags = [r.flag for r in results if "debug" in r.flag.lower()]
    assert len(debug_flags) > 0, f"Expected debug flags in results: {[r.flag for r in results]}"

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


def test_search_flags_by_pinyin():
    """输入拼音 'moxing' 应匹配中文描述中的 '模型'"""
    results = search_flags(FLAGS, "moxing", lang="zh")
    assert any(r.flag == "--model" for r in results), \
        "拼音 'moxing' 应匹配到 --model"


def test_search_flags_by_pinyin_debug():
    """输入拼音 'tiaoshi' 应匹配中文描述中的 '调试'"""
    results = search_flags(FLAGS, "tiaoshi", lang="zh")
    assert len(results) >= 2, f"拼音 'tiaoshi' 应匹配到至少 2 个结果，实际: {len(results)}"


def test_search_flags_by_pinyin_partial():
    """输入拼音 'mox' (部分拼音) 应匹配 '模型'"""
    results = search_flags(FLAGS, "mox", lang="zh")
    assert any(r.flag == "--model" for r in results), \
        "部分拼音 'mox' 应匹配到 --model"


def test_highlight_line_exact_match():
    fragments = highlight_line("--model", "model", "class:item", "class:match")
    # 应有至少 2 个片段: "--" 普通 + "model" 高亮
    assert len(fragments) >= 2
    assert fragments[-1][0] == "class:match"
    assert "model" in fragments[-1][1]


def test_highlight_line_no_match():
    fragments = highlight_line("hello", "xyz", "class:item", "class:match")
    assert fragments == [("class:item", "hello")]


def test_highlight_line_empty_query():
    fragments = highlight_line("hello", "", "class:item", "class:match")
    assert fragments == [("class:item", "hello")]


def test_highlight_line_chinese():
    fragments = highlight_line("当前会话使用的模型", "模型", "class:item", "class:match")
    assert len(fragments) >= 2
    # "模型" 两个字应该被高亮
    match_texts = [t for s, t in fragments if s == "class:match"]
    assert any("模" in t for t in match_texts)
    assert any("型" in t for t in match_texts)

def test_highlight_line_partial_no_highlight():
    """只有部分 query 匹配时不显示高亮（避免拼音匹配时的不完整高亮）"""
    fragments = highlight_line("--model", "mox", "class:item", "class:match")
    assert fragments == [("class:item", "--model")]