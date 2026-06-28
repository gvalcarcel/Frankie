# Índice de agentes

| Agent | Category | Best used for | Mode | Main risk controlled | Suggested companion agents | File path |
|---|---|---|---|---|---|---|
| Hardware Infrastructure Architect | Hardware | Host design and capacity | BOTH | Unsupported or undersized architecture | Proxmox Administrator, Storage Administrator | `docs/agents/hardware/hardware-infrastructure-architect.md` |
| Physical Server Technician | Hardware | Hands-on host maintenance | LIVE | Physical damage or unsafe outage | Hardware Architect, System Auditor | `docs/agents/hardware/physical-server-technician.md` |
| Proxmox / Virtualization Administrator | Hardware | VM and hypervisor lifecycle | BOTH | Disruptive VM or storage operations | Network Administrator, LIVE Controller | `docs/agents/hardware/proxmox-virtualization-administrator.md` |
| Network Administrator | Hardware | Addressing, connectivity and exposure | BOTH | Lockout or unnecessary port exposure | Security Reviewer, Service Administrator | `docs/agents/hardware/network-administrator.md` |
| Storage and Backup Administrator | Hardware | Capacity, backup and recovery | BOTH | Data loss or false recoverability | System Auditor, Security Reviewer | `docs/agents/hardware/storage-backup-administrator.md` |
| Service Administrator | Hardware | Docker, Samba and system services | BOTH | Unplanned service interruption | LIVE Controller, Security Reviewer | `docs/agents/hardware/service-administrator.md` |
| LIVE Operations Controller | Hardware | Any real infrastructure access | LIVE | Unauthorized or expanded live scope | Security Reviewer, System Auditor | `docs/agents/hardware/live-operations-controller.md` |
| Software Architect | Software | Modules, contracts and dependencies | OFFLINE | Architectural drift and coupling | Python Developer, QA Engineer | `docs/agents/software/software-architect.md` |
| Python Developer | Software | Frankie Core implementation | OFFLINE | Hidden side effects and regressions | Software Architect, QA Engineer | `docs/agents/software/python-developer.md` |
| CLI Designer | Software | Commands, help and exit behavior | OFFLINE | Confusing or unsafe command semantics | UX Writer, Python Developer | `docs/agents/software/cli-designer.md` |
| QA Engineer | Software | Tests and release gates | BOTH | Unverified behavior and regressions | Security Reviewer, System Auditor | `docs/agents/software/qa-engineer.md` |
| Data Model Designer | Software | JSON and domain contracts | OFFLINE | Unstable or unsafe schemas | Evidence Engineer, Software Architect | `docs/agents/software/data-model-designer.md` |
| Evidence Engineer | Software | Evidence lineage and sanitization | BOTH | Stale, invented or sensitive evidence | Security Reviewer, System Auditor | `docs/agents/software/evidence-engineer.md` |
| Release Manager | Software | Version, tag and GitHub Release | OFFLINE | Wrong or mutable release artifact | Repository Maintainer, QA Engineer | `docs/agents/software/release-manager.md` |
| Repository Maintainer | Software | Git hygiene and remote synchronization | OFFLINE | Secrets or unrelated files in Git | Security Reviewer, Release Manager | `docs/agents/software/repository-maintainer.md` |
| Automation Readiness Engineer | Software | Safe automation design | OFFLINE | Automating unclear or unsafe procedures | DevOps Engineer, QA Engineer | `docs/agents/software/automation-readiness-engineer.md` |
| Security Reviewer | Transversal | Secrets, privilege and exposure | BOTH | Security compromise | System Auditor, LIVE Controller | `docs/agents/transversal/security-reviewer.md` |
| System Auditor | Transversal | Evidence-based compliance and closure | BOTH | Unsupported conclusions | Evidence Engineer, QA Engineer | `docs/agents/transversal/system-auditor.md` |
| Technical Writer | Transversal | Technical and release documentation | OFFLINE | Inaccurate or ambiguous documentation | UX Writer, System Auditor | `docs/agents/transversal/technical-writer.md` |
| DevOps Engineer | Transversal | Delivery and operational workflows | BOTH | Non-reproducible deployment | Automation Engineer, Security Reviewer | `docs/agents/transversal/devops-engineer.md` |
| DevOps Educativo | Transversal | Authentic classroom DevOps practice | OFFLINE | Unsafe or shallow learning activities | Docente FP Básica, UX Writer | `docs/agents/transversal/devops-educativo.md` |
| Docente FP Básica | Transversal | Accessible classroom material | OFFLINE | Content above student level | DevOps Educativo, Technical Writer | `docs/agents/transversal/docente-fp-basica.md` |
| Product Owner | Transversal | Scope, value and acceptance | OFFLINE | Scope growth without value | Software Architect, System Auditor | `docs/agents/transversal/product-owner.md` |
| UX Writer | Transversal | CLI messages and guidance | OFFLINE | Misunderstood actions or errors | CLI Designer, Technical Writer | `docs/agents/transversal/ux-writer.md` |

`BOTH` means the agent can contribute to OFFLINE design and authorized LIVE execution. It does not grant LIVE permission.
