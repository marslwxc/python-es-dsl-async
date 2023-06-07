from elasticsearch_dsl import Field


class AsyncField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def analyze(self, value):
        # 异步分析方法
        pass

    async def process_search(self, value):
        # 异步处理查询方法
        pass

    async def process_aggs(self, aggs):
        # 异步处理聚合方法
        pass