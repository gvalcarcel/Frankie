# Frankie CLI

Frankie CLI is a read-only command-line interface for consulting, auditing, and inventorying the Frankie infrastructure repository.

Version target: `v0.6.0 - Frankie CLI Foundation`.

## Commands

```bash
python -m frankie version
python -m frankie status
python -m frankie inventory
python -m frankie audit
python -m frankie help
```

After installation, the equivalent command is:

```bash
frankie status
```

## Safety

This first version is read-only:

- It does not install packages.
- It does not restart services.
- It does not delete files.
- It does not connect to servers by SSH.
- It does not require secrets.
- It only writes output when `--output` is explicitly provided.

## Formats

Supported output formats:

- `text`
- `json`
- `markdown`

Example:

```bash
python -m frankie status --format json
```
