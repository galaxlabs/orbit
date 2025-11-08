import os, sys, subprocess, pathlib, typer

app = typer.Typer(help="Orbit CLI")

def ensure_django():
    """Prepare sys.path and DJANGO_SETTINGS_MODULE, then django.setup()."""
    root = pathlib.Path(__file__).resolve().parents[2]  # repo root containing manage.py
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.orbit_core.settings")
    # Only setup if not already ready
    from django.apps import apps as _apps
    if not _apps.ready:
        import django
        django.setup()
    return root

@app.command("doctype-generate")
def doctype_generate(name: str):
    root = ensure_django()
    from apps.orbit_core.models import DocType
    from apps.orbit_codegen.generator import generate_model
    dt = DocType.objects.get(name=name)
    generate_model(dt)
    typer.secho(f"Generated: {name}", fg=typer.colors.GREEN)

@app.command("migrate")
def migrate():
    root = ensure_django()
    subprocess.check_call([sys.executable, str(root / "manage.py"), "migrate"])

@app.command("runserver")
def runserver(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Bind host"),
    port: int = typer.Option(8000, "--port", "-p", help="Bind port"),
):
    root = ensure_django()
    bind = f"{host}:{port}"
    subprocess.check_call([sys.executable, str(root / "manage.py"), "runserver", bind])

if __name__ == "__main__":
    app()
