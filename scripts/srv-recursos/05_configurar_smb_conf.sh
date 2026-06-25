#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 05_configurar_smb_conf.sh
# Version: 2026-06-25
# Finalidad: insertar bloque gestionado Frankie en smb.conf.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
SMB_CONF="${SMB_CONF:-/etc/samba/smb.conf}"
BACKUP_SUFFIX="$(date +%Y%m%d_%H%M%S)"
BEGIN_MARK="# BEGIN FRANKIE SAMBA"
END_MARK="# END FRANKIE SAMBA"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root
[[ -f "$SMB_CONF" || "$DRY_RUN" == "true" ]] || { echo "ERROR: no existe $SMB_CONF" >&2; exit 1; }

BLOCK="$(cat <<'EOF'
# BEGIN FRANKIE SAMBA
[recursos]
	path = /srv/recursos
	valid users = alumno profesor
	read only = Yes

[instalables]
	path = /srv/recursos/01_INSTALABLES
	valid users = alumno profesor
	read only = Yes

[isos]
	path = /srv/recursos/02_ISOS
	valid users = alumno profesor
	read only = Yes
	write list = profesor
	force group = profesorado
	create mask = 0664
	directory mask = 02775

[material]
	path = /srv/recursos/04_MATERIAL_CLASE
	valid users = alumno profesor
	read only = Yes

[plantillas]
	path = /srv/recursos/05_PLANTILLAS
	valid users = alumno profesor
	read only = Yes

[practicas]
	path = /srv/recursos/06_PRACTICAS
	valid users = alumno profesor
	read only = Yes

[profesorado]
	path = /srv/recursos/99_PROFESORADO
	valid users = profesor
	read only = No
	browseable = No
	force group = profesorado
	create mask = 0660
	directory mask = 0770
# END FRANKIE SAMBA
EOF
)"

if "$DRY_RUN"; then
  echo "[DRY-RUN] crear backup $SMB_CONF.frankie-$BACKUP_SUFFIX.bak"
  echo "[DRY-RUN] insertar o sustituir bloque gestionado Frankie"
else
  cp -a "$SMB_CONF" "$SMB_CONF.frankie-$BACKUP_SUFFIX.bak"
  tmp="$(mktemp)"
  if grep -Fq "$BEGIN_MARK" "$SMB_CONF"; then
    awk -v begin="$BEGIN_MARK" -v end="$END_MARK" -v block="$BLOCK" '
      $0 == begin { print block; skip=1; next }
      $0 == end { skip=0; next }
      !skip { print }
    ' "$SMB_CONF" > "$tmp"
  else
    cat "$SMB_CONF" > "$tmp"
    printf '\n%s\n' "$BLOCK" >> "$tmp"
  fi
  if cmp -s "$SMB_CONF" "$tmp"; then
    log "smb.conf sin cambios"
    rm -f "$tmp"
  else
    mv "$tmp" "$SMB_CONF"
    testparm -s
    systemctl restart smbd
  fi
fi

log "Validacion"
run_cmd testparm -s
run_cmd systemctl status smbd --no-pager
