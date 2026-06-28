# Frankie OFFLINE Work Order

## WO-XXXX — <Nombre>

## Tipo

```text
Tipo: OFFLINE
Requiere conexión con Frankie: NO
Toca servidores: NO
Riesgo producción: NULO
Tamaño: PEQUEÑA / MEDIA / AMPLIA
```

## Agentes asignados

```text
- docs/agents/software/<agent>.md
- docs/agents/transversal/security-reviewer.md
```

## Objetivo

<Resultado local, documental o de software.>

## Permitido

- leer y modificar el repositorio;
- ejecutar tests locales y herramientas de análisis;
- crear documentación, código y fixtures saneados;
- preparar commit y push si la WO lo autoriza;
- realizar una WO amplia cuando el alcance sea cohesivo y de bajo riesgo.

## Prohibido

- conexión con Frankie;
- SSH;
- Docker real;
- Samba real;
- Proxmox real;
- tocar servidores, VMs o servicios;
- presentar evidencia offline como observación actual.

## Alcance y fuera de alcance

<Lista cerrada de archivos, comportamiento y exclusiones.>

## Validación

```text
<CLI, tests, compileall, enlaces o contratos.>
```

## Seguridad

- Buscar secretos y artefactos temporales.
- Usar placeholders en ejemplos.
- Confirmar ausencia de red, subprocess o escritura runtime cuando proceda.

## Git

```text
Commit: <mensaje exacto o NO>
Push: SÍ / NO
Tag: NO salvo autorización expresa
Release: NO salvo autorización expresa
```

## Criterio de cierre

<Resultado verificable y estado Git esperado.>
