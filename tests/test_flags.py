# tests/test_flags.py
import json
import os

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

from claude_run.flags import Flag, FlagGroup, load_flags

def test_load_flags_default():
    flags = load_flags()
    group_map = {f.group for f in flags}
    assert "model" in group_map
    assert "permission" in group_map
    assert "session" in group_map
    assert "output" in group_map
    assert "tools" in group_map
    assert "dev" in group_map
    assert "debug" in group_map
    assert "mcp" in group_map

def test_flag_has_label():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    assert model_flag.label("zh") == "当前会话使用的模型"
    assert model_flag.label("en") == "Model for the current session"

def test_flag_get_display_choices():
    flags = load_flags()
    model_flag = next(f for f in flags if f.flag == "--model")
    choices = model_flag.get_choices("zh")
    assert len(choices) == 3
    assert choices[0]["value"] == "opus"

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
