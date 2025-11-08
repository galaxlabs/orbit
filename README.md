# Orbit — Meta-Driven DocType Framework (Django + DRF)

Orbit is a batteries-included meta framework inspired by Frappe/ERPNext, Odoo, etc.
It provides a DocType factory that generates Django models, REST viewsets, and a Desk UI.

## Highlights
- DocType metadata → models, APIs, views
- CLI: `orbit runserver`, `orbit migrate`, `orbit doctype-generate`
- OpenAPI via drf-spectacular (Swagger + ReDoc at `/schema/`)
- Bootstrap script: `bootstrap_orbit.sh` (one-shot workspace creator)

## Quickstart
```bash
cd ~/orbit
source .venv/bin/activate
orbit runserver --host 0.0.0.0 --port 8000
# Swagger: http://<ip>:8000/schema/   Admin: http://<ip>:8000/admin/


cat > README.md <<'MD'
# Orbit — Meta-Driven DocType Framework (Django + DRF)

Orbit is a batteries-included meta framework inspired by Frappe/ERPNext, Odoo, etc.
It provides a DocType factory that generates Django models, REST viewsets, and a Desk UI.

## Highlights
- DocType metadata → models, APIs, views
- CLI: `orbit runserver`, `orbit migrate`, `orbit doctype-generate`
- OpenAPI via drf-spectacular (Swagger + ReDoc at `/schema/`)
- Bootstrap script: `bootstrap_orbit.sh` (one-shot workspace creator)

## Quickstart

```bash
cd ~/orbit
source .venv/bin/activate
orbit runserver --host 0.0.0.0 --port 8000
# Swagger: http://<ip>:8000/schema/   Admin: http://<ip>:8000/admin/
apps/
  orbit_core/        # core models (DocType, DocField, DocPerm), settings/wsgi
  orbit_api/         # dynamic API routing + schema endpoints
  orbit_codegen/     # generator: DocType → model source
tools/
  orbit_cli/         # Typer-based CLI (orbit)
bootstrap_orbit.sh   # one-time initializer



orbit --help
orbit runserver --host 0.0.0.0 --port 8000
orbit migrate
orbit doctype-generate "Customer"

License

MIT © Galaxy Lab


cat > CHANGELOG.md <<'MD'

Changelog
0.0.1 — Bootstrap

Workspace bootstrap script (bootstrap_orbit.sh)

Django 5.2 + DRF + drf-spectacular wiring

DocType/DocField/DocPerm core models

CLI (orbit) with runserver, migrate, doctype-generate

Swagger /schema, ReDoc /schema/redoc


cat > ROADMAP.md <<'MD'

Roadmap

 orbit setup wizard (choose DB: sqlite/postgres/mysql; install redis/celery/nginx/ssl helpers)

 orbit new-site, orbit create-app, orbit add-module, orbit add-doctype UX

 Desk UI generator: orbit gen-ui --frontend [desk|nextjs|react|vue]

 Reporting server + dynamic charts (Stimulsoft-inspired scope per app)

 Per-module AI Agent (task suggestions, auto-workflows)

 Object-level permissions (guardian policies in metadata)

 Multi-tenant + site routing + ops commands (orbit ops dns|ssl|proxy)

 Packaging to PyPI and installable orbit globally


cat > TASKS.md <<'MD'

Tasks / Status
Done

Bootstrap shell: creates venv, installs deps, writes project, migrates.

Fixed drf-spectacular wiring (direct views instead of include("drf_spectacular.urls")).

CLI made Django-aware (lazy django.setup()).

CLI runserver now supports --host/--port.

Root / redirects to /schema/.

Next

Add orbit doctor (check DB, ports, redis, permissions).

Add orbit freeze (emit models/migrations/templates).

Add orbit assets build (Tailwind node-less).

Implement orbit ops (dns/ssl/proxy) scaffolds.

Write generator tests (pytest) and minimal CI.



# 3) Developer guide + contributing
```bash
cat > CONTRIBUTING.md <<'MD'
# Contributing

- Branching: `main` (stable), feature branches as `feat/<short-name>`.
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:` …).
- Python >= 3.12. Use the project venv (`.venv`).
- Run checks before PR:
  - `python -m tools.orbit_cli.main migrate`
  - `python -m tools.orbit_cli.main runserver` (smoke test)
- OpenAPI should render at `/schema`.

## Releasing
1. Bump version in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Tag + push: `git tag vX.Y.Z && git push --tags`.



