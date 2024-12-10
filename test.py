from collections import defaultdict
import re
from modules.csv_reader import CsvReader
from modules.redis import RedisService
import json


class QueryBuilder:
    def __init__(self):
        self.page_size = 20
        self.redisService = RedisService()
        pass

    def set_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    # Function to tokenize and preprocess a document
    def preprocess(self):
        # Initialize the inverted index
        inverted_index = defaultdict(set)

        file = open('sorted_transactions.csv', 'rb')
        csvReader = CsvReader(file)

        line_offset = 0

        while csvReader.is_eof() is False:
            raw_text = csvReader.readline()
            text = raw_text.decode("ascii")
            text = text.lower()
            tokens = re.findall(r'\w+', text)
            tokens = set(tokens)
            for token in tokens:
                inverted_index[token].add(line_offset)

            line_offset += len(raw_text)

        self.redisService.set('index', json.dumps(inverted_index, default=self.set_default))
        return inverted_index

    def tokenizes(self, text):
        text = text.lower()
        tokens = re.findall(r'\w+', text)
        return set(tokens)  # Use a set to remove duplicate tokens

    def query(self, search_term):
        inverted_index = json.loads(self.redisService.get("index"))
        terms = self.tokenizes(search_term)
        # print(terms)
        results = set(line_offset for term in terms for line_offset in inverted_index.get(term, []))
        return results
    
    
    def get_transaction(self, offset_list, page):
        result = list()
        file = open('sorted_transactions.csv', 'rb')
        csvReader = CsvReader(file)

        for i in range(20*(page-1), 20*page):
            offset = offset_list[i]
            csvReader.seek(offset)

            line = csvReader.readline()
            line = line.decode("ascii")
            line = line.split(',', 4)

            result.append(line)

        return result
    
queryBuilder = QueryBuilder()

# queryBuilder.preprocess()

offset_list = queryBuilder.query("Test")

print(len(offset_list))