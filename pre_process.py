from modules.csv_reader import CsvReader
import json
import pandas as pd

def sort_raw_file(file_path):
    # TODO 
    data = pd.read_csv(file_path)
    data = data.sort_values(by=["credit"])
    
    data.to_csv("sorted_transactions.csv", encoding='utf-8', index = False, header= False)
    # Read the "chuyen_khoan.csv" file, then sort this file by "credit" column
    # Write the result to the new file with name "sorted_transactions.csv" without header row.
    pass

if __name__ == "__main__":
    file_path = './chuyen_khoan.csv'
    sort_raw_file(file_path)

    file = open('sorted_transactions.csv', 'rb')
    csvReader = CsvReader(file)
    indexes = csvReader.index()

    with open('index.json', 'w') as file:
        json.dump(indexes, file)
