# Procedimientos operativos

## Comprobar estado de srv-servicios

```bash
docker ps
ufw status verbose
fail2ban-client status sshd
curl -I http://127.0.0.1:5678
```

## Comprobar estado de srv-recursos

```bash
systemctl status smbd --no-pager
testparm -s
ss -tulpn
```

## Ejecutar backup manual de servicios

```bash
sudo /srv/docker/scripts/backup.sh
```

## Validar permisos de ISOs

```bash
sudo -u profesor touch /srv/recursos/02_ISOS/prueba.tmp
sudo -u profesor rm /srv/recursos/02_ISOS/prueba.tmp
sudo -u alumno touch /srv/recursos/02_ISOS/prueba_alumno.tmp
```

El ultimo comando debe fallar.

## Reinicio controlado

1. Avisar a usuarios.
2. Comprobar IPs actuales.
3. Confirmar backups.
4. Reiniciar una VM cada vez.
5. Validar servicios.
6. Documentar IPs nuevas si DHCP cambia.

## Mantenimiento y actualización

El procedimiento completo de mantenimiento, actualización y optimización está documentado en:

- `docs/mantenimiento_servidor.md`

Checklist asociada:

- `checklists/mantenimiento_servidor.md`

Regla operativa: no actualizar ambas VMs a la vez y no ejecutar cambios reales sin snapshot previo.
