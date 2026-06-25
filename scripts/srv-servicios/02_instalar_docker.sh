#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 02_instalar_docker.sh
# Version: 2026-06-25
# Finalidad: instalar Docker Engine desde el repositorio oficial.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
DOCKER_USER="${DOCKER_USER:-}"
KEYRING="/etc/apt/keyrings/docker.gpg"
REPO_FILE="/etc/apt/sources.list.d/docker.list"
PACKAGES=(docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin)

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;;
  esac
done

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }
pkg_installed() { dpkg -s "$1" >/dev/null 2>&1; }

require_root

log "Preparando repositorio Docker"
run_cmd install -m 0755 -d /etc/apt/keyrings
if [[ ! -f "$KEYRING" ]]; then
  if "$DRY_RUN"; then
    echo "[DRY-RUN] curl Docker GPG -> $KEYRING"
  else
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o "$KEYRING"
    chmod a+r "$KEYRING"
  fi
else
  log "Clave Docker ya existe"
fi

CODENAME="$(. /etc/os-release && echo "${VERSION_CODENAME}")"
ARCH="$(dpkg --print-architecture)"
REPO_LINE="deb [arch=${ARCH} signed-by=${KEYRING}] https://download.docker.com/linux/ubuntu ${CODENAME} stable"
if [[ ! -f "$REPO_FILE" ]] || ! grep -Fq "$REPO_LINE" "$REPO_FILE"; then
  if "$DRY_RUN"; then
    echo "[DRY-RUN] escribir repositorio Docker en $REPO_FILE"
  else
    echo "$REPO_LINE" > "$REPO_FILE"
  fi
else
  log "Repositorio Docker ya configurado"
fi

run_cmd apt update

missing=()
for pkg in "${PACKAGES[@]}"; do
  pkg_installed "$pkg" || missing+=("$pkg")
done
if [[ "${#missing[@]}" -gt 0 ]]; then
  run_cmd env DEBIAN_FRONTEND=noninteractive apt install -y "${missing[@]}"
else
  log "Docker ya esta instalado"
fi

if [[ -n "$DOCKER_USER" ]]; then
  if id "$DOCKER_USER" >/dev/null 2>&1; then
    if id -nG "$DOCKER_USER" | tr ' ' '\n' | grep -qx docker; then
      log "Usuario $DOCKER_USER ya pertenece a docker"
    else
      run_cmd usermod -aG docker "$DOCKER_USER"
      log "El usuario $DOCKER_USER debera cerrar sesion y volver a entrar"
    fi
  else
    echo "ERROR: DOCKER_USER=$DOCKER_USER no existe" >&2
    exit 1
  fi
fi

log "Validacion"
run_cmd docker version
run_cmd docker compose version
