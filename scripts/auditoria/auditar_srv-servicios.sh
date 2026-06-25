#!/bin/bash
set -euo pipefail

# Auditoria de solo lectura para srv-servicios.
# No modifica el sistema, no instala nada y no reinicia servicios.

section() { echo; echo "## $*"; }
run_if_exists() {
  local cmd="$1"
  shift
  if command -v "$cmd" >/dev/null 2>&1; then
    "$cmd" "$@"
  else
    echo "NO DISPONIBLE: $cmd"
  fi
}

section "Sistema"
run_if_exists hostnamectl
run_if_exists lsb_release -a || true

section "qemu-guest-agent"
run_if_exists systemctl is-active qemu-guest-agent || true
run_if_exists systemctl status qemu-guest-agent --no-pager || true

section "Docker"
run_if_exists docker --version || true
run_if_exists systemctl is-active docker || true
if command -v docker >/dev/null 2>&1; then
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' || true
  echo
  docker network ls || true
  echo
  docker network inspect aula-network >/dev/null 2>&1 && echo "OK: aula-network existe" || echo "ERROR: aula-network no existe"
fi

section "Contenedores esperados"
if command -v docker >/dev/null 2>&1; then
  for name in portainer postgres n8n; do
    docker ps --format '{{.Names}}' | grep -qx "$name" && echo "OK: $name activo" || echo "AVISO: $name no activo"
  done
fi

section "PostgreSQL no expuesto"
if command -v ss >/dev/null 2>&1; then
  if ss -tlnp | grep -q ':5432'; then
    echo "AVISO: puerto 5432 escucha en el host"
    ss -tlnp | grep ':5432'
  else
    echo "OK: 5432 no escucha en el host"
  fi
else
  echo "NO DISPONIBLE: ss"
fi

section "Puertos abiertos"
run_if_exists ss -tulpn || true

section "UFW"
run_if_exists ufw status verbose || true

section "Fail2ban"
run_if_exists fail2ban-client status sshd || true

section "Backups"
if [[ -d /srv/docker/backups ]]; then
  echo "OK: /srv/docker/backups existe"
  find /srv/docker/backups -maxdepth 2 -type f -printf '%TY-%Tm-%Td %TH:%TM %p\n' 2>/dev/null | sort | tail -20
else
  echo "AVISO: /srv/docker/backups no existe"
fi

section "Cron backup"
crontab -l 2>/dev/null | grep -E '/srv/docker/scripts/backup.sh|backup' || echo "AVISO: no se detecta cron de backup"
