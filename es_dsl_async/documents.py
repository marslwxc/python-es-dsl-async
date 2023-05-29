from abc import abstractmethod, ABC
from elasticsearch_dsl import Document


class Model(Document):

    @classmethod
    async def async_search(cls, **kwargs):
        s = cls.search(**kwargs)
        response = await s.execute_async()
        return response