from elasticsearch_dsl import Document


class AsyncDocument(Document):

    @classmethod
    async def async_search(cls, **kwargs):
        return await cls.search(**kwargs)
