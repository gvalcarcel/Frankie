from __future__ import annotations

import sys
from collections.abc import Sequence

from frankie.cli.parser import build_parser
from frankie.commands import audit, doctor, evidence, help, inventory, report, status, version
from frankie.reports.writer import ReportOutputError


COMMANDS = {
    "version": version.run,
    "help": help.run,
    "status": status.run,
    "inventory": inventory.run,
    "audit": audit.run,
    "doctor": doctor.run,
    "evidence": None,
    "report": None,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "help"

    if command not in COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Run 'frankie help' to see available commands.", file=sys.stderr)
        return 2

    if command != "evidence" and (args.evidence_action or args.evidence_id):
        print(f"Unexpected argument for command '{command}'.", file=sys.stderr)
        print("Run 'frankie help' to see valid command syntax.", file=sys.stderr)
        return 2

    if args.verbose and command not in {"audit", "doctor"}:
        print(f"Verbose output is not available for command: {command}", file=sys.stderr)
        return 2

    if args.json_output and command not in {"status", "inventory", "audit", "doctor", "evidence", "report"}:
        print(f"JSON output is not available for command: {command}", file=sys.stderr)
        return 2

    if args.markdown_output and command != "report":
        print(f"Markdown output is not available for command: {command}", file=sys.stderr)
        return 2
    if args.json_output and args.markdown_output:
        print("Choose either --json or --markdown, not both.", file=sys.stderr)
        return 2
    if (args.output_path or args.force) and command != "report":
        print("--output and --force are only available for the report command.", file=sys.stderr)
        return 2
    if args.force and not args.output_path:
        print("--force requires --output.", file=sys.stderr)
        return 2

    if command == "evidence":
        return _run_evidence(args.evidence_action, args.evidence_id, args.json_output)

    if command == "report":
        try:
            print(
                report.generate(
                    json_output=args.json_output,
                    markdown_output=args.markdown_output,
                    output_path=args.output_path,
                    force=args.force,
                )
            )
        except ReportOutputError as exc:
            print(f"Report output error: {exc}", file=sys.stderr)
            return 2
        return 0

    handler = COMMANDS[command]
    if command in {"audit", "doctor"}:
        print(handler(verbose=args.verbose, json_output=args.json_output))
    elif command in {"status", "inventory"}:
        print(handler(json_output=args.json_output))
    else:
        print(handler())
    return 0


def _run_evidence(action: str | None, evidence_id: str | None, json_output: bool) -> int:
    if action is None:
        print("Evidence action required: list, validate, summary or show.", file=sys.stderr)
        return 2
    if action not in {"list", "validate", "summary", "show"}:
        print(f"Unknown evidence action: {action}", file=sys.stderr)
        return 2
    if action == "show" and not evidence_id:
        print("Evidence id required for 'evidence show'.", file=sys.stderr)
        return 2
    if action != "show" and evidence_id:
        print(f"Unexpected evidence id for 'evidence {action}'.", file=sys.stderr)
        return 2
    if json_output and action not in {"show", "summary"}:
        print("JSON output is only available for 'evidence show' and 'evidence summary'.", file=sys.stderr)
        return 2

    output, exit_code = evidence.dispatch(action, evidence_id=evidence_id, json_output=json_output)
    print(output, file=sys.stderr if exit_code else sys.stdout)
    return exit_code
