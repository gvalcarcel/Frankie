# Frankie Release Work Order

## WO-XXXX — Release <versión>

## Agentes asignados

```text
- docs/agents/software/release-manager.md
- docs/agents/software/repository-maintainer.md
- docs/agents/software/qa-engineer.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/technical-writer.md
- docs/agents/transversal/system-auditor.md
```

## Objetivo

Preparar o publicar `<versión>` sin mezclar cambios funcionales.

## Gates previos

- working tree limpio;
- versión coherente en código, paquete, tests y docs;
- `CHANGELOG.md` completo;
- notas de release preparadas;
- tests correctos;
- `python -m compileall frankie` correcto;
- revisión de secretos y cachés;
- riesgos conocidos documentados.

## Alcance

```text
Preparación / Tag / GitHub Release / Post-release
```

## Tag

```text
Nombre: vX.Y.Z
Tipo: anotado
Mensaje: <exacto>
Commit objetivo: <hash validado>
```

No mover ni recrear un tag publicado.

## GitHub Release

```text
Título: <exacto>
Notas: <archivo>
Draft: NO
Pre-release: NO salvo decisión explícita
```

## Validación de publicación

- tag remoto apunta al commit correcto;
- release existe y usa ese tag;
- assets fuente disponibles;
- estado Latest verificado si procede.

## Post-release

- crear informe después de publicar;
- indicar que no forma parte del tag;
- commit y push separados;
- no modificar tag o release durante el registro documental.

## Criterio de cierre

<Versión publicada/preparada, evidencia y estado Git final.>
