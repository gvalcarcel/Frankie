#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 02_crear_usuarios_samba.sh
# Version: 2026-06-25
# Finalidad: crear grupos y usuarios funcionales para Samba.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
ALUMNO_USER="${ALUMNO_USER:-alumno}"
PROFESOR_USER="${PROFESOR_USER:-profesor}"
ALUMNADO_GROUP="${ALUMNADO_GROUP:-alumnado}"
PROFESORADO_GROUP="${PROFESORADO_GROUP:-profesorado}"
LOGIN_SHELL="/usr/sbin/nologin"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

for group in "$ALUMNADO_GROUP" "$PROFESORADO_GROUP"; do
  getent group "$group" >/dev/null || run_cmd groupadd "$group"
done

if ! id "$ALUMNO_USER" >/dev/null 2>&1; then
  run_cmd useradd -M -s "$LOGIN_SHELL" -g "$ALUMNO_USER" "$ALUMNO_USER" || run_cmd useradd -M -s "$LOGIN_SHELL" "$ALUMNO_USER"
fi
if ! id "$PROFESOR_USER" >/dev/null 2>&1; then
  run_cmd useradd -M -s "$LOGIN_SHELL" "$PROFESOR_USER"
fi

run_cmd usermod -aG "$ALUMNADO_GROUP" "$ALUMNO_USER"
run_cmd usermod -aG "$PROFESORADO_GROUP" "$PROFESOR_USER"

log "No se establecen contrasenas reales en este script."
log "Configurar Samba de forma interactiva y segura:"
echo "  sudo smbpasswd -a $ALUMNO_USER"
echo "  sudo smbpasswd -a $PROFESOR_USER"
echo "  sudo smbpasswd -e $ALUMNO_USER"
echo "  sudo smbpasswd -e $PROFESOR_USER"

log "Validacion"
run_cmd id "$ALUMNO_USER"
run_cmd id "$PROFESOR_USER"
run_cmd pdbedit -L
