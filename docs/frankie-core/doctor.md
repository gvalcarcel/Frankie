# Frankie Doctor

## Propósito

`python -m frankie doctor` ejecuta el diagnóstico asistido y pedagógico de Frankie Core.

El comando interpreta hallazgos del Audit Engine y los transforma en explicaciones comprensibles, urgencia, impacto y siguientes pasos seguros.

No repara. No cambia configuraciones. No sustituye el criterio del administrador.

## Campos del diagnóstico

Cada incidencia activa incluye:

- `Issue`: identificador del check de auditoría;
- `Title`: nombre breve del problema;
- `Severity`: gravedad técnica documentada;
- `Urgency`: rapidez con la que conviene revisar el problema;
- `Impact`: qué podría ocurrir;
- `Why it matters`: por qué merece atención;
- `Recommended action`: siguiente acción recomendada;
- `Safe next steps`: comprobaciones seguras y ordenadas;
- `Do not`: acciones que no deben improvisarse;
- `Student explanation`: explicación cercana para alumnado;
- `Evidence`: documentos que respaldan el diagnóstico.

Severidad y urgencia no son lo mismo. Una severidad `LOW` puede tener urgencia `LOW`: conviene planificar su revisión, pero no detener una clase ni actuar sin autorización.

## Diferencia entre `status`, `inventory`, `audit` y `doctor`

`status` responde a:

```text
¿Como esta Frankie segun la informacion disponible?
```

`inventory` responde a:

```text
¿Que compone Frankie segun la informacion disponible?
```

`audit` responde a:

```text
¿Que comprobaciones podemos validar, con que evidencias y que hallazgos aparecen?
```

`doctor` responde a:

```text
¿Que significan los hallazgos y que pasos seguros puedo seguir para entenderlos mejor?
```

## En que se apoya

`doctor` reutiliza el Audit Engine de forma programatica. No invoca `python -m frankie audit` como subprocess.

Flujo resumido:

```text
doctor command
-> audit engine
-> doctor engine
-> doctor rules and advice
-> doctor models
-> console renderer
```

## Fuentes usadas

Doctor usa indirectamente las mismas evidencias del Audit Engine porque parte del `AuditReport` generado en memoria.

En esta version se apoya en:

- `docs/evidencias/paso-5-auditorias/`
- `docs/evidencias/frankie-core-v0.6.0/`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- knowledge base del repositorio

Si Audit Engine marca un check como `PASS` gracias a evidencia posterior, Doctor no lo presenta como accion pendiente. Esto ocurre con SMB: historicamente estaba pendiente, pero la evidencia pre-release valida la conexion desde cliente real, por lo que Doctor se centra en el hallazgo activo de Portainer puerto `8000`.

## Que no hace

`doctor` no realiza ninguna de estas acciones:

- No se conecta a Frankie fisico.
- No usa SSH.
- No ejecuta comandos externos.
- No ejecuta scripts Bash.
- No consulta servicios reales.
- No escribe ficheros.
- No borra ficheros.
- No lee `.env`.
- No usa credenciales.
- No accede a Internet.
- No repara nada.

## Por que no repara

El objetivo de Doctor MVP es diagnosticar, no actuar.

Esto es importante por dos motivos:

- un hallazgo tecnico no siempre implica que deba cambiarse algo inmediatamente;
- actuar sin comprender antes el problema puede empeorar la situacion o romper una clase en curso.

## Estados globales de Doctor

- `HEALTHY`
- `ACTIONS_RECOMMENDED`
- `ATTENTION_REQUIRED`
- `INSUFFICIENT_EVIDENCE`
- `CRITICAL`

En el estado actual conocido, el resultado esperable es `ACTIONS_RECOMMENDED`.

## Ejemplo de uso

```bash
python -m frankie doctor
python -m frankie doctor --verbose
```

Salida orientativa:

```text
Frankie Doctor
Version: 0.7.0-dev
Mode: read-only foundation

Scope:
  Source........................ audit engine
  Live connection............... no
  Repairs....................... no
  Writes files.................. no
  Executes commands............. no

Diagnosis summary:
  Audit result.................. WARN
  Issues reviewed............... 1
  Critical issues............... 0
  Safe to continue.............. yes

Findings explained:

Issue: AUD-SERVICES-PORTAINER-001
  Title: Portainer port 8000 remains published
  Severity: LOW
  Urgency: LOW

  Impact:
    Portainer is documented as exposing port 8000 in addition to its main access port.

  Why it matters:
    Published ports increase the surface that should be reviewed.

  Recommended action:
    Review the port exposure in a future explicitly authorized LIVE Work Order.

  Student explanation:
    It is like finding an extra open door in a computer room. It may be intentional, but we should check why it is open before changing it.
```

## Verbose

`--verbose` esta implementado.

Amplia la salida con:

- relacion exacta con el check de auditoria;
- severidad y estado;
- resultado diagnostico;
- razon por la que no se propone reparacion automatica;
- limitaciones si existen.
- disponibilidad de evidencias estructuradas;
- checks resueltos que no requieren acción, como `AUD-SAMBA-001 (PASS; no active action)`.

SMB puede aparecer en esta lista resuelta, pero no como incidencia pendiente.

## Limitaciones del MVP

- No hace diagnostico en vivo.
- No interpreta hardware real.
- No reemplaza pruebas desde cliente Windows.
- No verifica red real ni puertos en tiempo real.
- Depende de evidencias documentadas.
- No sustituye el criterio del administrador.

## Uso pedagogico

Este comando puede usarse en clase para explicar:

- la diferencia entre detectar y entender un problema;
- la diferencia entre diagnosticar y reparar;
- como relacionar evidencia, causa probable e impacto;
- por que conviene proponer pasos seguros antes de tocar una configuracion;
- como documentar razonamientos tecnicos ordenados.

## Proximos pasos

- Añadir salida JSON en una Work Order futura.
- Añadir diagnosticos para mas checks del Audit Engine.
- Añadir modo live seguro y separado si el proyecto lo requiere.
- Conectar Doctor con dashboard o modulo IA sin romper el modo seguro.
