from modules.csv_reader import CsvReader
from collections import defaultdict
import json
import re 
import os
from dotenv import load_dotenv

load_dotenv()

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def preprocess():
    # Initialize the inverted index
    inverted_index = defaultdict(set)
    file_path = os.environ.get("SOURCE_FILE_PATH")
    file = open(file_path, 'rb')
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

    index_file_path = os.environ.get("INDEX_FILE_PATH")
    with open(index_file_path, 'w') as file:
        json.dump(inverted_index, file, default=set_default)

    return inverted_index

if __name__ == "__main__":
    preprocess()