import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def ambiente(nome, padrao=None):
    valor = os.getenv(nome, padrao)
    if valor is None:
        raise ImproperlyConfigured(f"Variável obrigatória ausente: {nome}")
    return valor


def banco_mysql(nome):
    return {
        "ENGINE": "django.db.backends.mysql",
        "NAME": nome,
        "USER": ambiente("DB_USER"),
        "PASSWORD": ambiente("DB_PASSWORD"),
        "HOST": ambiente("DB_HOST", "127.0.0.1"),
        "PORT": ambiente("DB_PORT", "3306"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }


SECRET_KEY = ambiente("DJANGO_SECRET_KEY")
DEBUG = ambiente("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in ambiente("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "alunos",
    "acervo",
    "gestao",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "multimeios.urls"
TEMPLATES = []
WSGI_APPLICATION = "multimeios.wsgi.application"
ASGI_APPLICATION = "multimeios.asgi.application"

DATABASES = {
    "default": banco_mysql(ambiente("DB_LIVROS_NAME", "livros")),
    "usuarios": banco_mysql(ambiente("DB_USUARIOS_NAME", "usuarios")),
    "admin_db": banco_mysql(ambiente("DB_ADMIN_NAME", "admin")),
}

DATABASE_ROUTERS = ["multimeios.db_router.MultimeiosRouter"]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
