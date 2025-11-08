# Architecture

- `apps/orbit_core`: metadata models (DocType, DocField, DocPerm), settings/wsgi.
- `apps/orbit_api`: dynamic router + schema endpoints; `/` redirects to `/schema`.
- `apps/orbit_codegen`: generate Django model source from DocType.
- `tools/orbit_cli`: Typer-based commands (runserver/migrate/generate).

**Flow:** DocType (metadata) → codegen → Django models + DRF viewsets → OpenAPI schema.
