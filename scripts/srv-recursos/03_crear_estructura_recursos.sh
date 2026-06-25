#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 03_crear_estructura_recursos.sh
# Version: 2026-06-25
# Finalidad: crear arbol base de /srv/recursos.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
BASE_DIR="${BASE_DIR:-/srv/recursos}"
DIRS=(00_LEEME 01_INSTALABLES 02_ISOS 03_DRIVERS 04_MATERIAL_CLASE 05_PLANTILLAS 06_PRACTICAS 07_ENTREGAS 99_PROFESORADO)

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root
for dir in "${DIRS[@]}"; do run_cmd mkdir -p "$BASE_DIR/$dir"; done

README="$BASE_DIR/00_LEEME/README.txt"
if [[ ! -f "$README" ]]; then
  if "$DRY_RUN"; then
    echo "[DRY-RUN] crear $README"
  else
    cat > "$README" <<'EOF'
Recursos compartidos del aula.

01_INSTALABLES: instaladores comunes.
02_ISOS: imagenes ISO.
03_DRIVERS: controladores.
04_MATERIAL_CLASE: materiales de consulta.
05_PLANTILLAS: plantillas.
06_PRACTICAS: enunciados y recursos de practicas.
07_ENTREGAS: zona prevista para entregas.
99_PROFESORADO: zona privada del profesorado.
EOF
  fi
fi

log "Validacion"
run_cmd tree -L 2 "$BASE_DIR"
