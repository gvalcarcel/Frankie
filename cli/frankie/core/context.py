from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_MARKERS = ("README.md", "ROADMAP.md", "governance", "knowledge")


@dataclass(frozen=True)
class AppContext:
    repo_root: Path | None

    @classmethod
    def discover(cls, start: Path | None = None) -> "AppContext":
        current = (start or Path.cwd()).resolve()
        for candidate in (current, *current.parents):
            if all((candidate / marker).exists() for marker in REPO_MARKERS):
                return cls(candidate)
        return cls(None)

    def path(self, relative_path: str) -> Path | None:
        if not self.repo_root:
            return None
        return self.repo_root / relative_path

    def existing_paths(self, relative_paths: list[str]) -> list[str]:
        found: list[str] = []
        for relative_path in relative_paths:
            path = self.path(relative_path)
            if path and path.exists():
                found.append(relative_path)
        return found
