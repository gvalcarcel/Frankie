from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="frankie",
        description="Frankie Core read-only foundation CLI.",
        add_help=False,
    )
    parser.add_argument("command", nargs="?")
    parser.add_argument("evidence_action", nargs="?")
    parser.add_argument("evidence_id", nargs="?")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Return structured JSON for supported commands.",
    )
    parser.add_argument("-h", "--help", action="store_const", const="help", dest="command")
    return parser
