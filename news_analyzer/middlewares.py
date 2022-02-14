import logging
from http import HTTPStatus
from typing import List, Callable

from aiohttp import web, web_exceptions

from news_analyzer.apps.base_handler import error_response, ErrMsg
# from news_analyzer.apps.auth.middlewares import auth_middleware


def get_middlewares() -> List[Callable]:
    """
    Тут регистрируем все миддлваеры
    :return: список миддлваеров
    """
    return [
        exception_middleware,
        # auth_middleware,
    ]


@web.middleware
async def exception_middleware(request: web.Request, handler: Callable) -> web.Response:
    try:
        response = await handler(request)

    except web_exceptions.HTTPUnprocessableEntity:
        err_msg = ErrMsg.BAD_PARAMETERS
        response = error_response(
            message=err_msg,
            status=HTTPStatus.BAD_REQUEST,
        )

    except web.HTTPError as e:
        err_msg = e.reason
        response = error_response(
            message=err_msg,
            status=e.status,
        )
    #
    # except Exception as e:
    #     err_msg = str(e)
    #     response = error_response()

    finally:
        if response.status < 400:
            logging.info(
                "%s %s %s %s",
                request.method,
                request.path,
                response.status,
                request.remote,
            )
        else:
            logging.error(
                "%s %s %s %s %s",
                request.method,
                request.path,
                response.status,
                request.remote,
                err_msg,
            )

    return response
