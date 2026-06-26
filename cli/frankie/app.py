from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from frankie.commands import audit, help as help_command, inventory, status, version
from frankie.core.context import AppContext
from frankie.core.output import OutputError, emit


COMMANDS = {
    "version": version.run,
    "status": status.run,
    "inventory": inventory.run,
    "audit": audit.run,
    "help": help_command.run,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="frankie",
        description="Read-only CLI for the Frankie infrastructure repository.",
        add_help=False,
    )
    parser.add_argument("command", nargs="?", default="help", choices=sorted(COMMANDS))
    parser.add_argument(
        "--format",
        choices=("text", "json", "markdown"),
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        help="Optional file path for writing command output. Without this flag, no file is written.",
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.help:
        args.command = "help"

    context = AppContext.discover()
    payload = COMMANDS[args.command](context)

    try:
        emit(payload, args.format, args.output)
    except OutputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0
