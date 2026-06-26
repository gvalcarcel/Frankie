from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="frankie",
        description="Frankie Core read-only foundation CLI.",
        add_help=False,
    )
    parser.add_argument("command", nargs="?")
    parser.add_argument("-h", "--help", action="store_const", const="help", dest="command")
    return parser
