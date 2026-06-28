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
        "--simulate",
        action="store_true",
        help="Use fictitious offline Live Mode data; never contacts Frankie.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Return structured JSON for supported commands.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        dest="markdown_output",
        help="Return Markdown for the report command.",
    )
    parser.add_argument("--output", dest="output_path", help="Write report output inside docs/evidencias/.")
    parser.add_argument("--force", action="store_true", help="Allow report output to replace an existing file.")
    parser.add_argument("-h", "--help", action="store_const", const="help", dest="command")
    return parser
