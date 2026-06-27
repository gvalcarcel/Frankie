# Qué es Frankie

## Tres nombres que no debemos confundir

### Frankie

Frankie es el **servidor físico** del aula. Es la máquina real que ejecuta Proxmox y aloja las máquinas virtuales.

### Frankie Core

Frankie Core es una herramienta escrita en Python. Consulta inventario, estados, auditorías y evidencias guardadas en el repositorio.

En `v0.7.0` funciona offline y en modo de solo lectura.

### Repositorio Frankie

Es la carpeta versionada con Git. Contiene código, documentación, pruebas, plantillas y evidencias publicables.

## Una comparación sencilla

Imagina un taller:

- Frankie es el vehículo real.
- El repositorio es su carpeta técnica.
- Frankie Core es la herramienta que ordena y consulta esa carpeta.

Leer la carpeta no es lo mismo que abrir el capó. Por eso Frankie Core indica si sus datos son documentados y no observados en directo.

## Qué hay dentro de Frankie

- VM100, `srv-servicios`: Docker, Portainer, PostgreSQL y n8n.
- VM101, `srv-recursos`: Samba y recursos compartidos del aula.

## Qué puede hacer Frankie Core ahora

- mostrar ayuda y versión;
- resumir el estado conocido;
- presentar el inventario documentado;
- ejecutar una auditoría sobre evidencias locales;
- explicar avisos con Doctor;
- listar, validar y mostrar evidencias estructuradas;
- ofrecer salidas de texto y JSON.

## Qué no puede hacer todavía

- conectarse a Frankie;
- consultar servicios en tiempo real;
- reparar problemas;
- cambiar configuraciones;
- reiniciar o detener servicios.

Estas limitaciones son una medida de seguridad, no un defecto oculto.
