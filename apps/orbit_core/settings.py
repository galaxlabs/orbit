import os, pathlib
import dj_database_url

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

# optional cfg.yaml
_cfg = {}
try:
    import yaml
    fp = BASE_DIR / "cfg.yaml"
    if fp.exists():
        _cfg = yaml.safe_load(fp.read_text()) or {}
except Exception:
    _cfg = {}

SECRET_KEY = os.environ.get("SECRET_KEY") or _cfg.get("secret_key") or "dev-secret"
DEBUG = (os.environ.get("DJANGO_DEBUG","1") == "1") if os.environ.get("DJANGO_DEBUG") else bool(int(_cfg.get("debug", 1)))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS","").split(",") if os.environ.get("ALLOWED_HOSTS") else _cfg.get("allowed_hosts", ["*"])

INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","drf_spectacular","django_filters","guardian",
    "apps.orbit_core","apps.orbit_api",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apps.orbit_api.urls"
TEMPLATES = [{
  "BACKEND":"django.template.backends.django.DjangoTemplates",
  "DIRS":[BASE_DIR / "apps" / "orbit_core" / "templates"],
  "APP_DIRS":True,
  "OPTIONS":{"context_processors":[
      "django.template.context_processors.debug",
      "django.template.context_processors.request",
      "django.contrib.auth.context_processors.auth",
      "django.contrib.messages.context_processors.messages",
  ]},
}]
WSGI_APPLICATION = "apps.orbit_core.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL") or _cfg.get("database_url") or f"sqlite:///{BASE_DIR}/orbit.sqlite3"
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}

# MySQL/PyMySQL shim
if DATABASE_URL.startswith(("mysql://","mariadb://")):
    try:
        import MySQLdb  # mysqlclient
    except Exception:
        try:
            import pymysql
            pymysql.install_as_MySQLdb()
        except Exception:
            pass

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "static")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
  "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
  "DEFAULT_FILTER_BACKENDS": [
      "django_filters.rest_framework.DjangoFilterBackend",
      "rest_framework.filters.SearchFilter",
      "rest_framework.filters.OrderingFilter",
  ],
  "DEFAULT_AUTHENTICATION_CLASSES":[
      "rest_framework.authentication.SessionAuthentication",
      "rest_framework.authentication.BasicAuthentication",
  ],
  "DEFAULT_PERMISSION_CLASSES":[
      "rest_framework.permissions.IsAuthenticated",
  ]
}
SPECTACULAR_SETTINGS = {"TITLE":"Orbit API","VERSION":"0.0.1"}

ANONYMOUS_USER_NAME = "orbit-anon"
