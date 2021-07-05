from urllib.parse import urlparse

from dynaconf import Dynaconf, Validator


settings = Dynaconf(
    envvar_prefix=False,
    environments=True,
    settings_files=["settings.toml", ".secrets.toml", "settings.local.toml"],
    validators=[
        Validator("bot_token", must_exist=True),
        Validator("check_ip",
                  "debug",
                  "is_reload",
                  "skip_updates",
                  "wh_on",
                  "recreate_db",
                  "echo_db",
                  default=False),
        Validator("admins", default=[]),
        Validator(
            "wh_url",
            "db_url",
            "proxy",
            "proxy_auth.login",
            "proxy_auth.password",
            "api_id",
            "api_hash",
            default=""),
        Validator("tg_api", default="https://api.telegram.org"),
        Validator("server", "redis", "polling", default={}),
        Validator("path", default=lambda s, v: urlparse(s.wh_url).path or "/"),
    ]
)

# gunicorn
wsgi_app = "app.utils.runner:webhook"
reload = settings.is_reload
if settings.server:
    bind = "{host}:{port}".format(**settings.server)
worker_class = "aiohttp.GunicornWebWorker"
