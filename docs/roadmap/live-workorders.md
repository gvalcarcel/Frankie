# Work Orders LIVE futuras

## Regla común

Estas propuestas no autorizan ni ejecutan acciones. Cada Work Order necesitará confirmación expresa, conectividad verificada, alcance cerrado y revisión de secretos antes de versionar evidencias.

## WO-LIVE-0001 — Captura real de estado Frankie

**Objetivo:** observar el host físico y las dos VMs para comparar su estado con el inventario documentado.

**Acceso necesario:** sesión temporal de solo lectura al host y a cada VM, con perfiles externos al repositorio.

**Comandos de solo lectura:** versión del sistema, hostname saneado, estado de servicios, puertos en escucha, uso general de recursos e inventario de VMs. La lista exacta deberá aprobarse antes de ejecutar.

**Riesgos:** identificar objetivos incorrectos, recoger datos internos o producir una salida demasiado amplia.

**Evidencias a recoger:** fecha, objetivo lógico, versión, servicios observados, diferencias frente al repositorio y declaración de saneamiento.

**Criterio de cierre:** los tres objetivos están identificados, la evidencia está saneada y cada desviación queda documentada sin cambios en servidores.

## WO-LIVE-0002 — Revisión Portainer puerto 8000

**Objetivo:** determinar por qué se publica el puerto `8000`, si se usa y qué dependencia tendría retirarlo.

**Acceso necesario:** solo lectura a `srv-servicios`, Docker y configuración efectiva de Portainer.

**Comandos de solo lectura:** listado e inspección saneada de contenedores, puertos publicados, redes y configuración declarativa. No se recreará ningún contenedor.

**Riesgos:** confundir puerto publicado con puerto permitido, exponer variables de entorno o retirar un servicio necesario sin análisis.

**Evidencias a recoger:** propósito documentado, proceso asociado, exposición observada, reglas de firewall y dependencias conocidas.

**Criterio de cierre:** decisión razonada entre mantener, restringir o planificar retirada. Cualquier cambio se trasladará a otra Work Order con rollback.

## WO-LIVE-0003 — Validación avanzada Samba

**Objetivo:** confirmar permisos efectivos de alumnado y profesorado desde servidor y cliente.

**Acceso necesario:** solo lectura a `srv-recursos` y pruebas supervisadas con cuentas funcionales de aula, sin registrar sus credenciales.

**Comandos de solo lectura:** validación de configuración, consulta de usuarios Samba, grupos, permisos y puertos; pruebas de lectura/escritura únicamente en una carpeta temporal autorizada si una Work Order posterior permite escritura de prueba.

**Riesgos:** exponer nombres internos, alterar material docente o confundir permisos Unix y Samba.

**Evidencias a recoger:** configuración efectiva saneada, matriz de permisos esperados/observados y resultado por recurso compartido.

**Criterio de cierre:** alumnado conserva lectura, profesorado escribe donde corresponde y la carpeta de profesorado permanece restringida, sin modificar datos reales.

## WO-LIVE-0004 — Validación de backups

**Objetivo:** comprobar existencia, antigüedad, tamaño razonable y trazabilidad de backups de servicios y recursos.

**Acceso necesario:** lectura limitada de metadatos en las ubicaciones de backup. No se leerá contenido sensible innecesario.

**Comandos de solo lectura:** listado de ficheros, fechas, tamaños, logs saneados y estado del planificador. No se borrarán backups ni se lanzará una copia.

**Riesgos:** revelar nombres o rutas internas, confundir existencia con restaurabilidad y consumir recursos al inspeccionar archivos grandes.

**Evidencias a recoger:** última ejecución, antigüedad, tamaño, resultado del log y cobertura conocida. Las pruebas de restauración se planificarán aparte.

**Criterio de cierre:** cada backup esperado tiene evidencia reciente o una desviación clasificada; no se afirma restaurabilidad sin prueba.

## WO-LIVE-0005 — Snapshot/backup antes de cambios

**Objetivo:** definir y verificar la protección previa necesaria para una futura intervención con cambios.

**Acceso necesario:** inicialmente solo lectura a Proxmox, almacenamiento y política de backups. Crear un snapshot requerirá autorización adicional de escritura.

**Comandos de solo lectura:** consulta de VMs, almacenamiento disponible, snapshots existentes, backups y fechas. No se creará ni eliminará nada durante la fase de revisión.

**Riesgos:** almacenamiento insuficiente, snapshot inconsistente, falsa sensación de seguridad o ausencia de rollback probado.

**Evidencias a recoger:** cobertura, capacidad, antigüedad, propietario del rollback y prueba de restauración disponible.

**Criterio de cierre:** queda decidido qué protección usar, quién la valida y cómo se revierte. La Work Order de cambio no empieza hasta cumplirlo.

## Orden recomendado

1. Capturar estado general.
2. Revisar el aviso de Portainer.
3. Profundizar en Samba.
4. Validar backups.
5. Aprobar protección antes de cualquier cambio.

Cada intervención termina al completar su propio objetivo. Una Work Order LIVE de lectura nunca se convierte automáticamente en una Work Order de cambio.

## Contrato operativo detallado tras WO-0021

| WO | Agentes | Precondiciones | Consultas de solo lectura | Evidencia esperada | Riesgos | Rollback | Cierre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `WO-LIVE-0001` | LIVE Controller, Hardware Architect, Proxmox, Service, Network, Security, Auditor, Evidence | autorización, tres targets verificados, allowlist, timeout, raw privado | versión, identidad saneada, estado, recursos e inventario VM | timestamp, target lógico, diferencias y saneamiento | target erróneo, exceso de salida | detener sesión y descartar raw inseguro | tres targets contrastados, cero cambios |
| `WO-LIVE-0002` | LIVE Controller, Service, Network, Security, Auditor, Evidence | acceso read-only, alcance Portainer, configuración protegida | contenedores, puertos, redes, firewall y configuración saneada | propósito, exposición y dependencias del puerto `8000` | variables sensibles, confundir observación con retirada | cualquier cambio exige otra WO con backup | decisión mantener, restringir o planificar cambio |
| `WO-LIVE-0003` | LIVE Controller, Service, Network, Security, Auditor, Evidence | cuentas fuera de Git, matriz esperada, cliente supervisado | configuración, usuarios/grupos, permisos y puertos | matriz por recurso y saneamiento | alterar material, exponer usuarios | retirar solo artefacto temporal autorizado | permisos contrastados y recursos intactos |
| `WO-LIVE-0004` | LIVE Controller, Backup Admin, Service, Security, Auditor, Evidence | rutas allowlist, solo metadatos, límites de tiempo | nombres saneados, fechas, tamaños, logs y planificador | cobertura, antigüedad y límites de restaurabilidad | falsa confianza, exposición, carga excesiva | detener consulta; no lanzar ni borrar backups | cobertura y desviaciones documentadas |

Una desviación se documenta; nunca activa Repair Mode ni amplía el alcance automáticamente.
