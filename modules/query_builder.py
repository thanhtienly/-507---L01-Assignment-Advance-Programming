from collections import defaultdict
import re
from modules.csv_reader import CsvReader
from modules.redis import RedisService
import os
from dotenv import load_dotenv

load_dotenv()

class QueryBuilder:
    def __init__(self):
        self.page_size = 20
        pass

    def is_search_term_exist(self, search_term):
        return self.redisService.get(search_term)

    def tokenizes(self, text):
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        return set(tokens)  # Use a set to remove duplicate tokens

    def query(self, inverted_index, search_term):
        terms = self.tokenizes(search_term)
        matches = None

        for term in terms:
            if term in inverted_index:
                term_matches = set(inverted_index.get(term, []))
                if matches is None:
                    matches = term_matches
                else:
                    matches &= term_matches
            else:
                matches = set()
                break
        results = list(matches)
        return results
    
    
    def get_transaction(self, offset_list, page = 1):
        result = list()
        file_path = os.environ.get("SOURCE_FILE_PATH")
        file = open(file_path, 'rb')
        csvReader = CsvReader(file)
        skip = 20*(page - 1)
        limit = 0

        if skip >= len(offset_list):
            return {
                "data": [],
                "page": page,
                "num_of_transactions": len(offset_list)
            }
        
        for i in range(skip, len(offset_list)):
            if limit >= self.page_size:
                break
            offset = offset_list[i]
            csvReader.seek(offset)

            line = csvReader.readline()
            line = line.decode("ascii")
            line = line.split(',', 4)

            result.append({
                "date": line[0],
                "transactionId": line[1],
                "credit": line[2],
                "detail": line[4]
            })

            limit += 1

        return {
            "data": result,
            "page": page,
            "num_of_transactions": len(offset_list)
        }