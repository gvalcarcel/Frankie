#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 01_instalar_dependencias.sh
# Version: 2026-06-25
# Finalidad: instalar dependencias base del servidor de servicios.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
PACKAGES=(ca-certificates curl gnupg lsb-release apt-transport-https tree nano ufw fail2ban)

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;;
  esac
done

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() {
  if "$DRY_RUN"; then
    echo "[DRY-RUN] $*"
  else
    "$@"
  fi
}
require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "ERROR: ejecuta este script con sudo o como root." >&2
    exit 1
  fi
}
pkg_installed() { dpkg -s "$1" >/dev/null 2>&1; }

require_root

log "Actualizando indice APT"
run_cmd apt update

missing=()
for pkg in "${PACKAGES[@]}"; do
  if ! pkg_installed "$pkg"; then
    missing+=("$pkg")
  fi
done

if [[ "${#missing[@]}" -gt 0 ]]; then
  log "Instalando paquetes pendientes: ${missing[*]}"
  run_cmd env DEBIAN_FRONTEND=noninteractive apt install -y "${missing[@]}"
else
  log "Todos los paquetes base ya estan instalados"
fi

log "Validacion"
for pkg in "${PACKAGES[@]}"; do
  if "$DRY_RUN"; then
    echo "[DRY-RUN] validar paquete $pkg"
  elif pkg_installed "$pkg"; then
    echo "OK: $pkg instalado"
  else
    echo "ERROR: $pkg no esta instalado" >&2
    exit 1
  fi
done
