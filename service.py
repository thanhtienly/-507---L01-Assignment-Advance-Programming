from modules.query_builder import QueryBuilder
from modules.transaction import Transaction
from modules.csv_reader import CsvReader
from modules.redis import RedisService
import json

class AppService:
    def __init__(self) -> None:
        self.redisService = RedisService()
        pass

    def get_transaction_with_query(self, amount: str = "", message : str = "", next_cursor: str = ""):
        redisKey = ":".join([amount, message.lower(), next_cursor])

        # Check if redis cache has this search term or not, if exist get from redis and return
        found = self.redisService.get(redisKey)
        if found:
            return json.loads(found)
        
        # Don't have any more transaction
        if next_cursor == "null":
            return {
                "data": [],
                "next_cursor": "null"
            }
        
        # Check is next_cursor valid
        try:
            next_cursor = int(next_cursor)
        except:
            return {"Error": "Next cursor invalid type"}
        
        # Empty query params
        if amount == "" and message == "":
            return {
                "data": [],
                "next_cursor": "null"
            }
        
        queryBuilder = QueryBuilder(next_cursor, amount, message)


        # get start_offset, end_offset from QueryBuilder, then csvReader use this offset to read the CSV file
        # offset = {
        #   start_offset: value_1,
        #   end_offset: value_2    
        # }

        offset = queryBuilder.get_offset()


        # Next cursor's value negative
        if offset["start_offset"] == None and offset["end_offset"] == None:
            return {
                "data": [],
                "next_cursor": "null"
            }
        

        start_offset = offset["start_offset"]
        end_offset = offset["end_offset"]


        # csvReader use the offset above to jump to specific position, then read transaction line by line
        # Use QueryBuilder to check each transaction line, 
        # If transaction detail match the search term, then insert transaction into transaction table
        file = open('sorted_transactions.csv', 'rb')
        csvReader = CsvReader(file)

        # Jump to start position
        csvReader.seek(start_offset)
        current_offset = csvReader.tell()

        # Stop only end of file or out of searching range
        while csvReader.is_eof() is False and current_offset <= end_offset:
            line = csvReader.readline()
            transaction = Transaction(line)
            transaction_detail = transaction.get_message()

            if queryBuilder.validate_message(transaction_detail):
                queryBuilder.insert_transaction(transaction)

            # update current offset
            current_offset += transaction.get_raw_transaction_length()

            # update next cursor
            queryBuilder.set_next_cursor(current_offset)
            
            if queryBuilder.is_transaction_table_full() is True: 
                break
        
        result = queryBuilder.get_result()

        # Update Redis cache with search temp response
        self.redisService.set(redisKey, json.dumps(result))
        return result