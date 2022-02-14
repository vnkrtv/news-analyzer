import logging

from aiomisc.log import basic_config
from aiohttp import web
from aiohttp_cache import setup_cache
from sqlalchemy.ext.asyncio import create_async_engine

from news_analyzer.routes import register_routes
from news_analyzer.middlewares import get_middlewares
from news_analyzer.settings import Config


async def init_db_engine(base_app: web.Application):
    base_app["db_engine"] = create_async_engine(
        f"postgresql+asyncpg://{Config.DB.url}",
        pool_size=Config.DB.pool_size,
        echo=Config.Logging.DB.echo,
        echo_pool=Config.Logging.DB.echo_pool,
        hide_parameters=False,
    )


async def close_db_engine(base_app: web.Application):
    """
    Close all active connections
    """
    await base_app["db_engine"].dispose()


def make_app() -> web.Application:
    basic_config(Config.Logging.level, buffered=False)
    base_app = web.Application(middlewares=get_middlewares())
    setup_cache(
        base_app,
        cache_type=Config.Cache.cache_type,
        backend_config=Config.Cache.backend_config,
    )
    logging.info("setup cache: %s", Config.Cache.cache_type)

    register_routes(base_app)

    base_app.on_startup.append(init_db_engine)
    base_app.on_cleanup.append(close_db_engine)

    return base_app


app = make_app()

if __name__ == "__main__":
    web.run_app(app, host=Config.host, port=Config.port)
