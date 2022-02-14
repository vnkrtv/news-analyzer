from aiohttp import web
from .handlers import ArticleSourcesApi, ArticleApi


def register_api_routes(app: web.Application, prefix: str = ""):
    app.router.add_view(prefix + r"/sources", ArticleSourcesApi)
    app.router.add_view(prefix + r"/source/{src_id:\w+}/articles", ArticleApi)
