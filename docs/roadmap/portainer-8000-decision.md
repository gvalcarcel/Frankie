# Decisión técnica sobre Portainer 8000

## Contexto

Portainer CE está documentado en VM100 como servicio activo. El puerto principal de acceso es `9443`; el puerto `8000` aparece publicado y escuchando, pero UFW no lo permite explícitamente.

WO-0023 es OFFLINE. Este documento analiza evidencia ya saneada y no afirma el estado actual más allá de la fecha de la captura LIVE.

## Evidencias utilizadas

| Evidencia | Aporte |
| --- | --- |
| `docs/evidencias/structured/portainer_warning.json` | Mantiene `WARNING / LOW`, `resolved=false` y exige revisión LIVE futura. |
| `wo-live-0001/structured_live_summary.json` | Confirma que `8000` estaba publicado y escuchando durante la captura, sin permiso explícito en UFW. |
| `wo-live-0001/vm100_services_sanitized.md` | Documenta `8000` y `9443` publicados por Portainer CE. |
| `wo-live-0001/network_ports_sanitized.md` | Confirma UFW activo, entrada denegada por defecto y ausencia de regla para `8000`. |
| `wo-live-0001/security_baseline_sanitized.md` | Conserva el warning y la separación entre publicación Docker y permiso de firewall. |
| `wo-live-0002/structured_access_removal_summary.json` | Confirma la retirada del acceso temporal; no acredita cambios en Portainer. |

## Estado actual documentado

- Docker/Portainer publicaba `8000` al host durante WO-LIVE-0001.
- El puerto aparecía escuchando en VM100.
- UFW no lo permitía explícitamente y aplicaba denegación de entrada por defecto.
- La captura no modificó servicios.
- WO-LIVE-0002 retiró únicamente el acceso temporal usado para la captura.
- No existe evidencia de que la publicación haya sido retirada, de que el puerto sea necesario o de que esté accesible a través de otras capas de red.

Por tanto, el hallazgo sigue **abierto** como `WARNING / WARN / LOW`.

## Riesgo e impacto

El riesgo documentado permanece `LOW`: existe una superficie publicada adicional, pero el firewall del host no la permite explícitamente. No hay evidencia que justifique elevar la severidad ni cerrar el hallazgo.

El impacto potencial de retirarlo sin conocer su función es interrumpir una capacidad de Portainer. El impacto de mantenerlo sin decisión es conservar configuración innecesaria y depender del firewall para bloquearla.

## Opciones

### Opción A — Mantener 8000 documentado y aceptado

Aplicable si una revisión confirma una dependencia real. Requiere documentar propósito, propietario, alcance de red, controles compensatorios, fecha de revisión y aceptación expresa del riesgo.

### Opción B — Cerrar 8000 en futura WO-LIVE

Aplicable si la revisión confirma que no existe dependencia. La retirada debe realizarse en una WO de cambio separada, con protección previa, copia de la configuración, rollback y validación posterior de Portainer.

### Opción C — Revisar configuración Portainer antes de decidir

Consiste en una intervención LIVE de solo lectura para identificar el mapeo efectivo, su origen declarativo, la finalidad del puerto y posibles dependencias. No permite editar, recrear ni reiniciar contenedores.

## Recomendación

Adoptar primero la **Opción C** mediante `WO-LIVE-0003`. La evidencia disponible prueba la publicación y el bloqueo por UFW, pero no prueba si el puerto se usa ni dónde se declara.

Después de esa revisión:

- elegir la Opción A si existe una necesidad demostrada y el riesgo se acepta formalmente;
- elegir la Opción B si no existe dependencia, mediante una nueva WO-LIVE de cambio;
- mantener el hallazgo abierto si la evidencia continúa siendo insuficiente.

## Próxima Work Order sugerida

`WO-LIVE-0003 — Revisión controlada de Portainer puerto 8000`, definida en [Work Orders LIVE](live-workorders.md).

## Estado de ejecución tras WO-0024

WO-LIVE-0003 quedó bloqueada porque la cuenta autorizada podía entrar por SSH pero no consultar la API de Docker. WO-LIVE-0003A se detuvo antes de crear permisos porque no se podían confirmar todas las precondiciones de seguridad. No se creó `sudoers` adicional y no se ejecutaron consultas con privilegios improvisados.

La recomendación se replantea mediante estas vías, por orden prudente:

1. revisión manual con una cuenta administrativa ya autorizada y allowlist cerrada;
2. revisión presencial supervisada desde la consola de VM100;
3. aplazamiento hasta una ventana técnica con acceso y propietario definidos;
4. snapshot o backup y WO-LIVE de cambio separada únicamente si posteriormente se decide retirar el puerto.

No deben crearse permisos temporales adicionales cuando su alcance mínimo no pueda verificarse de forma inequívoca. Mientras no exista nueva evidencia, el hallazgo permanece `OPEN / WARN / LOW`.

## Criterio para cerrar el hallazgo

El hallazgo solo podrá cerrarse cuando una evidencia LIVE posterior demuestre uno de estos resultados:

1. `8000` ya no está publicado ni escuchando y Portainer continúa operativo; o
2. su mantenimiento ha sido aprobado como excepción documentada, con propósito, alcance, controles y revisión periódica.

Una regla UFW que lo bloquee reduce exposición, pero por sí sola no elimina la desviación de publicación. La ausencia del puerto en documentación offline tampoco constituye evidencia de cierre.
