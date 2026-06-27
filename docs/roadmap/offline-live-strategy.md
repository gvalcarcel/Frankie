# Estrategia OFFLINE / LIVE de Frankie

Fecha: 2026-06-27

Estado: propuesta para revisión

## 1. Propósito

Esta estrategia separa el desarrollo local y documental de las operaciones que requieren acceso al servidor físico Frankie o a sus máquinas virtuales.

La separación reduce riesgo, permite avanzar fuera de la red del aula y hace explícito cuándo una tarea puede afectar o consultar infraestructura real.

## 2. Regla predeterminada

Toda Work Order se considera `OFFLINE` salvo que el usuario indique expresamente que existe conexión con Frankie y autorice una Work Order `LIVE`.

La presencia de credenciales históricas, direcciones o scripts en el repositorio no constituye autorización para conectarse.

## 3. Tipos de Work Order

### OFFLINE

Puede:

- leer y modificar el repositorio;
- implementar código que opere sobre fixtures o evidencias locales;
- ejecutar tests locales;
- diseñar arquitectura y seguridad;
- crear documentación, esquemas y ejemplos saneados;
- preparar recolectores sin ejecutarlos contra sistemas reales.

No puede:

- conectarse a Frankie, Proxmox o las VMs;
- usar SSH contra la infraestructura;
- consultar Docker, Samba o systemd remotos;
- modificar configuraciones reales;
- afirmar que una observación local representa el estado live actual.

### LIVE de solo lectura

Requiere autorización expresa y conectividad confirmada.

Puede:

- ejecutar una lista cerrada de comprobaciones de lectura;
- capturar evidencia con timestamp y objetivo;
- comparar estado real con documentación;
- sanear resultados antes de versionarlos.

Debe incluir:

- objetivo concreto;
- sistemas afectados por la consulta;
- comandos permitidos;
- límites de tiempo y alcance;
- política de saneamiento;
- criterios para detenerse;
- evidencia esperada.

### LIVE con cambios

Debe ser excepcional, pequeña y separada de la auditoría de solo lectura.

Requiere:

- autorización explícita para el cambio;
- snapshot o backup cuando sea aplicable;
- comprobaciones previas;
- plan de rollback;
- ventana de mantenimiento;
- pruebas posteriores;
- documentación antes/después.

## 4. Clasificación de riesgo

| Nivel | Ejemplos | Requisitos mínimos |
| --- | --- | --- |
| Nulo | Documentación, planificación y tests con fixtures. | Revisión Git y no incluir secretos. |
| Bajo | Consulta live de estado con comandos aprobados. | Autorización, timeout y saneamiento. |
| Medio | Captura de evidencias amplia o prueba de restauración aislada. | Backup, alcance, supervisión y criterios de parada. |
| Alto | Firewall, red, permisos, contenedores o servicios. | Snapshot, rollback probado, ventana y validación completa. |
| Crítico | Almacenamiento, pérdida de datos, acceso general o cambios irreversibles. | Work Order específica, revisión previa y aprobación reforzada. |

## 5. Ciclo recomendado

```text
OFFLINE: diseñar
    -> OFFLINE: implementar con fixtures
    -> OFFLINE: probar y auditar
    -> LIVE: observar sin cambios
    -> OFFLINE: analizar evidencia saneada
    -> LIVE: cambiar solo si está autorizado
    -> LIVE: validar
    -> OFFLINE: documentar y versionar
```

No todos los trabajos deben llegar a la fase de cambio. Una observación puede concluir que no es necesario actuar.

## 6. Evidencias raw y saneadas

- La evidencia raw se considera privada hasta revisión.
- La evidencia saneada puede versionarse si no contiene secretos ni datos internos no autorizados.
- Deben conservarse fecha, objetivo, método y resultado.
- El saneamiento debe quedar declarado.
- No se debe copiar una evidencia raw a Git por comodidad.
- La ausencia de secretos debe revisarse antes de commit y push.

## 7. Credenciales

- Nunca se almacenan en el repositorio.
- Los perfiles versionados solo contienen identificadores y placeholders.
- Live Mode futuro deberá usar mecanismos externos al repositorio.
- Una Work Order OFFLINE no solicita ni prueba credenciales reales.
- Una autorización LIVE no autoriza acciones fuera del alcance descrito.

## 8. Estrategia pedagógica

La separación OFFLINE/LIVE permite enseñar:

- diferencia entre simulación, evidencia y observación real;
- principio de mínimo privilegio;
- planificación antes de ejecutar;
- importancia de snapshot, backup y rollback;
- trazabilidad de una intervención;
- responsabilidad al trabajar con sistemas compartidos.

Las actividades de aula deben comenzar con fixtures offline. Las prácticas live requieren una guía cerrada, supervisión y un objetivo verificable.

## 9. Aplicación a v0.7.0

`v0.7.0` será OFFLINE y de solo lectura:

- JSON para datos locales;
- evidencias estructuradas de ejemplo;
- Doctor pedagógico;
- documentación de aula;
- diseño de Live Mode.

No incluirá conexiones reales, repair ni cambios sobre Frankie.

Las validaciones live se planificarán en Work Orders separadas cuando el usuario confirme que está en la misma red que Frankie.

## 10. Criterios para detener una Work Order LIVE

Detenerse si:

- el objetivo o la autorización no son claros;
- la IP, hostname o identidad del sistema no coinciden;
- aparece un cambio no previsto;
- faltan snapshot, backup o rollback requeridos;
- una comprobación solicita más privilegios de los previstos;
- la salida contiene secretos que no pueden sanearse con seguridad;
- cambia la conectividad durante la intervención;
- los resultados contradicen la documentación de forma crítica;
- una prueba posterior falla.

## 11. Decisión operativa

```text
OFFLINE por defecto.
LIVE solo con aviso y autorización expresa del usuario.
Cambios live separados de la observación y protegidos por rollback.
```
