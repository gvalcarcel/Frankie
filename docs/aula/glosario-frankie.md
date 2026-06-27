# Glosario Frankie

## A-D

### Audit

Comando que aplica comprobaciones a las evidencias y muestra resultados como `PASS` o `WARN`.

### Auditoría

Revisión ordenada que compara una situación con unos criterios y conserva las pruebas usadas.

### CLI

Interfaz de línea de comandos. Permite usar un programa escribiendo órdenes en una terminal.

### Comando

Instrucción que damos a un programa. Ejemplo: `python -m frankie status`.

### Diagnóstico

Explicación razonada de un aviso: qué ocurre, qué impacto puede tener y cuál sería el siguiente paso seguro.

### Docker

Tecnología para ejecutar aplicaciones en contenedores aislados y reproducibles.

### Doctor

Comando de Frankie Core que transforma avisos de Audit en explicaciones y recomendaciones pedagógicas. No repara.

## E-L

### Evidencia

Dato o documento que permite justificar una conclusión. Debe tener origen y contexto.

### Frankie

Servidor físico del aula. Ejecuta Proxmox y aloja las máquinas virtuales.

### Frankie Core

Herramienta Python que consulta inventario, estado, auditorías y evidencias del repositorio Frankie.

### Inventory

Comando que muestra los elementos conocidos de la infraestructura y su función.

### JSON

Formato de datos con claves y valores. Es fácil de procesar para otros programas.

### Live Mode

Modo futuro para consultar infraestructura real con acceso controlado. No está implementado.

## M-R

### Proxmox

Plataforma de virtualización instalada en Frankie para gestionar máquinas virtuales y almacenamiento.

### Portainer

Interfaz web para administrar entornos Docker. Su puerto `8000` mantiene un aviso documentado de severidad baja.

### Repair Mode

Modo futuro que podría realizar cambios autorizados. No está implementado y requeriría controles más estrictos.

### Repositorio

Conjunto versionado de código, documentación, pruebas y evidencias. Git conserva su historial.

### Riesgo

Combinación de la posibilidad de que ocurra un problema y el daño que podría causar.

## S-Z

### Samba

Software que permite compartir carpetas entre sistemas Linux y clientes Windows mediante SMB.

### Severidad

Importancia técnica de un hallazgo. No indica necesariamente cuándo actuar.

### SMB

Protocolo de red usado para acceder a carpetas y recursos compartidos.

### Status

Comando que resume el estado conocido de los componentes documentados.

### Urgencia

Indica cuándo conviene atender una incidencia. Severidad y urgencia pueden ser diferentes.

### VM

Máquina virtual. Es un ordenador definido por software que funciona dentro de un host físico.

### Servidor físico

Equipo real con procesador, memoria, discos y red. En este proyecto, el servidor físico es Frankie.
