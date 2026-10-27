**English | [Türkçe](README.tr.md)**

<div align="center">

# AI Shift Analysis Assistant

**A Python desktop application for preparing, filtering, and analyzing Excel-based production shift logs, with AI-assisted operational reporting.**

[![Version](https://img.shields.io/badge/version-1.5.2-0f766e.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab.svg?logo=python&logoColor=white)](requirements.txt)
[![Platform](https://img.shields.io/badge/platform-Windows-0078d4.svg?logo=windows)](#installation)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An **internship/portfolio prototype** designed to identify recurring issues, summarize periods, and help prepare action-oriented reports from shift records. It is not a production-deployed operational system.

</div>

## Project purpose

Production facilities often store shift logs in Excel files and unstructured text columns. This application brings the following operations into a single desktop workflow:

1. Import an Excel workbook.
2. Identify columns that may contain personal data using heuristic checks.
3. Filter records by the selected date range.
4. Analyze the prepared dataset with a selected LLM provider.
5. Review the result in the application and export PDF or Excel reports.

```text
Excel workbook
       |
       v
File validation --> potential personal-data minimization --> date filtering
                                                                  |
                                                                  v
                                                         LLM-based analysis
                                                                  |
                                                                  v
                                                          PDF / Excel report
```

## Screenshots

The Turkish README references screenshots of data preparation, date filtering, AI analysis, and report previews under `docs/screenshots/`. **Those image files are not currently tracked in this repository**, so this page does not display broken image embeds. See the application's source and demo entry point below.

## Key features

- Read `.xlsx` shift records; `.xls` support depends on the environment and `xlrd` compatibility.
- Merge data from multiple worksheets.
- Detect potential personal-data fields using column names and sample content.
- Filter by 1/7/30/60/90/180 days or a custom date range.
- Select among OpenAI, Anthropic, and xAI providers.
- Generate operational summaries, recurring issue analysis, recommended actions, and trend assessments.
- Export results to PDF and Excel.
- Write local JSON process/audit logs.
- Check file size, extension, and signature.

## Installation

### Requirements

- Windows 10 or 11.
- Python 3.8+.
- Tkinter (normally included with standard Python installations on Windows).
- An API key from a supported provider for AI analysis.

### Quick start

```powershell
git clone https://github.com/Merd0/ai-shift-analysis-assistant.git
cd ai-shift-analysis-assistant

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python vardiya_gui.py
```

If the Windows terminal encounters an emoji-related encoding error:

```powershell
$env:PYTHONUTF8 = "1"
python vardiya_gui.py
```

## Usage

1. Open **File Analysis** to select an Excel file.
2. Run file checks and inspect the column analysis.
3. Choose a period under **Date Filter**.
4. Select a provider/model and enter an API key under **AI Analysis**.
5. Review the generated analysis.
6. Export PDF or Excel results under **Reports**.

The application also provides a demo menu:

```powershell
python demo.py
```

> The application's actual UI labels are primarily **Turkish**. English documentation does not imply a localized application interface.

## Expected data

The program heuristically recognizes Turkish and English column names. No fixed schema is required, but these fields improve analysis:

| Field | Example columns | Purpose |
| --- | --- | --- |
| Time | `Tarih`, `Date`, `Zaman` | Record or shift timestamp |
| Shift | `Vardiya`, `Shift` | Shift name or period |
| Equipment | `Makine`, `Ekipman`, `Unit` | Equipment identification |
| Event | `Sorun`, `Açıklama`, `Description` | Operational note |
| Action | `Çözüm`, `Bakım`, `Action` | Taken or recommended action |

Back up source workbooks and review sensitive personal/corporate fields before processing real production data.

## Repository structure

```text
.
├── vardiya_gui.py       # Tkinter desktop UI
├── excel_analyzer.py    # Excel loading, cleanup, summaries
├── ai_analyzer.py       # Provider integrations and analysis flow
├── prompts.py           # Analysis prompts
├── file_security.py     # File type and integrity checks
├── security_audit.py    # Local audit logs
├── config.py            # Provider and model configuration
├── demo.py              # CLI/GUI demo menu
├── version.py           # Version information
└── docs/screenshots/    # Referenced screenshots; not currently tracked
```

## Security and personal data

The project uses **heuristic data-minimization aids**, not a verified legal or technical guarantee of KVKK compliance.

- Both false positives and false negatives are possible.
- Users must review all information before sending it to an AI provider.
- Provider retention and processing terms require separate consideration.
- Production use would require additional access controls, encryption, retention policies, and security testing.
- AI-generated findings must be validated by a qualified person before operational decisions.

To report a vulnerability, consult [SECURITY.md](SECURITY.md).

## Known limitations

- Desktop prototype; not a multi-user system.
- Rule/heuristic-based detection of potentially personal data.
- Results depend on column names and free-text structure.
- AI output varies with provider, model, and data quality.
- The Word export button is not functional in this version.
- File checks are not a substitute for antivirus scanning or sandboxing.

## Roadmap

- Facility-specific column-mapping profiles.
- Structured AI output grounded in records.
- Deterministic KPIs and anomaly detection.
- Automated tests and data-quality validation.
- Research toward a web-based, multi-user version.

## Background

The application originated as an internship project addressing the need to inspect and summarize production shift logs more efficiently. The public repository demonstrates a working prototype, a privacy-aware data-processing approach, and AI-assisted analysis techniques. It does not contain production records or represent a certified deployment.

## License

Released under the [MIT License](LICENSE).
