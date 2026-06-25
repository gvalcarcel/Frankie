#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 07_configurar_backup_recursos.sh
# Version: 2026-06-25
# Finalidad: configurar backup diario de recursos y Samba.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
BACKUP_BASE="${BACKUP_BASE:-/srv/backups/recursos}"
SCRIPT_PATH="${SCRIPT_PATH:-/srv/scripts/backup-recursos.sh}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
BACKUP_ISOS="${BACKUP_ISOS:-false}"
CRON_LINE="0 2 * * * ${SCRIPT_PATH}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root
run_cmd mkdir -p "$BACKUP_BASE/logs" "$(dirname "$SCRIPT_PATH")"

if "$DRY_RUN"; then
  echo "[DRY-RUN] generar $SCRIPT_PATH"
else
  cat > "$SCRIPT_PATH" <<EOF
#!/bin/bash
set -euo pipefail
FECHA="\$(date +%Y%m%d_%H%M%S)"
BASE="$BACKUP_BASE"
RETENTION_DAYS="$RETENTION_DAYS"
BACKUP_ISOS="$BACKUP_ISOS"
mkdir -p "\$BASE/logs"
echo "==== INICIO \$FECHA ====" >> "\$BASE/logs/backup.log"
EXCLUDES=()
if [[ "\$BACKUP_ISOS" != "true" ]]; then
  EXCLUDES+=(--exclude=/srv/recursos/02_ISOS)
fi
tar -czf "\$BASE/recursos_\$FECHA.tar.gz" "\${EXCLUDES[@]}" /srv/recursos
cp -a /etc/samba/smb.conf "\$BASE/smb.conf_\$FECHA"
find "\$BASE" -maxdepth 1 -name "recursos_*.tar.gz" -mtime +"\$RETENTION_DAYS" -delete
find "\$BASE" -maxdepth 1 -name "smb.conf_*" -mtime +"\$RETENTION_DAYS" -delete
echo "==== FIN \$FECHA ====" >> "\$BASE/logs/backup.log"
EOF
  chmod 750 "$SCRIPT_PATH"
fi

if "$DRY_RUN"; then
  echo "[DRY-RUN] instalar cron: $CRON_LINE"
else
  current="$(mktemp)"
  crontab -l 2>/dev/null > "$current" || true
  grep -Fq "$SCRIPT_PATH" "$current" || echo "$CRON_LINE" >> "$current"
  crontab "$current"
  rm -f "$current"
fi

log "Validacion"
run_cmd crontab -l
