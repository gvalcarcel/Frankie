# Puertos y riesgos: el caso Portainer 8000

## Qué es un puerto

Un puerto es un número que ayuda al sistema operativo a entregar una conexión al servicio correcto. Una misma máquina puede ofrecer varios servicios porque cada uno escucha en uno o más puertos.

## Qué significa publicar un puerto

En Docker, publicar un puerto conecta un puerto del contenedor con el host. Esto hace posible dirigir tráfico hacia el servicio, pero no garantiza por sí solo que cualquier equipo pueda alcanzarlo: también influyen el firewall, la red y otros controles.

En la evidencia de Frankie, Portainer publicaba `8000` y `9443`. UFW permitía `9443`, pero no `8000`.

## Por qué un puerto extra no siempre es una emergencia

Un puerto adicional aumenta la superficie que debe revisarse. Sin embargo, su riesgo depende de si es accesible, qué servicio atiende, quién puede llegar hasta él y para qué se usa.

En este caso UFW aplicaba denegación de entrada por defecto y no permitía explícitamente `8000`. Por eso la evidencia clasifica el riesgo como `LOW`, no como una emergencia.

## Qué significa riesgo LOW

`LOW` significa que el posible impacto o la probabilidad documentada son reducidos, pero el hallazgo merece seguimiento. No significa “sin riesgo” ni “resuelto”.

La decisión correcta puede ser mantener el puerto con una justificación, retirarlo con un plan o recoger más evidencia antes de decidir.

## Por qué no se toca un servicio sin plan

Un puerto puede participar en una función que no resulta evidente al mirar una lista. Eliminarlo sin conocer dependencias podría interrumpir Portainer.

Antes de un cambio se necesitan objetivo, autorización, copia de la configuración, protección previa, rollback y comprobaciones posteriores. Una auditoría de solo lectura no debe convertirse sobre la marcha en una reparación.

## Actividad guiada

### Objetivo

Proponer una decisión segura a partir de evidencia incompleta.

### Pasos

1. Ejecuta `python -m frankie doctor`.
2. Localiza `AUD-SERVICES-PORTAINER-001` y anota estado, severidad y recomendación.
3. Ejecuta `python -m frankie report --json`.
4. Localiza `known_state.portainer`, `known_risks` y `recommended_next_steps`.
5. Lee `docs/roadmap/portainer-8000-decision.md`.
6. Explica la diferencia entre “publicado por Docker” y “permitido por UFW”.
7. Elige A, B o C y justifica tu respuesta solo con las evidencias disponibles.
8. Indica qué dato adicional necesitarías antes de cerrar el hallazgo.

### Resultado esperado

La opción prudente con la evidencia actual es revisar primero la configuración en una WO-LIVE controlada. El warning permanece abierto mientras no exista prueba de retirada o aceptación formal.

## Mini rúbrica

| Criterio | 0 puntos | 1 punto | 2 puntos |
| --- | --- | --- | --- |
| Concepto de puerto | No lo explica | Explicación parcial | Relaciona host, contenedor y servicio |
| Docker y UFW | Los confunde | Reconoce que son distintos | Explica publicación y filtrado correctamente |
| Riesgo LOW | Lo interpreta como resuelto | Reconoce seguimiento | Razona impacto, probabilidad y límites |
| Decisión | Propone cambiar sin evidencia | Elige una opción con poca justificación | Elige y justifica con evidencias y límites |
| Seguridad operativa | Omite controles | Menciona algún control | Incluye autorización, backup, rollback y validación |

Puntuación máxima: **10 puntos**.
