# Automated validation result

## Identification

- Work Order: `WO-0020`.
- Generated at: `2026-06-28T12:24:40+02:00`.
- Mode: `offline`.
- Result: `PASS`.
- Output directory: `docs/evidencias/frankie-core-v0.8.0/wo-0020`.

## Checks

| Check | Result |
| --- | --- |
| Unit and integration tests | PASS (90 tests) |
| Python compilation | PASS |
| CLI regression | PASS (14 commands) |
| Structured evidence | PASS (7 valid, 0 invalid) |
| Markdown report export | PASS |
| JSON report export and parsing | PASS |
| Repository delta | PASS |

The Git baseline contained pre-existing Work Order changes. The final delta check accepts only the four generated artifacts in this output directory and preserves any pre-existing changes without modifying them.

## Artifacts

| File | SHA-256 |
| --- | --- |
| `consolidated_report.md` | `416A0BD8698AC11DAC38BB14B6F6C491A1DE6B718100BD77BDDD84234A51B772` |
| `consolidated_report.json` | `C1822E9539C6A54A8C8F51684E64265350533FD8D5AD5C4D0181BCB000E450F2` |
| `validation_evidence.json` | `EDDEFE92A5A4C078DA654576E4339F906C9CC7398125244D4441274B1E36A693` |

## Safety

- No connection to Frankie or its virtual machines.
- No package installation, service restart or configuration change.
- No secrets, credentials or internal addresses collected.
- Files are written only inside `docs/evidencias/`.
- Existing artifacts are not replaced unless `--force` is explicit.

## Limitations

- Results describe the local repository and documented evidence, not current LIVE infrastructure.
- The generated execution evidence is validated with the Frankie loader but is not added automatically to the canonical structured evidence catalog.
- Git cleanliness is a delta check; use `--require-clean` when a completely clean baseline is mandatory.
