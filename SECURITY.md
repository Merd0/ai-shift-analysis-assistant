# Security Policy

## Supported version

This repository is a portfolio-stage desktop prototype. Security fixes are applied to the latest version on the `main` branch; older tags are not actively maintained.

## Reporting a vulnerability

Please do not publish a vulnerability, credential, production workbook, log file, or personal data in a public issue.

Use GitHub's private vulnerability reporting feature when it is available. Otherwise, open a public issue containing only a short, non-sensitive description and request a private communication channel.

Include the following information without attaching real production data:

- affected version or commit;
- operating system and Python version;
- steps required to reproduce the behavior;
- expected and observed results;
- a sanitized proof of concept, if available.

## Data and privacy scope

The application includes heuristic checks intended to reduce accidental processing of common personal-data fields. These checks are not a legal compliance certification and may produce false positives or false negatives.

Before processing operational data:

1. Work on a copy of the source workbook.
2. Remove personal, confidential, and trade-secret fields that are not required for analysis.
3. Review the data that will be sent to an external AI provider.
4. Evaluate the provider's retention, regional processing, and contractual terms.
5. Keep API keys out of source files, screenshots, logs, and Git history.

The file-validation module performs basic structural and signature checks. It is not a replacement for endpoint protection, malware scanning, sandboxing, or organizational security controls.

## Secrets

API keys are entered at runtime and must never be committed to the repository. If a key is exposed, revoke it immediately at the relevant provider and create a replacement.
