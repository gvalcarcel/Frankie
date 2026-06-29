# Evidencias LIVE saneadas

## Objetivo

Comprender cómo Frankie Core puede estudiar una observación real sin volver a conectarse al servidor ni publicar información sensible.

## Qué es una evidencia LIVE

Una evidencia LIVE nace de una observación autorizada de una infraestructura real. Puede describir servicios, alertas o una operación controlada. Después de la captura se conserva únicamente una versión preparada para su revisión pública.

## Qué significa sanear

Sanear consiste en retirar datos que no son necesarios para comprender el resultado: direcciones internas, usuarios, MACs, credenciales, claves y salidas brutas. El documento resultante conserva conclusiones y metadatos útiles, pero reduce el riesgo de exposición.

Las salidas brutas no se suben porque pueden revelar más información de la prevista, aunque el comando ejecutado fuera de solo lectura.

## Captura y cambio

Una captura observa y registra. WO-LIVE-0001 fue una captura `live-readonly` y no modificó los servidores.

Un cambio altera un estado concreto. WO-LIVE-0002 fue `live-controlled` porque retiró el acceso temporal utilizado para la captura. Su indicador `changes_made=true` describe únicamente esa retirada, no una modificación de servicios.

El acceso se retiró para aplicar mínimo privilegio: una autorización temporal debe desaparecer cuando termina la tarea que la necesitaba.

## Actividad guiada

1. Ejecuta `python -m frankie evidence validate`.
2. Localiza los recuentos `Live read-only evidences` y `Live controlled evidences`.
3. Ejecuta `python -m frankie evidence summary`.
4. Identifica WO-LIVE-0001 y WO-LIVE-0002 en el bloque `LIVE evidence`.
5. Ejecuta `python -m frankie evidence summary --json` y localiza `live_evidence`.
6. Comprueba que `readonly_captures` vale `1`, `access_cleanup` vale `1` y `temporary_access_removed` es `true`.
7. Explica por qué `server_contacted=true` no significa que este comando se haya conectado ahora.

## Preguntas de reflexión

- ¿Qué información aporta una evidencia saneada frente a una salida bruta?
- ¿Por qué una retirada de acceso cuenta como cambio aunque no altere un servicio?
- ¿Qué dato demuestra que la consulta actual sigue siendo OFFLINE?
- ¿Qué riesgo existiría si una autorización temporal permaneciera activa?

## Resultado esperado

El alumnado distingue observación, cambio controlado y consulta offline; además, comprende por qué la trazabilidad y el saneamiento forman parte de la seguridad.
