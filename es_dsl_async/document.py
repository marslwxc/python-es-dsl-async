from elasticsearch_dsl import Document
from elasticsearch import AsyncElasticsearch


class AsyncDocument(Document):
    class Meta:
        index = 'my_index'
        using = AsyncElasticsearch()

    @classmethod
    async def search_by_title(cls):
        s = cls.search().filter()
        response = await s.execute()
        return response.hits