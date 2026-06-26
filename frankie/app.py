from __future__ import annotations

import sys
from collections.abc import Sequence

from frankie.cli.parser import build_parser
from frankie.commands import audit, doctor, help, inventory, status, version


COMMANDS = {
    "version": version.run,
    "help": help.run,
    "status": status.run,
    "inventory": inventory.run,
    "audit": audit.run,
    "doctor": doctor.run,
}


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "help"

    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Run 'frankie help' to see available commands.", file=sys.stderr)
        return 2

    if command in {"audit", "doctor"}:
        print(handler(verbose=args.verbose))
    else:
        print(handler())
    return 0
