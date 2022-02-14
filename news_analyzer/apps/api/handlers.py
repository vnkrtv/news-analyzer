from typing import Optional
from http import HTTPStatus
from uuid import UUID

from aiohttp import web, web_exceptions
from aiohttp_cache import cache

from news_analyzer.apps.base_handler import BaseHandler, json_response


class ArticleSourcesApi(BaseHandler):
    @cache()
    async def get(self) -> web.Response:
        """
        /v1/sources/?[type=<str>]
        Get article sources
        """

        articles_sources = await self.db.articles_sources.all()
        return json_response(
            [_.dict() for _ in articles_sources],
            status=HTTPStatus.OK
        )


class ArticleApi(BaseHandler):
    @cache()
    async def get(self, src_id: int) -> web.Response:
        """
        /source/{src_id:<int>}/articles/?[limit=<int>&cursor=<int>]
        Get articles by source name
        """

        articles = await self.db.articles.all_by_src(src_id=src_id)
        return json_response(
            [_.dict() for _ in articles],
            status=HTTPStatus.OK
        )


#
# class CreateChat(BaseHandler):
#     async def post(self) -> web.Response:
#         """
#         /v1/chats
#         {
#           "chat_name": <str>
#         }
#         Create new chat with name chat_name
#         """
#         chat = await self.get_from_request(ChatCreate)
#         if not chat:
#             raise web_exceptions.HTTPBadRequest(reason=ErrMsg.BAD_PARAMETERS)
#
#         chat.creator_username = self.user["username"]
#         chat_id = await self.db.chats.create(chat)
#
#         chat_info = ChatInfo(chat_id=chat_id)
#         return json_response(chat_info.dict(), status=HTTPStatus.CREATED)
#
#
# class AddUserToChat(BaseHandler):
#     async def post(self, chat_id: str) -> web.Response:
#         """
#         /v1/chats/{chat_id}/users
#         {
#            "user_name": <str>
#         }
#         Add authenticated user to chat(id=chat_id) with ChatUser(chat_username=user_name)
#         """
#         try:
#             chat_id = UUID(chat_id)
#         except (TypeError, ValueError) as e:
#             raise web_exceptions.HTTPNotFound(reason=ErrMsg.CHAT_NOT_FOUND) from e
#
#         chat_user = await self.get_from_request(ChatUserAdd)
#         if not chat_user:
#             raise web_exceptions.HTTPBadRequest(reason=ErrMsg.BAD_PARAMETERS)
#
#         chat = await self.db.chats.get(chat_id=chat_id)
#         if not chat:
#             raise web_exceptions.HTTPNotFound(reason=ErrMsg.CHAT_NOT_FOUND)
#
#         chat_user_id = await self.db.chat_users.create(
#             ChatUser(
#                 chat_id=chat["chat_id"],
#                 username=self.user["username"],
#                 chat_username=chat_user.user_name,
#             )
#         )
#         chat_user_info = ChatUserInfo(user_id=chat_user_id)
#         return json_response(chat_user_info.dict(), status=HTTPStatus.CREATED)