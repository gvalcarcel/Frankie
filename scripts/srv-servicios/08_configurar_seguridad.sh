#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 08_configurar_seguridad.sh
# Version: 2026-06-25
# Finalidad: configurar UFW y Fail2ban para srv-servicios.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
JAIL_FILE="/etc/fail2ban/jail.d/frankie-sshd.conf"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

run_cmd ufw default deny incoming
run_cmd ufw default allow outgoing
for rule in "22/tcp" "5678/tcp" "9443/tcp"; do
  run_cmd ufw allow "$rule"
done
run_cmd ufw --force enable

if "$DRY_RUN"; then
  echo "[DRY-RUN] escribir $JAIL_FILE"
else
  cat > "$JAIL_FILE" <<'EOF'
[sshd]
enabled = true
bantime = 24h
findtime = 10m
maxretry = 5
backend = systemd
EOF
fi
run_cmd systemctl restart fail2ban

log "Validacion"
run_cmd ufw status verbose
run_cmd fail2ban-client status sshd
