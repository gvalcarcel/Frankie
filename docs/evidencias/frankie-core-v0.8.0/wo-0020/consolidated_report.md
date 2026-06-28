# Frankie Core Consolidated Report

- Frankie Core version: `0.8.0-dev`
- Mode: `offline`
- Generated at: `2026-06-28T12:24:51+02:00`
- Data source: `documented_evidence`

## Executive summary

Frankie Core consolidated documented evidence with overall status WARNING and audit result WARN.

## Overall status

- Status: `WARNING`
- Audit: `WARN`
- Doctor: `ACTIONS_RECOMMENDED`

## Inventory summary

### Physical server

- **Name:** Frankie (`KNOWN`)
- **Role:** Educational physical server (`KNOWN`)
- **Hypervisor:** Proxmox (`KNOWN`)
- **Purpose:** Educational lab infrastructure (`KNOWN`)

### Frankie Core

- **Role:** Read-only software tool (`KNOWN`)
- **Purpose:** Consult, audit, inventory and document known infrastructure (`KNOWN`)
- **Repository:** Documentation, scripts, evidence and source code (`KNOWN`)

### Virtual machines

- **VM100:** srv-servicios (`KNOWN`)
- **VM100 role:** Services server (`KNOWN`)
- **VM100 known services:** Docker, Portainer, PostgreSQL, n8n, backups, UFW, Fail2ban (`KNOWN`)
- **VM101:** srv-recursos (`KNOWN`)
- **VM101 role:** Resources server (`KNOWN`)
- **VM101 known services:** Samba, shared classroom resources, alumnado/profesorado access model (`KNOWN`)

### Docker

- **Network:** aula-network (`KNOWN`)
- **Containers:** Portainer, PostgreSQL, n8n (`KNOWN`)

### Resources

- **Root path:** /srv/recursos (`KNOWN`)
- **Shares:** recursos, instalables, isos, material, plantillas, practicas, profesorado (`KNOWN`)

### Security

- **Firewall:** UFW (`KNOWN`)
- **Intrusion prevention:** Fail2ban (`KNOWN`)
- **PostgreSQL exposure:** not exposed on host port 5432 (`KNOWN`)

### Backups

- **srv-servicios backup evidence:** known (`KNOWN`)
- **srv-recursos backup evidence:** known (`KNOWN`)

### Evidence

- **Source:** repository documentation and audit evidence (`KNOWN`)
- **Live connection:** no (`KNOWN`)
- **Available sources:** 15 of 15 (`KNOWN`)
- **Missing sources:** none (`KNOWN`)

## Audit findings

- **AUD-EVIDENCE-001:** Evidence files available (`PASS / INFO`)
  - Required step 5 audit evidence files are available.
- **AUD-REPORT-001:** Audit report dry-run decision (`PASS / INFO`)
  - The audit report indicates that the environment is apt for dry-run.
- **AUD-SERVICES-PORTAINER-001:** Known Portainer port deviation (`WARN / LOW`)
  - Portainer publishes port 8000 although it is documented as not allowed by UFW.
- **AUD-SAMBA-001:** SMB Windows client validation (`PASS / INFO`)
  - Historical SMB validation was pending, but pre-release evidence validates SMB from a real client.
- **AUD-POSTGRES-001:** PostgreSQL external exposure (`PASS / INFO`)
  - Evidence indicates PostgreSQL is not exposed on host port 5432.
- **AUD-CORE-READONLY-001:** Frankie Core read-only mode (`PASS / INFO`)
  - Frankie Core read-only behavior is documented.
- **AUD-CONCEPTS-001:** Frankie concepts distinction (`PASS / INFO`)
  - Documentation distinguishes Frankie, Frankie Core and the Frankie repository.

## Doctor diagnosis

- **AUD-SERVICES-PORTAINER-001:** Portainer port 8000 remains published
  - Impact: Portainer is documented as exposing port 8000 in addition to its main access port.
  - Recommended action: Review the port exposure in a future explicitly authorized LIVE Work Order.

## Evidence summary

- Valid evidence: `7`
- Invalid evidence: `0`
- By status: `ACTIVE: 1`, `OK: 2`, `PASS: 1`, `RELEASED: 1`, `WARN: 1`, `WARNING: 1`
- By severity: `INFO: 5`, `LOW: 2`
- By mode: `offline: 7`

## Known state

- SMB: `OK / PASS / INFO`
- Portainer: `WARNING / WARN / LOW`

## Known risks

- AUD-SERVICES-PORTAINER-001: Known Portainer port deviation (WARN / LOW)

## Limitations

- Frankie physical server was not consulted.
- The report is based on documented repository evidence.
- Live Mode is not implemented.
- Repair Mode is not implemented.

## Recommended next steps

- Revisar si el puerto 8000 debe mantenerse publicado o eliminarse del compose si no es necesario.
