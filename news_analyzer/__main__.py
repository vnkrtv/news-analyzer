"""
Overriding gunicorn command
"""
import re
import sys

from gunicorn.app.wsgiapp import run

from news_analyzer.settings import Config


def main():
    """
    Запускаем gunicorn на асинхронных воркерах
    """
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])

    sys.argv += ["--bind", "%s:%s" % (Config.host, Config.port)]
    sys.argv += ["--worker-class", "aiohttp.GunicornWebWorker"]
    sys.argv += ["--workers", str(Config.workers_num)]
    sys.argv += ["news_analyzer.app:app"]

    sys.exit(run())
