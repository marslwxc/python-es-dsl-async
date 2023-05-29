from es_dsl_async import AsyncElasticsearchClient


host = '127.0.0.1'
port = '9092'
client = AsyncElasticsearchClient([f"{host}:{port}"])
