from __future__ import annotations

from dataclasses import dataclass


ALLOWED_STATES = ("OK", "WARNING", "ERROR", "UNKNOWN", "PENDING", "MISSING EVIDENCE")
ALLOWED_INVENTORY_STATES = ("KNOWN", "UNKNOWN", "PARTIAL", "PENDING", "MISSING EVIDENCE")


@dataclass(frozen=True)
class StatusItem:
    name: str
    state: str
    detail: str = ""

    def __post_init__(self) -> None:
        if self.state not in ALLOWED_STATES:
            raise ValueError(f"Unsupported status state: {self.state}")


@dataclass(frozen=True)
class StatusSection:
    title: str
    items: tuple[StatusItem, ...]


@dataclass(frozen=True)
class StatusReport:
    version: str
    mode: str
    sections: tuple[StatusSection, ...]
    overall_status: str


@dataclass(frozen=True)
class InventoryItem:
    name: str
    value: str
    state: str = "KNOWN"

    def __post_init__(self) -> None:
        if self.state not in ALLOWED_INVENTORY_STATES:
            raise ValueError(f"Unsupported inventory state: {self.state}")


@dataclass(frozen=True)
class InventorySection:
    title: str
    items: tuple[InventoryItem, ...]


@dataclass(frozen=True)
class InventoryReport:
    version: str
    mode: str
    sections: tuple[InventorySection, ...]
