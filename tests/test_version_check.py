"""Tests for version_check.py pure functions."""
import pytest
from claude_run.version_check import _normalize, _parse_semver, _is_newer


class TestNormalize:
    def test_strips_v_prefix(self):
        assert _normalize("v0.6.1") == "0.6.1"

    def test_preserves_no_prefix(self):
        assert _normalize("0.6.1") == "0.6.1"

    def test_empty_string(self):
        assert _normalize("") == ""


class TestParseSemver:
    def test_standard(self):
        assert _parse_semver("0.6.1") == (0, 6, 1)

    def test_major_only(self):
        assert _parse_semver("1") == (1,)

    def test_two_component(self):
        assert _parse_semver("2.1") == (2, 1)

    def test_non_numeric_returns_empty(self):
        assert _parse_semver("dev") == ()

    def test_empty_returns_empty(self):
        assert _parse_semver("") == ()


class TestIsNewer:
    def test_remote_newer(self):
        assert _is_newer("0.6.1", "0.6.0")

    def test_same_version(self):
        assert not _is_newer("0.6.0", "0.6.0")

    def test_local_newer(self):
        assert not _is_newer("0.5.0", "0.6.0")

    def test_major_bump(self):
        assert _is_newer("1.0.0", "0.9.9")

    def test_minor_bump(self):
        assert _is_newer("0.7.0", "0.6.9")

    def test_patch_bump(self):
        assert _is_newer("0.6.2", "0.6.1")

    def test_unparseable_remote(self):
        assert _is_newer("dev", "0.6.0")

    def test_unparseable_local(self):
        assert _is_newer("0.6.0", "dev")

    def test_both_unparseable_different(self):
        assert _is_newer("abc", "xyz")

    def test_both_unparseable_same(self):
        assert not _is_newer("abc", "abc")
