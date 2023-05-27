"""
与Elasticsearch进行通信的相关类
"""
import typing
from typing import Any, Mapping, Coroutine
import aiohttp
from elasticsearch import AsyncElasticsearch
from elastic_transport import ApiResponse, AsyncTransport

from .utils import TYPE_HOST


class AsyncElasticsearchClient(AsyncElasticsearch):
    """异步es客户端"""

    def __init__(
        self,
        hosts: TYPE_HOST,
        transport_class: typing.Type[AsyncTransport],
        **kwargs
    ) -> None:
        super().__init__(
            hosts=hosts,
            transport_class=transport_class,
            **kwargs
        )

    async def _async_call(
        self,
        method: str,
        url: str,
        params: typing.Any = None,
        body: typing.Any = None,
        headers: typing.Any = None,
        **kwargs
    ) -> typing.Any:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=body,
                headers=headers,
                **kwargs
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def perform_request(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, headers: Mapping[str, str] | None = None, body: Any | None = None) -> Coroutine[Any, Any, ApiResponse[Any]]:
        return await self._async_call(method, path, params=params, headers=headers, body=body)


# TODO: 添加fastapi特化连接