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
                assert "placeholder" in arg
                assert "zh" in arg["placeholder"]
                assert "en" in arg["placeholder"]
