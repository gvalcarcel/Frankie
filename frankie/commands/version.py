from __future__ import annotations

from frankie.core.constants import MODE, PROJECT_NAME, READ_ONLY_MESSAGE, VERSION


def run() -> str:
    return "\n".join(
        [
            f"Frankie Core {VERSION}",
            f"Mode: {MODE}",
            f"Project: {PROJECT_NAME}",
            READ_ONLY_MESSAGE,
        ]
    )
