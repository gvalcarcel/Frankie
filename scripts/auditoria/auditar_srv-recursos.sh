#!/bin/bash
set -euo pipefail

# Auditoria de solo lectura para srv-recursos.
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

section "Samba"
run_if_exists systemctl is-active smbd || true
run_if_exists systemctl status smbd --no-pager || true

section "Recursos"
if [[ -d /srv/recursos ]]; then
  echo "OK: /srv/recursos existe"
  if command -v tree >/dev/null 2>&1; then
    tree -L 2 /srv/recursos
  else
    find /srv/recursos -maxdepth 2 -type d | sort
  fi
else
  echo "AVISO: /srv/recursos no existe"
fi

section "Grupos y usuarios"
for group in alumnado profesorado; do
  getent group "$group" || echo "AVISO: falta grupo $group"
done
for user in alumno profesor; do
  id "$user" || echo "AVISO: falta usuario $user"
done

section "Usuarios Samba"
run_if_exists pdbedit -L || true

section "Permisos principales"
for path in /srv/recursos /srv/recursos/02_ISOS /srv/recursos/99_PROFESORADO; do
  if [[ -e "$path" ]]; then
    ls -ld "$path"
  else
    echo "AVISO: falta $path"
  fi
done

section "Configuracion Samba"
run_if_exists testparm -s || true

section "Puertos Samba"
if command -v ss >/dev/null 2>&1; then
  ss -tulpn | grep -E ':(139|445|137|138)\b' || echo "AVISO: no se detectan puertos Samba"
else
  echo "NO DISPONIBLE: ss"
fi

section "UFW"
run_if_exists ufw status verbose || true
