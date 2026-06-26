from __future__ import annotations

from frankie.core.models import AuditCheck


AUDIT_CHECKS = (
    AuditCheck(
        id="AUD-EVIDENCE-001",
        name="Evidence files available",
        description="Validate that the required step 5 audit evidence files are available.",
        category="Evidence",
    ),
    AuditCheck(
        id="AUD-REPORT-001",
        name="Audit report dry-run decision",
        description="Evaluate whether the documented audit report is apt for dry-run.",
        category="Evidence",
    ),
    AuditCheck(
        id="AUD-SERVICES-PORTAINER-001",
        name="Known Portainer port deviation",
        description="Check whether Portainer has the documented port 8000 deviation.",
        category="Services",
    ),
    AuditCheck(
        id="AUD-SAMBA-001",
        name="SMB Windows client validation",
        description="Check whether Samba validation from a real Windows or SMB client is pending or resolved by newer evidence.",
        category="Samba",
    ),
    AuditCheck(
        id="AUD-POSTGRES-001",
        name="PostgreSQL external exposure",
        description="Check whether evidence indicates PostgreSQL is not exposed on host port 5432.",
        category="Security",
    ),
    AuditCheck(
        id="AUD-CORE-READONLY-001",
        name="Frankie Core read-only mode",
        description="Confirm that Audit Engine v1 is documented and implemented as a read-only flow.",
        category="Core",
    ),
    AuditCheck(
        id="AUD-CONCEPTS-001",
        name="Frankie concepts distinction",
        description="Validate the distinction between Frankie, Frankie Core and the Frankie repository.",
        category="Concepts",
    ),
)
