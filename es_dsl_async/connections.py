"""
es数据库连接模块
"""
import contextlib
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl.connections import Connections
from elasticsearch_dsl.serializer import serializer
from six import string_types


class AsyncConnection(Connections):
    """异步elasticsearch-dsl连接模块

    Args:
        Connections (obj): elasticsearch-dsl连接模块
    """

    def __init__(self):
        super().__init__()
        self.session = None
        self.connection = None

    async def create_async_connection(self, alias="default", **kwargs):
        """创建异步连接方法

        Args:
            alias (str, optional): 连接别名. Defaults to "default".

        Returns:
            AsyncElasticsearch: 异步es连接实例
        """
        kwargs.setdefault("serializer", serializer)
        conn = self._conns[alias] = AsyncElasticsearch(**kwargs)
        return conn

    async def get_async_connection(self, alias="default"):
        """获取异步es连接方法

        Args:
            alias (str, optional): 连接别名. Defaults to "default".

        Raises:
            KeyError: 连接未找到

        Returns:
            AsyncElasticsearch: AsyncElasticsearch实例
        """
        if not isinstance(alias, string_types):
            return alias

        with contextlib.suppress(KeyError):
            return self._conns[alias]
        try:
            return await self.create_async_connection(alias, **self._kwargs[alias])
        except KeyError as e:
            raise KeyError(f"There is no connection with alias {alias}.") from e

# TODO: 添加orm 模型注册方法


connections = AsyncConnection()
configure = connections.configure
add_connection = connections.add_connection
remove_connection = connections.remove_connection
create_connection = connections.create_connection
get_connection = connections.get_connection
create_async_connection = connections.create_async_connection
get_async_connection = connections.get_async_connection
