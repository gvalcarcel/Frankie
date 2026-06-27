# JSON en Frankie Core

## Qué es JSON

JSON es una forma de guardar o transmitir datos usando etiquetas y valores.

Puede imaginarse como una ficha ordenada:

```text
nombre: Portainer
estado: WARNING
severidad: LOW
```

En JSON, esa ficha se escribe así:

```json
{
  "name": "Portainer",
  "status": "WARNING",
  "severity": "LOW"
}
```

## Personas y programas

La salida normal de Frankie Core está preparada para que la lea una persona:

```bash
python -m frankie status
```

La salida JSON está preparada para que otro programa pueda identificar cada dato sin tener que adivinar dónde aparece:

```bash
python -m frankie status --json
```

Los dos modos usan el mismo informe. Solo cambia la forma de presentarlo.

## De informe a ficha estructurada

Antes, Frankie Core consultaba principalmente informes escritos en Markdown. Ahora también puede cargar fichas JSON que un programa entiende campo por campo.

```text
Antes: leemos un informe escrito.
Ahora: también tenemos fichas JSON que puede leer Frankie Core.
```

Las fichas no borran los informes. Los complementan y apuntan a ellos mediante `references`.

## Status en JSON

```bash
python -m frankie status --json
```

Busca estas etiquetas:

- `schema_version`: versión del formato de datos;
- `command`: comando que produjo la salida;
- `overall_status`: estado global;
- `components`: lista de elementos revisados.

Samba debe aparecer como `OK` y Portainer como `WARNING` según las evidencias actuales.

## Audit en JSON

```bash
python -m frankie audit --json
```

Busca:

- `overall_result`: resultado global;
- `counts`: número de checks por estado;
- `checks`: comprobaciones y evidencias.

Para obtener más explicación sin abandonar JSON:

```bash
python -m frankie audit --verbose --json
```

## Mini actividad

1. Ejecuta `python -m frankie status`.
2. Ejecuta `python -m frankie status --json`.
3. Localiza Samba y Portainer en ambas salidas.
4. Explica qué datos son iguales y qué cambia en la presentación.
5. Repite la comparación con `audit`.

Evidencia a entregar:

- una tabla con el estado de Samba y Portainer;
- el nombre de tres etiquetas JSON;
- una frase que explique por qué JSON resulta útil para otro programa.

## Preguntas de repaso

1. ¿JSON cambia el estado real de Frankie?
2. ¿Qué diferencia hay entre `WARNING` y `LOW`?
3. ¿Por qué no conviene construir JSON analizando texto de consola?
4. ¿Qué significa que Frankie Core funcione en modo offline?
5. ¿Qué programa futuro podría aprovechar estos datos?

## Actividad con una evidencia

1. Abre `docs/evidencias/structured/samba_validation.json`.
2. Localiza `component.name`.
3. Localiza `status` y `severity`.
4. Localiza `recommendation`.
5. Explica con tus palabras por qué la ficha está `OK`.
6. Repite el ejercicio con `portainer_warning.json` y explica por qué está en `WARNING`.

## Seguridad

Estos comandos no se conectan al servidor físico Frankie, no ejecutan comandos externos y no necesitan contraseñas. Los resultados proceden de evidencias documentadas en el repositorio.
