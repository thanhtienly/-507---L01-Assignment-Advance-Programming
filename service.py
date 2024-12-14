from modules.query_builder import QueryBuilder
from modules.csv_reader import CsvReader
from modules.redis import RedisService
import json

class AppService:
    def __init__(self) -> None:
        self.redisService = RedisService()
        pass

    def get_transaction_with_query(self, search_term: str = "", page: int = 1):
        redisKey = search_term + ":" + str(page)

        # Check if redis cache has this search term or not, if exist get from redis and return
        found = self.redisService.get(redisKey)
        if found:
            return json.loads(found)
        
        # Empty query params
        if search_term == "":
            return {
                "data": [],
                "page": 1,
                "num_of_transactions": 0
            }
        
        queryBuilder = QueryBuilder()

        inverted_index = json.loads(self.redisService.get("index"))

        offset_list = queryBuilder.query(inverted_index, search_term)

        result = queryBuilder.get_transaction(offset_list, page)

        self.redisService.set(redisKey, json.dumps(result))

        return result