# tests/test_flags.py
import json
import os
from pathlib import Path

from claude_run.flags import FlagGroup, load_flags, _default_flags_path


def get_flags_path():
    return os.path.join(os.path.dirname(__file__), "..", "data", "flags_default.json")


def test_flags_json_valid():
    path = get_flags_path()
    with open(path) as f:
        data = json.load(f)
    assert data["version"] == 1
    assert "flags" in data
    assert len(data["flags"]) > 0


def test_flag_structure():
    path = get_flags_path()
    with open(path) as f:
        data = json.load(f)
    for flag in data["flags"]:
        assert "flag" in flag
        assert "description" in flag
        assert "zh" in flag["description"]
        assert "en" in flag["description"]
        assert "type" in flag
        assert "group" in flag
        assert flag["type"] in ("single", "multi", "value")
        if flag["type"] == "single":
            assert "choices" in flag
            for choice in flag["choices"]:
                assert "value" in choice
                assert "label" in choice
                assert "zh" in choice["label"]
                assert "en" in choice["label"]
        if flag["type"] == "value":
            assert "required_args" in flag
            assert isinstance(flag["required_args"], list)
            for arg in flag["required_args"]:
                assert "name" in arg
                assert "label" in arg
                assert "zh" in arg["label"]
                assert "en" in arg["label"]
                if arg.get("placeholder"):
                    assert isinstance(arg["placeholder"], dict)


def test_load_flags_default():
    flags = load_flags()
    group_map = {f.group for f in flags}
    expected_groups = {"model", "permission", "session", "output", "tools",
                       "dev", "debug", "mcp", "system", "agent", "ide",
                       "remote", "hook", "limit", "config"}
    assert group_map == expected_groups


def test_flag_has_label():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    assert model_flag.label("zh") == "当前会话使用的模型，支持别名或完整模型名"
    assert model_flag.label("en") == "Model for the current session (alias or full name)"


def test_flag_get_display_choices():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    choices = model_flag.get_choices("zh")
    assert len(choices) == 7
    assert choices[0]["value"] == "sonnet"


def test_flag_requires_value():
    flags = load_flags()
    mcp_flag = next(f for f in flags if f.flag == "--mcp-config")
    assert mcp_flag.requires_value() == True
    assert mcp_flag.required_args[0].label_str("zh") == "配置文件路径"


def test_group_flags():
    flags = load_flags()
    groups = FlagGroup.group_by(flags)
    assert "model" in groups
    assert all(f.group == "model" for f in groups["model"])


def test_default_flags_path_source_mode(monkeypatch):
    monkeypatch.delattr("sys._MEIPASS", raising=False)
    p = _default_flags_path()
    assert p.name == "flags_default.json"
    assert p.exists()


def test_default_flags_path_pyinstaller_mode(monkeypatch, tmp_path):
    meipass = tmp_path / "bundle"
    data_dir = meipass / "data"
    data_dir.mkdir(parents=True)
    target = data_dir / "flags_default.json"
    target.write_text("{}", encoding="utf-8")
    monkeypatch.setattr("sys._MEIPASS", str(meipass), raising=False)
    assert _default_flags_path() == target


def test_flag_conflicts_with():
    """conflicts_with 引用的 flag 必须存在。"""
    flags = load_flags()
    all_names = {f.flag for f in flags}
    for f in flags:
        if f.conflicts_with:
            for target in f.conflicts_with:
                assert target in all_names, \
                    f"{f.flag}.conflicts_with 引用不存在的 {target}"


def test_flag_conflicts_symmetric():
    """互斥关系应双向声明。"""
    flags = load_flags()
    for f in flags:
        if f.conflicts_with:
            for target in f.conflicts_with:
                target_flag = next(fl for fl in flags if fl.flag == target)
                assert target_flag.conflicts_with is not None, \
                    f"{f.flag} 声明与 {target} 互斥，但 {target} 未声明 conflicts_with"
                assert f.flag in target_flag.conflicts_with, \
                    f"{f.flag} 声明与 {target} 互斥，但 {target} 未反向声明"

