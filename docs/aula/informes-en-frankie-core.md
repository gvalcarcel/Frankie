# Informes en Frankie Core

## Qué es un informe técnico

Un informe técnico reúne datos, resultados y riesgos para que otra persona pueda entender una situación y tomar una decisión.

Frankie Core combina cinco fuentes internas:

- Status resume el estado.
- Inventory explica qué elementos conocemos.
- Audit aplica comprobaciones.
- Doctor explica los avisos.
- Evidence indica qué fichas apoyan la conclusión.

## Markdown y JSON

Markdown está pensado para leer, revisar y publicar documentación.

```bash
python -m frankie report --markdown
```

JSON está pensado para que otro programa identifique los datos por sus claves.

```bash
python -m frankie report --json
```

Los dos formatos usan el mismo informe. Solo cambia la presentación.

## Exportar no es tocar el servidor

Exportar significa guardar una copia del informe dentro de `docs/evidencias/`. Frankie Core sigue leyendo el repositorio local.

No se conecta a Frankie, no reinicia servicios y no repara problemas.

## Actividad guiada

### Objetivo

Leer un informe consolidado y distinguir datos, riesgos y limitaciones.

### Material necesario

Repositorio Frankie, Python y una terminal abierta en la raíz.

### Pasos

1. Ejecuta `python -m frankie report`.
2. Localiza versión, modo y fecha.
3. Busca el estado de SMB.
4. Busca el aviso de Portainer.
5. Localiza una limitación que indique que Frankie no fue consultado.
6. Ejecuta `python -m frankie report --json`.
7. Busca las claves `status`, `audit`, `doctor` y `evidence`.
8. Explica una diferencia entre Markdown y JSON.

### Resultado esperado

- modo `offline`;
- SMB `OK / PASS / INFO`;
- Portainer `WARNING / WARN / LOW`;
- una advertencia clara de que el servidor físico no fue consultado;
- los mismos datos principales en Markdown y JSON.

### Preguntas de repaso

1. ¿Por qué la fecha de generación no demuestra que el servidor se haya consultado hoy?
2. ¿Qué formato resulta más cómodo para una persona?
3. ¿Qué formato resulta más cómodo para otro programa?
4. ¿Exportar un informe cambia Portainer?

### Mini rúbrica

- Localiza los estados y riesgos: 1 punto.
- Distingue Markdown y JSON: 1 punto.
- Explica la diferencia entre informar y tocar un servidor: 1 punto.
