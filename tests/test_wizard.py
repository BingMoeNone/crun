"""Tests for wizard.py — first-run flow."""
from unittest import mock
from claude_run.config import Preferences, ConfigError
from claude_run.wizard import run_wizard


def _mock_select(return_value):
    """Create a mock questionary.select that returns a mock with .ask() → return_value."""
    m = mock.MagicMock()
    m.ask.return_value = return_value
    return m


class TestRunWizard:
    def test_selects_both_options(self, monkeypatch):
        """When user selects both search mode and language, preferences are updated."""
        responses = iter(["B", "en"])

        def mock_select(*args, **kwargs):
            return _mock_select(next(responses))

        monkeypatch.setattr("claude_run.wizard.questionary.select", mock_select)
        monkeypatch.setattr("claude_run.wizard.save_preferences", lambda p: None)
        monkeypatch.setattr("claude_run.wizard.CONFIG_DIR", mock.MagicMock())

        prefs = Preferences()
        result = run_wizard(prefs)

        assert result.search_mode == "B"
        assert result.language == "en"
        assert result.first_run is False

    def test_cancel_on_search_mode_returns_unchanged(self, monkeypatch):
        """When user cancels at search mode, preferences are unchanged."""
        monkeypatch.setattr(
            "claude_run.wizard.questionary.select",
            lambda *args, **kwargs: _mock_select(None),
        )
        monkeypatch.setattr("claude_run.wizard.CONFIG_DIR", mock.MagicMock())

        prefs = Preferences(language="en")
        result = run_wizard(prefs)

        assert result.search_mode == "A"  # default
        assert result.language == "en"  # original
        assert result.first_run is True

    def test_cancel_on_language_returns_unchanged(self, monkeypatch):
        """When user cancels at language, prefs are returned unmodified."""
        responses = iter(["B", None])

        def mock_select(*args, **kwargs):
            return _mock_select(next(responses))

        monkeypatch.setattr("claude_run.wizard.questionary.select", mock_select)
        monkeypatch.setattr("claude_run.wizard.CONFIG_DIR", mock.MagicMock())

        prefs = Preferences()
        result = run_wizard(prefs)

        # search_mode & language are only written to prefs after both prompts succeed
        assert result.search_mode == "A"
        assert result.language == "zh"
        assert result.first_run is True

    def test_saves_preferences_on_success(self, monkeypatch):
        """Preferences are saved when wizard completes."""
        responses = iter(["A", "zh"])

        def mock_select(*args, **kwargs):
            return _mock_select(next(responses))

        monkeypatch.setattr("claude_run.wizard.questionary.select", mock_select)
        monkeypatch.setattr("claude_run.wizard.CONFIG_DIR", mock.MagicMock())

        saved = []
        monkeypatch.setattr("claude_run.wizard.save_preferences", lambda p: saved.append(p))

        prefs = Preferences()
        result = run_wizard(prefs)

        assert len(saved) == 1
        assert saved[0].search_mode == "A"
        assert saved[0].language == "zh"
        assert result.first_run is False

    def test_handles_save_failure_gracefully(self, monkeypatch):
        """When save fails, updated preferences are still returned."""
        responses = iter(["A", "zh"])

        def mock_select(*args, **kwargs):
            return _mock_select(next(responses))

        monkeypatch.setattr("claude_run.wizard.questionary.select", mock_select)
        monkeypatch.setattr("claude_run.wizard.CONFIG_DIR", mock.MagicMock())
        monkeypatch.setattr(
            "claude_run.wizard.save_preferences",
            lambda p: (_ for _ in ()).throw(ConfigError("disk full")),
        )

        prefs = Preferences()
        result = run_wizard(prefs)

        assert result.search_mode == "A"
        assert result.language == "zh"
        assert result.first_run is False
