import re
from datetime import datetime
from typing import Optional
from http import HTTPStatus
from uuid import UUID

from aiohttp import web, web_exceptions
from aiohttp_cache import cache

from news_analyzer.apps.base_handler import BaseHandler, json_response


class Ping(BaseHandler):
    async def get(self):
        return json_response("OK", status=HTTPStatus.OK)


class GetArticleSources(BaseHandler):
    @cache()
    async def get(self) -> web.Response:
        """
        /v1/sources/?[type=<str>]
        Get article sources
        """

        src_type = self.request.query.get("type")
        if src_type:
            articles_sources = await self.db.articles_sources.all_by_type(
                src_type=src_type
            )
        else:
            articles_sources = await self.db.articles_sources.all()

        return json_response([_.dict() for _ in articles_sources], status=HTTPStatus.OK)


class GetArticles(BaseHandler):
    @cache()
    async def get(self, src_id: int) -> web.Response:
        """
        /source/{src_id:<int>}/articles/?[limit=<int>&cursor=<int>]
        Get articles by source name
        """

        articles = await self.db.articles.all_by_src(src_id=src_id)
        return json_response([_.dict() for _ in articles], status=HTTPStatus.OK)


class NamedEntitiesApi(BaseHandler):
    @cache()
    async def get(self, src_id: int) -> web.Response:
        """
        /source/{src_id:<int>}/articles/?[limit=<int>&cursor=<int>]
        Get articles by source name
        """

        articles = await self.db.articles.all_by_src(src_id=src_id)
        return json_response([_.dict() for _ in articles], status=HTTPStatus.OK)


class GetNamedEntitiesTonality(BaseHandler):
    async def get(self) -> web.Response:
        """
        /analyze/entities/all?[src_id=<int>&entity_id=<int>&start_date_ts=<int>&end_date_ts=<int>]
        Get articles by source name
        """

        try:
            src_id = int(self.request.query.get("src_id"))
        except (TypeError, ValueError):
            src_id = None

        try:
            entity_id = int(self.request.query.get("entity_id"))
        except (TypeError, ValueError):
            entity_id = None

        try:
            start_date = datetime.fromtimestamp(
                int(self.request.query.get("start_date_ts"))
            )
        except (TypeError, ValueError):
            start_date = None

        try:
            end_date = datetime.fromtimestamp(
                int(self.request.query.get("end_date_ts"))
            )
        except (TypeError, ValueError):
            end_date = None

        entities = await self.db.named_entities.group_by_name(
            src_id=src_id,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
        )
        return json_response(entities.dict(), status=HTTPStatus.OK)


class GetNamedEntitiesTonalityBySources(BaseHandler):
    async def get(self) -> web.Response:
        """
        /analyze/entities/group_by_sources{entity_id:<int>}?[src_id=<int>&entity_id=<int>&start_date_ts=<int>&end_date_ts=<int>]
        Get articles by source name
        """

        try:
            src_id = int(self.request.query.get("src_id"))
        except (TypeError, ValueError):
            src_id = None

        try:
            entity_id = int(self.request.query.get("entity_id"))
        except (TypeError, ValueError):
            entity_id = None

        try:
            start_date = datetime.fromtimestamp(
                int(self.request.query.get("start_date_ts"))
            )
        except (TypeError, ValueError):
            start_date = None

        try:
            end_date = datetime.fromtimestamp(
                int(self.request.query.get("end_date_ts"))
            )
        except (TypeError, ValueError):
            end_date = None

        entities = await self.db.named_entities.group_by_name_and_src(
            src_id=src_id,
            entity_id=entity_id,
            start_date=start_date,
            end_date=end_date,
        )
        return json_response(entities.dict(), status=HTTPStatus.OK)


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
