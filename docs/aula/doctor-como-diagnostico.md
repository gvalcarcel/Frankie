# Doctor como diagnóstico técnico

## Qué hace Doctor

Doctor ayuda a entender los avisos que encuentra Audit.

Audit dice qué comprobación ha pasado o ha detectado un aviso. Doctor explica qué significa ese aviso y qué pasos seguros podemos dar.

```text
Audit  = detecta y clasifica.
Doctor = explica y orienta.
```

Doctor no repara el servidor. Tampoco ejecuta comandos sobre Frankie.

## Una comparación sencilla

Imagina que se enciende una luz en un coche.

- La luz es el aviso de Audit.
- Doctor explica qué puede significar.
- También indica si puedes continuar, qué revisar y qué no debes tocar todavía.

El mecánico no cambia piezas sin comprobar primero la causa. En servidores hacemos lo mismo.

## Cómo leer un diagnóstico

### Severity

Indica la gravedad técnica del problema.

### Urgency

Indica cuándo conviene revisarlo. No todos los avisos obligan a actuar inmediatamente.

### Impact

Explica qué podría ocurrir si el problema es real o se ignora.

### Why it matters

Explica por qué merece nuestra atención.

### Recommended action

Propone el siguiente paso general. No es una orden automática.

### Safe next steps

Presenta comprobaciones seguras y ordenadas.

### Do not

Recuerda acciones que podrían empeorar el problema o interrumpir servicios.

### Student explanation

Usa un ejemplo cercano para comprender la idea técnica.

## Caso actual: Portainer 8000

Frankie Core documenta que Portainer mantiene publicado el puerto `8000`.

El riesgo conocido es bajo, pero el puerto debe revisarse porque cada acceso publicado debe tener un propósito claro.

Doctor propone comprobarlo en una futura Work Order LIVE de solo lectura. No propone cerrar el puerto, reiniciar Portainer ni cambiar el firewall desde una tarea offline.

SMB no aparece como problema activo porque su validación está documentada como correcta.

## Actividad: Doctor Frankie

Objetivo: aprender a leer un diagnóstico técnico sin tocar el servidor.

1. Ejecuta `python -m frankie doctor`.
2. Localiza el apartado `Issue`.
3. Copia el valor de `Severity`.
4. Copia el valor de `Urgency`.
5. Lee `Student explanation`.
6. Explica con tus palabras qué ocurre.
7. Escribe una acción indicada en `Do not`.
8. Escribe cuál sería el siguiente paso seguro.
9. Ejecuta `python -m frankie doctor --verbose`.
10. Localiza el check de SMB entre los checks resueltos.
11. Ejecuta `python -m frankie doctor --json` y localiza los mismos campos en formato estructurado.

## Evidencia a entregar

- Identificador de la incidencia.
- Severidad y urgencia.
- Explicación del impacto en una frase.
- Una acción segura.
- Una acción que no debe realizarse.
- Confirmación de que SMB está resuelto.

## Preguntas de repaso

1. ¿Qué diferencia hay entre Audit y Doctor?
2. ¿Severity y Urgency significan lo mismo?
3. ¿Por qué no debemos cerrar un puerto sin comprobar su propósito?
4. ¿Por qué hace falta un plan de rollback?
5. ¿Doctor modifica Frankie?
