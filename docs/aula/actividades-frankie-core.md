# Actividades Frankie Core

## Antes de empezar

Trabaja desde la raíz del repositorio. Todas las actividades son offline y de solo lectura. No necesitan acceso a Frankie.

La mini rúbrica de cada actividad suma 3 puntos: `1` conseguido, `0,5` parcial y `0` no conseguido.

## Actividad 1: descubrir la ayuda

**Objetivo:** reconocer los comandos disponibles.

**Material necesario:** repositorio Frankie, Python y una terminal.

**Pasos guiados:**

1. Ejecuta `python -m frankie help`.
2. Localiza `status`, `inventory`, `audit`, `doctor` y `evidence`.
3. Anota qué comandos admiten `--json`.
4. Busca las dos frases de seguridad del final.

**Resultado esperado:** una lista correcta de comandos y la confirmación de que funcionan offline.

**Preguntas de repaso:** ¿qué hace `help`? ¿Qué significa offline? ¿Qué comando usarías para ver la versión?

**Mini rúbrica:** identifica los comandos (1); reconoce las opciones JSON (1); explica la garantía offline (1).

## Actividad 2: leer Status

**Objetivo:** interpretar un resumen de estado.

**Material necesario:** terminal y [guía de Status](como-leer-un-status.md).

**Pasos guiados:**

1. Ejecuta `python -m frankie status`.
2. Anota el estado de Frankie, Samba y Portainer.
3. Localiza `Overall status`.
4. Explica por qué un único aviso puede afectar al resultado global.

**Resultado esperado:** Frankie y Samba en `OK`, Portainer en `WARNING` y estado global `WARNING`.

**Preguntas de repaso:** ¿Status es live? ¿Un warning significa caída? ¿Por qué importa la fecha de una evidencia?

**Mini rúbrica:** localiza estados (1); interpreta el resultado global (1); explica el límite offline (1).

## Actividad 3: comparar Status y JSON

**Objetivo:** distinguir una salida para personas de una salida para programas.

**Material necesario:** terminal y [guía JSON](json-en-frankie-core.md).

**Pasos guiados:**

1. Ejecuta `python -m frankie status`.
2. Ejecuta `python -m frankie status --json`.
3. Busca Samba y Portainer en ambas salidas.
4. Localiza `schema_version`, `command` y `overall_status` en JSON.
5. Describe una semejanza y una diferencia.

**Resultado esperado:** los estados coinciden; solo cambia la representación.

**Preguntas de repaso:** ¿JSON modifica datos? ¿Qué es una clave? ¿Por qué un programa prefiere JSON?

**Mini rúbrica:** encuentra las claves (1); comprueba la equivalencia (1); explica la utilidad de JSON (1).

## Actividad 4: leer Audit y Audit JSON

**Objetivo:** interpretar checks, estados, severidades y evidencias.

**Material necesario:** terminal y [guía de auditoría](como-leer-una-auditoria.md).

**Pasos guiados:**

1. Ejecuta `python -m frankie audit`.
2. Localiza los checks de Samba y Portainer.
3. Anota estado y severidad de cada uno.
4. Ejecuta `python -m frankie audit --json`.
5. Comprueba los mismos valores dentro de `checks`.

**Resultado esperado:** Samba `PASS / INFO` y Portainer `WARN / LOW` en ambos formatos.

**Preguntas de repaso:** ¿qué diferencia hay entre `WARN` y `LOW`? ¿Qué justifica un check? ¿Audit repara?

**Mini rúbrica:** localiza checks (1); diferencia estado y severidad (1); relaciona hallazgo y evidencia (1).

## Actividad 5: interpretar Doctor

**Objetivo:** convertir un aviso técnico en un diagnóstico comprensible.

**Material necesario:** terminal y [guía de Doctor](doctor-como-diagnostico.md).

**Pasos guiados:**

1. Ejecuta `python -m frankie doctor`.
2. Localiza severidad, urgencia e impacto.
3. Anota una acción segura y una acción indicada en `Do not`.
4. Ejecuta `python -m frankie doctor --verbose`.
5. Comprueba que SMB aparece como check resuelto, no como problema activo.

**Resultado esperado:** una explicación del aviso de Portainer sin proponer cambios automáticos.

**Preguntas de repaso:** ¿Doctor y Repair son lo mismo? ¿Urgencia y severidad son iguales? ¿Por qué aparece SMB solo como contexto?

**Mini rúbrica:** interpreta el diagnóstico (1); separa acciones seguras y prohibidas (1); reconoce que no hay reparación (1).

## Actividad 6: localizar una evidencia

**Objetivo:** consultar una ficha estructurada y comprobar su validez.

**Material necesario:** terminal y [guía de evidencias](evidencias-estructuradas.md).

**Pasos guiados:**

1. Ejecuta `python -m frankie evidence list`.
2. Ejecuta `python -m frankie evidence validate`.
3. Ejecuta `python -m frankie evidence show samba-validation-current`.
4. Repite el último comando con `--json`.
5. Localiza origen, estado, severidad, referencias y recomendación.

**Resultado esperado:** seis evidencias válidas, ninguna inválida y una ficha SMB `OK / INFO`.

**Preguntas de repaso:** ¿qué demuestra una referencia? ¿Qué ocurre si falta una ficha? ¿Por qué no se guardan secretos?

**Mini rúbrica:** lista y valida (1); interpreta la ficha (1); explica la trazabilidad (1).

## Actividad 7: distinguir los estados

**Objetivo:** no confundir los vocabularios de Status y Audit.

**Material necesario:** salidas de las actividades 2 y 4.

**Pasos guiados:**

1. Crea una tabla con columnas `Componente`, `Status`, `Check` y `Severidad`.
2. Añade Samba y Portainer.
3. Escribe `OK / PASS / INFO` para Samba.
4. Escribe `WARNING / WARN / LOW` para Portainer.
5. Explica con una frase qué representa cada columna.

**Resultado esperado:** una tabla que separa estado general, resultado del check y severidad.

**Preguntas de repaso:** ¿`OK` equivale a `PASS` en todos los contextos? ¿`WARNING` significa `FAIL`? ¿Qué indica `INFO`?

**Mini rúbrica:** completa la tabla (1); usa términos correctos (1); explica sus diferencias (1).

## Actividad 8: planificar antes de tocar

**Objetivo:** comprender por qué una intervención necesita autorización, evidencia y rollback.

**Material necesario:** este documento y la [estrategia OFFLINE/LIVE](../roadmap/offline-live-strategy.md).

**Pasos guiados:**

1. Imagina que alguien propone cerrar el puerto `8000` inmediatamente.
2. Anota qué información falta antes de decidir.
3. Define una comprobación de solo lectura.
4. Indica cuándo haría falta snapshot o backup.
5. Escribe un criterio para detener la intervención.
6. Resume un plan de rollback en dos frases.

**Resultado esperado:** un plan que primero observa, después decide y solo cambia con autorización.

**Preguntas de repaso:** ¿por qué un warning no autoriza un cambio? ¿Qué protege un snapshot? ¿Cuándo debemos detenernos?

**Mini rúbrica:** identifica información previa (1); propone controles (1); incluye parada y rollback (1).
