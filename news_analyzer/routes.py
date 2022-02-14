from aiohttp import web

from news_analyzer.apps.api.routes import register_api_routes

# from news_analyzer.apps.auth.routes import register_auth_routes
from news_analyzer.settings import Config


def register_routes(app: web.Application) -> None:
    """
    Тут регистрируем все роуты
    """
    base_path = "/api/v1"
    if Config.api_app in Config.apps:
        register_api_routes(app, prefix=base_path)
    # if Config.auth_app in Config.apps:
    #     register_auth_routes(app, prefix=f"{base_path}/auth")
