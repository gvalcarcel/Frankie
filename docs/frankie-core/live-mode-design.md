# Diseño seguro de Live Mode

## Estado del documento

- Versión objetivo: posterior a `v0.7.0`.
- Tipo: diseño OFFLINE.
- Implementación: no disponible.
- Conexiones realizadas para este diseño: ninguna.

## Objetivo

Live Mode permitiría comparar las evidencias versionadas con observaciones actuales de Frankie y sus máquinas virtuales. Su primera versión sería estrictamente de solo lectura.

No debe confundirse con Repair Mode. Observar no autoriza a cambiar.

## Sintaxis propuesta

```bash
python -m frankie live-status --profile <perfil>
python -m frankie live-audit --profile <perfil>
```

Se proponen comandos separados, en lugar de añadir `--live` a los comandos offline. Así la intención es visible, los tests pueden aislar ambos modos y resulta más difícil activar una conexión por accidente.

Estos comandos son solo diseño. Ejecutarlos en `v0.7.0` no inicia Live Mode porque no están implementados.

## Diferencia entre OFFLINE y LIVE

| Aspecto | OFFLINE actual | LIVE futuro |
|---|---|---|
| Fuente | Repositorio y evidencias saneadas | Sistemas reales autorizados |
| Red | No se usa | Necesaria y limitada |
| Credenciales | No se necesitan | Externas al repositorio |
| Riesgo | Nulo para producción | Bajo si solo consulta |
| Resultado | Estado conocido | Observación con fecha |
| Autorización | Work Order OFFLINE | Work Order LIVE expresa |

## Requisitos previos

1. Work Order marcada como `LIVE`.
2. Autorización expresa del propietario.
3. Objetivo, sistemas y duración definidos.
4. Identidad del servidor verificada.
5. Perfil de conexión externo y saneado.
6. Cuenta con mínimo privilegio y sin permisos de cambio.
7. Lista cerrada de comprobaciones aprobada.
8. Timeout, límite de salida y criterios de parada.
9. Ubicación privada para la evidencia raw.
10. Revisión humana antes de publicar evidencia saneada.

## Credenciales

- Nunca se guardan en Git, Markdown, JSON versionado o argumentos visibles.
- No se leen desde plantillas `.env.example`.
- Deben proceder de un almacén externo o de una sesión temporal autorizada.
- El perfil versionado solo puede contener alias y placeholders.
- Frankie Core debe rechazar perfiles con secretos incrustados.
- Los errores nunca deben imprimir contraseñas, claves, tokens o material de autenticación.

## Configuración propuesta

Una configuración versionable describiría únicamente objetivos lógicos:

```yaml
profile: aula-readonly
targets:
  physical: FRANKIE_HOST_PLACEHOLDER
  services_vm: SERVICES_VM_PLACEHOLDER
  resources_vm: RESOURCES_VM_PLACEHOLDER
connection_timeout_seconds: 5
command_timeout_seconds: 10
```

Los valores reales y la autenticación permanecerían fuera del repositorio.

## Confirmaciones necesarias

Antes de conectar, la CLI debería mostrar:

- modo `LIVE READ-ONLY`;
- perfil seleccionado;
- objetivos lógicos;
- comprobaciones previstas;
- ausencia de operaciones de escritura;
- ruta privada de la evidencia raw;
- aviso de que la autorización se limita a esa Work Order.

La ejecución debería requerir una confirmación explícita o una opción no interactiva reservada para automatizaciones previamente aprobadas.

## Comandos permitidos

La implementación futura deberá usar una lista cerrada. Ejemplos de intención permitida:

- consultar versión del sistema;
- leer estado de servicios;
- listar contenedores y redes sin modificarlos;
- comprobar puertos en escucha;
- consultar reglas activas de firewall;
- leer metadatos de permisos y recursos Samba;
- listar fecha, tamaño y nombre saneado de backups;
- consultar configuración efectiva con herramientas de validación en modo lectura.

Cada comando concreto deberá aprobarse en su Work Order LIVE. Esta lista no autoriza su ejecución ahora.

## Comandos prohibidos

- instalación o actualización de paquetes;
- `start`, `stop`, `restart`, `reload` o equivalentes;
- creación, edición, copia o borrado de ficheros remotos;
- cambios de usuarios, grupos, permisos o contraseñas;
- cambios de Docker, Samba, Proxmox, firewall o red;
- acceso a secretos, bases de datos completas o contenido privado;
- comandos encadenados o construidos con texto no validado;
- elevación de privilegios no prevista;
- cualquier comando fuera de la lista cerrada.

## Salida esperada

La consola debe indicar siempre:

```text
Mode: LIVE READ-ONLY
Target: <alias saneado>
Captured at: <fecha con zona horaria>
Result: OK / WARNING / UNKNOWN
Sanitization: pending / completed
```

La salida estructurada debe separar observaciones, errores y metadatos. La evidencia raw se considera privada hasta su saneamiento.

## Errores seguros

Live Mode debe detenerse sin reintentos agresivos cuando:

- no puede verificar la identidad del objetivo;
- falta autorización o configuración;
- la autenticación falla;
- una consulta pide privilegios superiores;
- vence un timeout;
- aparece una salida sensible no prevista;
- un comando no pertenece a la lista permitida;
- se detecta una posible operación de escritura;
- cambia la conectividad o el objetivo durante la captura.

El error debe explicar el motivo sin revelar datos internos ni credenciales.

## Riesgos

| Riesgo | Control propuesto |
|---|---|
| Conectar al sistema equivocado | Verificación de identidad y alias aprobados |
| Exponer datos internos | Evidencia raw privada y saneamiento obligatorio |
| Ejecutar cambios por error | Lista cerrada, cuenta read-only y comandos separados |
| Bloqueo por consultas largas | Timeouts y límites de salida |
| Inyección de comandos | Argumentos tipados y sin shell dinámico |
| Confundir evidencia antigua y actual | Timestamp, origen y modo en cada resultado |
| Ampliar el alcance durante la sesión | Parada y nueva autorización |

## Por qué no se implementa todavía

Faltan decisiones que deben probarse de forma controlada: transporte, perfiles, almacenamiento de credenciales, verificación de identidad, saneamiento y comportamiento ante fallos reales.

`v0.7.0` cierra primero la experiencia offline. Live Mode se dividirá en Work Orders pequeñas y revisables antes de escribir código de conexión.

## Relación con Repair Mode

Repair Mode queda fuera de este diseño. Cualquier capacidad de cambio necesitaría otra arquitectura, confirmaciones reforzadas, snapshot o backup, rollback probado y una Work Order independiente.
