# Contributing

Thank you for considering a contribution.

## Development setup

```powershell
git clone https://github.com/Merd0/ai-shift-analysis-assistant.git
cd ai-shift-analysis-assistant
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the desktop application with:

```powershell
$env:PYTHONUTF8 = "1"
python vardiya_gui.py
```

## Before opening a pull request

1. Keep each change focused and describe its user-visible effect.
2. Do not commit API keys, logs, production workbooks, exports, or personal data.
3. Use synthetic or fully anonymized data in tests and screenshots.
4. Compile the project to catch syntax errors:

   ```powershell
   python -m compileall -q .
   ```

5. Verify that the GUI starts and that the changed workflow behaves as expected.
6. Update `README.md` or `CHANGELOG.md` when behavior, setup, or limitations change.

## Bug reports

Include the application version, Windows version, Python version, reproduction steps, and sanitized error output. Security issues and sensitive data must be handled according to [SECURITY.md](SECURITY.md).
