from aiohttp import web
from .handlers import (
    Ping,
    GetArticleSources,
    GetArticles,
    GetNamedEntitiesTonality,
    GetNamedEntitiesTonalityBySources,
)


def register_api_routes(app: web.Application, prefix: str = ""):
    app.router.add_view(prefix + r"/ping", Ping)
    app.router.add_view(prefix + r"/sources", GetArticleSources)
    app.router.add_view(prefix + r"/source/{src_id:\w+}/articles", GetArticles)
    app.router.add_view(prefix + r"/analyze/entities/all", GetNamedEntitiesTonality)
    app.router.add_view(
        prefix + r"/analyze/entities/group_by_sources",
        GetNamedEntitiesTonalityBySources,
    )
