import asyncio from elasticsearch.helpers
import bulkfrom elasticsearch_dsl
import Q from models
import BaseModelfrom elasticsearch_async
import AsyncElasticsearchClient

# 创建异步的Elasticsearch客户端
es_client = AsyncElasticsearchClient(['localhost:9200'])

# 创建文
doc = BaseModel(id='1', name='Alice', age=18)
await doc.async_save(using=es_client)

# 异步创建文档
async def async_create_doc():
	doc = BaseModel(id='2', name='Bob', age=20)
	await doc.async_save(using=es_client)

await async_create_doc()

# 批量创建文档
actions = [
    BaseModel(id='3', name='Charlie', age=22).to_dict(True),
    BaseModel(id='4', name='David', age=24).to_dict(True),
]
bulk(es_client, actions)

# 异步批量创建文档
async def async_bulk_create_docs():
	actions = [
		BaseModel(id='5', name='Eve', age=26).to_dict(True),
		BaseModel(id='6', name='Frank', age=28).to_dict(True),
	]
	await bulk(es_client, actions)
	
	await async_bulk_create_docs()

# 搜索文档
query = Q('match', name='Alice')
response = await BaseModel.async_search().query(query).using(es_client)
print(response.hits[0].name)

# 异步搜索文档
async def async_search_docs():
    query = Q('match', name='Bob')
    response = await BaseModel.async_search().query(query).using(es_client)
    return response.hits[0].nameprint(await async_search_docs())

# 获取文档
doc = await BaseModel.async_get('1').using(es_client)
print(doc.name)

# 异步获取文档
async def async_get_doc():
    doc = await BaseModel.async_get('2').using(es_client)
    return doc.nameprint(await async_get_doc())

# 计数文档
count = await BaseModel.async_count().using(es_client)
print(count)

# 异步计数文档
async def async_count_docs():
    count = await BaseModel.async_count().using(es_client)
    return countprint(await async_count_docs())