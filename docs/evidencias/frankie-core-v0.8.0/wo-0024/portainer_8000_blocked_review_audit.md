# Auditoría de bloqueo de la revisión Portainer 8000

## Identificación

- Work Order: `WO-0024`.
- Fecha: 2026-06-30.
- Tipo: OFFLINE.
- Versión: `0.8.0-dev`.
- Resultado: revisión LIVE bloqueada y replanificada.

## Alcance

Esta Work Order registra los bloqueos de WO-LIVE-0003 y WO-LIVE-0003A, mantiene el hallazgo abierto y define alternativas seguras. No conecta con Frankie, no crea permisos y no modifica Docker, Portainer, UFW o servicios.

## Bloqueos registrados

### WO-LIVE-0003

- La conexión SSH a VM100 funcionó.
- La identidad lógica se contrastó con la divergencia de hostname ya documentada.
- La consulta `docker ps` falló por falta de permiso sobre la API de Docker.
- No se ejecutó `sudo docker`, no se consultó UFW y no se conservaron evidencias parciales.
- El repositorio permaneció limpio.

### WO-LIVE-0003A

- La preparación se detuvo antes de conectar o crear permisos.
- No se confirmó la precondición de seguridad relativa a la credencial expuesta.
- No se creó ni modificó ningún fichero `sudoers`.
- No se aceptó ampliar privilegios de forma improvisada.

## Estado del hallazgo

Portainer `8000` permanece `OPEN / WARN / LOW`. La última evidencia LIVE saneada confirma publicación y escucha, con UFW sin permiso explícito. Los intentos bloqueados no aportan evidencia de cierre ni de un cambio posterior.

## Alternativas seguras

### Opción A — Revisión manual con administrador existente

Una persona autorizada ejecuta la allowlist desde una cuenta administrativa ya establecida. La salida se sanea antes de incorporarla al repositorio. No se crean permisos nuevos.

### Opción B — Revisión presencial desde la consola de VM100

La comprobación se realiza de forma supervisada en el centro, con identidad visual del objetivo y registro manual de resultados saneados.

### Opción C — Posponer hasta una ventana técnica

El warning se conserva hasta disponer de propietario, tiempo, acceso seguro y criterios de parada. Posponer no equivale a resolver.

### Opción D — Protección y cambio controlado futuro

Si se decide retirar el puerto, una WO-LIVE distinta deberá verificar snapshot o backup, configuración declarativa, rollback y validación posterior. Esta opción no autoriza el cambio.

## Recomendación

No crear permisos temporales adicionales si no pueden limitarse y comprobarse de forma inequívoca. Priorizar A o B; usar C si ninguna está disponible. Reservar D únicamente para una decisión de cambio posterior respaldada por evidencia.

## Seguridad

- Sin conexión LIVE durante WO-0024.
- Sin credenciales utilizadas o registradas.
- Sin nuevos permisos.
- Sin salidas brutas.
- Sin direcciones internas, MACs o usuarios reales publicados.
- Sin Repair Mode.

## Validación

- JSON estructurado de WO-0024: válido.
- `python -m frankie version`: OK, `0.8.0-dev`.
- `python -m frankie evidence validate`: OK.
- `python -m frankie evidence summary`: OK.
- `python -m frankie report --json`: JSON válido; Portainer permanece `WARNING / WARN / LOW` y `new_live_connection=false`.
- `python -m frankie doctor --json`: JSON válido; hallazgo Portainer permanece `WARN / LOW`.
- `python -m unittest discover -s tests`: 104 tests, OK.
- `python -m compileall -q frankie`: OK.

## Riesgos y limitaciones

- El estado actual del puerto no ha podido volver a observarse.
- La evidencia LIVE disponible es histórica.
- El firewall documentado reduce exposición, pero no elimina la publicación Docker.
- Una cuenta administrativa existente también requiere control de alcance y saneamiento.

## Decisión final

El bloqueo queda documentado sin debilitar controles de acceso. La revisión se replantea mediante una vía administrativa ya autorizada, una sesión presencial o una ventana técnica controlada.

**Portainer 8000 permanece abierto como WARN / LOW.**
