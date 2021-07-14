from dataclasses import dataclass, asdict
import environs


env = environs.Env()
env.read_env()


@dataclass
class Server:
    host: str = env("SERVER_HOST", 'localhost')
    port: int = env("SERVER_PORT", 8080)


@dataclass
class Redis:
    host: str = env("REDIS_HOST", "localhost")
    port: int = env("REDIS_PORT", 6379)
    db: int = env("REDIS_DB", 0)
    password: str = env("REDIS_PASSWORD", "")


@dataclass
class Settings:
    debug: bool = env.bool("DEBUG", True)

    bot_token: str = env("BOT_TOKEN")
    admin_id: int = env.int("ADMIN_ID", 0)
    check_ip: bool = env.bool("CHECK_IP", False)
    tg_api: str = env("TG_API", "")
    skip_updates: bool = env.bool("SKIP_UPDATES", True)

    recreate_db: bool = env.bool("RECREATE_DB", False)
    echo_db: bool = env.bool("ECHO_DB", False)
    db_url: str = env("DB_URL", "sqlite+aiosqlite:///db.sqlite3")

    wh_on: bool = env.bool("WH_ON", False)
    wh_url: str = env("WH_URL", "")
    wh_path: str = "/" + env("WH_PATH", "webhook")
    is_reload: bool = env.bool("IS_RELOAD", False)

    session_name: str = env("SESSION_NAME", "Session")
    api_id: int = env.int("API_ID", 0)
    api_hash: str = env("API_HASH", "")

    proxy_url: str = env("PROXY_URL", "")
    proxy_login: str = env("PROXY_LOGIN", "")
    proxy_password: str = env("PROXY_PASSWORD", "")

    use_redis: bool = env.bool("USE_REDIS", False)
    redis_url: bool = env("REDIS_URL", "redis://localhost")

    server: Server = Server()


settings = Settings()


# gunicorn
wsgi_app = "app.utils.runner:webhook"
reload = settings.is_reload
if settings.server:
    bind = "{host}:{port}".format(**asdict(settings.server))
worker_class = "aiohttp.GunicornWebWorker"
