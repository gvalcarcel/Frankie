from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Payload:
    title: str
    status: str
    summary: str
    data: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "status": self.status,
            "summary": self.summary,
            "data": self.data,
        }
