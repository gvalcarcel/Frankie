from __future__ import annotations

import sys
from collections.abc import Sequence

from frankie.cli.parser import build_parser
from frankie.commands import audit, doctor, evidence, help, inventory, status, version


COMMANDS = {
    "version": version.run,
    "help": help.run,
    "status": status.run,
    "inventory": inventory.run,
    "audit": audit.run,
    "doctor": doctor.run,
    "evidence": None,
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

    if args.json_output and command not in {"status", "inventory", "audit", "doctor", "evidence"}:
        print(f"JSON output is not available for command: {command}", file=sys.stderr)
        return 2

    if command == "evidence":
        return _run_evidence(args.evidence_action, args.evidence_id, args.json_output)

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
        print("Evidence action required: list, validate or show.", file=sys.stderr)
        return 2
    if action not in {"list", "validate", "show"}:
        print(f"Unknown evidence action: {action}", file=sys.stderr)
        return 2
    if action == "show" and not evidence_id:
        print("Evidence id required for 'evidence show'.", file=sys.stderr)
        return 2
    if action != "show" and evidence_id:
        print(f"Unexpected evidence id for 'evidence {action}'.", file=sys.stderr)
        return 2
    if json_output and action != "show":
        print("JSON output is only available for 'evidence show'.", file=sys.stderr)
        return 2

    output, exit_code = evidence.dispatch(action, evidence_id=evidence_id, json_output=json_output)
    print(output, file=sys.stderr if exit_code else sys.stdout)
    return exit_code
