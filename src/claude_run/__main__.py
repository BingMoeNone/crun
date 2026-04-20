# src/claude_run/__main__.py
from claude_run.config import load_preferences, is_first_run, Preferences
from claude_run.wizard import run_wizard
from claude_run.app import MainApp

def main():
    if is_first_run():
        prefs = run_wizard(Preferences())
    else:
        prefs = load_preferences()

    app = MainApp(prefs)
    app.run()

if __name__ == "__main__":
    main()