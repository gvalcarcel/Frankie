# Frankie LIVE Work Order

## WO-LIVE-XXXX — <Nombre>

## Tipo

```text
Tipo: LIVE — SOLO LECTURA / CAMBIO CONTROLADO
Requiere conexión con Frankie: SÍ
Toca servidores: CONSULTA / SÍ
Riesgo producción: BAJO / MEDIO / ALTO
Tamaño: PEQUEÑA
```

## Agentes asignados

```text
- docs/agents/hardware/live-operations-controller.md
- docs/agents/hardware/<specialist>.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/system-auditor.md
- docs/agents/transversal/technical-writer.md
```

## Objetivo y targets

<Un objetivo concreto y sistemas identificados mediante alias seguros.>

## Autorización

- Confirmación expresa del usuario: PENDIENTE / RECIBIDA.
- Ventana y duración: <valor>.
- Nivel de privilegio: <mínimo necesario>.

## Comandos permitidos

```text
<Lista cerrada y exacta.>
```

## Comandos prohibidos

```text
<Restart, delete, write, firewall, package changes y cualquier comando fuera de allowlist.>
```

## Evidencias antes y después

- identidad y estado inicial;
- timestamp y objetivo;
- salida raw privada;
- evidencia saneada publicable;
- estado posterior y diferencias.

## Backup / snapshot

```text
Requerido: SÍ / NO
Evidencia: <ruta o referencia>
```

## Rollback

<Pasos exactos, responsable y criterio de activación.>

## Criterios de parada

- identidad o alcance no coinciden;
- aparece un cambio no previsto;
- faltan backup, snapshot o rollback;
- se requieren privilegios superiores;
- la salida contiene datos sensibles inesperados;
- falla una validación.

## Regla operativa

No improvisar. No ampliar alcance. No realizar cambios sin confirmación expresa. Una auditoría no se convierte en reparación.

## Criterio de cierre

<Evidencia esperada, estado final y decisión.>
