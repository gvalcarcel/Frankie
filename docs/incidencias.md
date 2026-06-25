# Registro de incidencias

## Formato

```markdown
## INC-XXX - Titulo

### Fecha

### Sintoma

### Evidencia

### Causa

### Solucion aplicada

### Validacion

### Estado
```

## INC-001 - Profesor no podia escribir en ISOs

### Fecha

2026-06-25

### Sintoma

El usuario `profesor` podia leer, pero no escribir en `/srv/recursos/02_ISOS`.

### Evidencia

- Carpeta: `/srv/recursos/02_ISOS`.
- Permisos iniciales: `drwxr-xr-x root:profesorado`.
- `profesor` pertenece a `profesorado`.

### Causa

El grupo `profesorado` no tenia permiso de escritura y Samba no declaraba escritura especifica para `[isos]`.

### Solucion aplicada

Pendiente de trasladar desde el informe operativo.

### Validacion

Pendiente de validación desde cliente SMB real.

### Estado

Resuelta parcialmente.
