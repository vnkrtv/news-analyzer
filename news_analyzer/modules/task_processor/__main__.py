import asyncio
import logging
import time

from aiomisc.log import basic_config

from news_analyzer.settings import Config
from news_analyzer.modules.task_processor.task_producer import run_task_producer


def main():
    basic_config(Config.Logging.level, buffered=True)
    while True:
        try:
            asyncio.run(run_task_producer())
        except Exception as e:
            # Wait for db
            logging.error("error on running task processor: %s", e)
            time.sleep(5)
