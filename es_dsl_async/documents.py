from elasticsearch_dsl
import Document, Keyword, Integer, Text
class BaseModel(Document):
    id = Keyword()
    name = Text()
    age = Integer()

    class Index:
        name = 'my_index'

    async def async_save(self, **kwargs):
        return await super().save(**kwargs)

    async def async_delete(self, **kwargs):
        return await super().delete(**kwargs)

    @classmethod
    async def async_search(cls, **kwargs):
        s = cls.search(**kwargs)
        response = await s.execute_async()
        return response    @classmethod    async def async_get(cls, id):
        return await cls.get(id).execute_async()

    @classmethod
    async def async_count(cls, **kwargs):
        s = cls.search(**kwargs)
        return await s.count_async()
    
class BaseResponse:
    def __init__(self, status, message=None, data=None):
        self.status = status        
        self.message = message        
        self.data = dataclass ErrorResponse(BaseResponse):
    def __init__(self, message):
        super().__init__('error', message=message)

class SuccessResponse(BaseResponse):
    def __init__(self, data):
        super().__init__('success', data=data)

class BaseModel(Document):
    ...

    async def async_save(self, **kwargs):
        try:
            await super().save(**kwargs)
            return SuccessResponse('Document saved successfully.')
        except Exception as e:
            return ErrorResponse(str(e))

    async def async_delete(self, **kwargs):
        try:
            await super().delete(**kwargs)
            return SuccessResponse('Document deleted successfully.')
        except Exception as e:
            return ErrorResponse(str(e))

    @classmethod
    async def async_search(cls, **kwargs):
        try:
            s = cls.search(**kwargs)
            response = await s.execute_async()
            return SuccessResponse(response.to_dict())
        except Exception as e:
            return ErrorResponse(str(e))

    @classmethod    
    async def async_get(cls, id):
        try:
            doc = await cls.get(id).execute_async()
            return SuccessResponse(doc.to_dict())
        except Exception as e:
            return ErrorResponse(str(e))

    @classmethod    
    async def async_count(cls, **kwargs):
        try:
            s = cls.search(**kwargs)
            count = await s.count_async()
            return SuccessResponse(count)
        except Exception as e:
            return ErrorResponse(str(e))
        
    @classmethod
    async def async_search_docs(cls, query, size=10, page=1):
        try:
            s = cls.search().query('multi_match', query=query, fields=['name', 'description'])
            response = await s[(page-1)*size:page*size].execute_async()
            docs = [hit.to_dict() for hit in response.hits]
            total = response.hits.total.value            return SuccessResponse({'docs': docs, 'total': total})
        except Exception as e:
            return ErrorResponse(str(e))
        
    from abc import ABC, abstractmethod
from elasticsearch import AsyncElasticsearch, exceptions as es_exceptions


from abc import ABC, abstractmethod
from elasticsearch import AsyncElasticsearch, exceptions as es_exceptions


class BaseIndex(ABC):
    """
    Base class for Elasticsearch index.
    """

    def __init__(self, client: AsyncElasticsearch, index_name: str):
        self.client = client
        self.index_name = index_name

    @abstractmethod
    async def create_index(self):
        """
        Create Elasticsearch index.
        """
        pass

    @abstractmethod
    async def delete_index(self):
        """
        Delete Elasticsearch index.
        """
        pass

    @abstractmethod
    async def add_document(self, document_id: str, document: dict):
        """
        Add document to Elasticsearch index.
        """
        pass

    @abstractmethod
    async def update_document(self, document_id: str, document: dict):
        """
        Update document in Elasticsearch index.
        """
        pass

    @abstractmethod
    async def delete_document(self, document_id: str):
        """
        Delete document from Elasticsearch index.
        """
        pass

    @abstractmethod
    async def search(self, query: dict):
        """
        Search documents in Elasticsearch index.
        """
        pass


class MyIndex(BaseIndex):
    """
    Example Elasticsearch index.
    """

    async def create_index(self):
        try:
            await self.client.indices.create(index=self.index_name)
        except es_exceptions.RequestError as e:
            print(f"Error creating index {self.index_name}: {e}")
            raise

    async def delete_index(self):
        try:
            await self.client.indices.delete(index=self.index_name)
        except es_exceptions.NotFoundError:
            pass  # Index not found, ignore error
        except es_exceptions.RequestError as e:
            print(f"Error deleting index {self.index_name}: {e}")
            raise

    async def add_document(self, document_id: str, document: dict):
        try:
            await self.client.index(index=self.index_name, id=document_id, body=document)
        except es_exceptions.RequestError as e:
            print(f"Error adding document {document_id} to index {self.index_name}: {e}")
            raise

    async def update_document(self, document_id: str, document: dict):
        try:
            await self.client.update(index=self.index_name, id=document_id, body={"doc": document})
        except es_exceptions.RequestError as e:
            print(f"Error updating document {document_id} in index {self.index_name}: {e}")
            raise

    async def delete_document(self, document_id: str):
        try:
            await self.client.delete(index=self.index_name, id=document_id)
        except es_exceptions.RequestError as e:
            print(f"Error deleting document {document_id} from index {self.index_name}: {e}")
            raise

    async def search(self, query: dict):
        try:
            response = await self.client.search(index=self.index_name, body=query)
            return response["hits"]["hits"]
        except es_exceptions.RequestError as e:
            print(f"Error searching index {self.index_name}: {e}")
            raise

from elasticsearch import AsyncElasticsearch
from my_index import MyIndex

client = AsyncElasticsearch()

my_index = MyIndex(client, "my_index")
await my_index.create_index()

async def search_with_aggregations(self, query: dict, aggregations: dict) -> dict:
    try:
        response = await self.client.search(index=self.index_name, body={"query": query, "aggs": aggregations})
        return response
    except es_exceptions.RequestError as e:
        print(f"Error searching index {self.index_name}: {e}")
        raise


async def search_with_sorting(self, query: dict, sorting: dict) -> List[dict]:
    try:
        response = await self.client.search(index=self.index_name, body={"query": query, "sort": sorting})
        return response["hits"]["hits"]
    except es_exceptions.RequestError as e:
        print(f"Error searching index {self.index_name}: {e}")
        raise

query = {"match": {"content": "python"}}
sorting = {"title": "asc"}
hits = await my_index.search_with_sorting(query, sorting)
for hit in hits:
    print(hit["_source"]["title"])

query = {"match": {"content": "python"}}
aggregations = {"tags": {"terms": {"field": "tags.keyword"}}}
response = await my_index.search_with_aggregations(query, aggregations)
for bucket in response["aggregations"]["tags"]["buckets"]:
    print(bucket["key"], bucket["doc_count"])