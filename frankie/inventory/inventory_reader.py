from __future__ import annotations

from frankie.core.constants import MODE, VERSION
from frankie.core.models import InventoryItem, InventoryReport, InventorySection
from frankie.core.paths import INVENTORY_SOURCE_PATHS, FrankiePaths


def build_inventory_report(paths: FrankiePaths | None = None) -> InventoryReport:
    repository = paths or FrankiePaths.discover()
    sources = _read_sources(repository)

    return InventoryReport(
        version=VERSION,
        mode=MODE,
        sections=(
            InventorySection(
                "Physical server",
                (
                    InventoryItem("Name", "Frankie"),
                    InventoryItem("Role", "Educational physical server"),
                    InventoryItem("Hypervisor", "Proxmox", _state_for("proxmox", sources)),
                    InventoryItem("Purpose", "Educational lab infrastructure"),
                ),
            ),
            InventorySection(
                "Frankie Core",
                (
                    InventoryItem("Role", "Read-only software tool"),
                    InventoryItem("Purpose", "Consult, audit, inventory and document known infrastructure"),
                    InventoryItem("Repository", "Documentation, scripts, evidence and source code"),
                ),
            ),
            InventorySection(
                "Virtual machines",
                (
                    InventoryItem("VM100", "srv-servicios"),
                    InventoryItem(
                        "VM100 role",
                        "Services server",
                    ),
                    InventoryItem(
                        "VM100 known services",
                        "Docker, Portainer, PostgreSQL, n8n, backups, UFW, Fail2ban",
                        _state_for_all(("docker", "portainer", "postgresql", "n8n"), sources),
                    ),
                    InventoryItem("VM101", "srv-recursos"),
                    InventoryItem("VM101 role", "Resources server"),
                    InventoryItem(
                        "VM101 known services",
                        "Samba, shared classroom resources, alumnado/profesorado access model",
                        _state_for("samba", sources),
                    ),
                ),
            ),
            InventorySection(
                "Docker",
                (
                    InventoryItem("Network", "aula-network", _state_for("aula-network", sources)),
                    InventoryItem(
                        "Containers",
                        "Portainer, PostgreSQL, n8n",
                        _state_for_all(("portainer", "postgresql", "n8n"), sources),
                    ),
                ),
            ),
            InventorySection(
                "Resources",
                (
                    InventoryItem("Root path", "/srv/recursos", _state_for("/srv/recursos", sources)),
                    InventoryItem(
                        "Shares",
                        "recursos, instalables, isos, material, plantillas, practicas, profesorado",
                        _shares_state(sources),
                    ),
                ),
            ),
            InventorySection(
                "Security",
                (
                    InventoryItem("Firewall", "UFW", _state_for("ufw", sources)),
                    InventoryItem("Intrusion prevention", "Fail2ban", _state_for("fail2ban", sources)),
                    InventoryItem(
                        "PostgreSQL exposure",
                        "not exposed on host port 5432",
                        _postgres_exposure_state(sources),
                    ),
                ),
            ),
            InventorySection(
                "Backups",
                (
                    InventoryItem(
                        "srv-servicios backup evidence",
                        "known",
                        _state_for_any(("backup", "backups"), sources),
                    ),
                    InventoryItem(
                        "srv-recursos backup evidence",
                        "known",
                        _state_for_any(("/srv/backups/recursos", "/srv/scripts/backup-recursos.sh"), sources),
                    ),
                ),
            ),
            InventorySection(
                "Evidence",
                (
                    InventoryItem("Source", "repository documentation and audit evidence"),
                    InventoryItem("Live connection", "no"),
                    InventoryItem("Available sources", _available_sources(repository), _source_state(repository)),
                    InventoryItem("Missing sources", _missing_sources(repository), _missing_source_state(repository)),
                ),
            ),
        ),
    )


def _read_sources(paths: FrankiePaths) -> str:
    contents: list[str] = []
    for relative_path in INVENTORY_SOURCE_PATHS:
        text = paths.read_text(relative_path)
        if text:
            contents.append(text.lower())
    return "\n".join(contents)


def _state_for(term: str, sources: str) -> str:
    if term.lower() in sources:
        return "KNOWN"
    return "UNKNOWN"


def _state_for_any(terms: tuple[str, ...], sources: str) -> str:
    if any(term.lower() in sources for term in terms):
        return "KNOWN"
    return "UNKNOWN"


def _state_for_all(terms: tuple[str, ...], sources: str) -> str:
    found = [term for term in terms if term.lower() in sources]
    if len(found) == len(terms):
        return "KNOWN"
    if found:
        return "PARTIAL"
    return "UNKNOWN"


def _shares_state(sources: str) -> str:
    shares = ("recursos", "instalables", "isos", "material", "plantillas", "practicas", "profesorado")
    return _state_for_all(shares, sources)


def _postgres_exposure_state(sources: str) -> str:
    evidence = (
        "postgresql no expone 5432",
        "5432 no escucha",
        "sin 5432",
        "not exposed on host port 5432",
    )
    return _state_for_any(evidence, sources)


def _available_sources(paths: FrankiePaths) -> str:
    found = [relative_path for relative_path in INVENTORY_SOURCE_PATHS if paths.exists(relative_path)]
    if not found:
        return "none"
    return f"{len(found)} of {len(INVENTORY_SOURCE_PATHS)}"


def _missing_sources(paths: FrankiePaths) -> str:
    missing = [relative_path for relative_path in INVENTORY_SOURCE_PATHS if not paths.exists(relative_path)]
    if not missing:
        return "none"
    return ", ".join(missing)


def _source_state(paths: FrankiePaths) -> str:
    found = [relative_path for relative_path in INVENTORY_SOURCE_PATHS if paths.exists(relative_path)]
    if len(found) == len(INVENTORY_SOURCE_PATHS):
        return "KNOWN"
    if found:
        return "PARTIAL"
    return "MISSING EVIDENCE"


def _missing_source_state(paths: FrankiePaths) -> str:
    if all(paths.exists(relative_path) for relative_path in INVENTORY_SOURCE_PATHS):
        return "KNOWN"
    return "MISSING EVIDENCE"
