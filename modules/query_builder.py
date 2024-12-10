from modules.transaction import Transaction, TransactionTable
import json
import re

class QueryBuilder:
    file = open('./index.json', 'r')
    indexes = json.load(file)

    def __init__(self, next_cursor: int = 0, amount: str = "", message: str = "") -> None:
        self.next_cursor = next_cursor
        self.amount = amount
        self.message = message
        self.transaction_table = TransactionTable()
        self.start_offset = None
        self.end_offset = None

        self.set_offset()

    # This function use to calculate start_offset, end_offset depend on amount and message store in self.amount, self.message
    # start_offset: offset of 1st transaction line that contain amount
    # end_offset: offset of last transaction line that contain amount
    # If amount's not provided (or amount == "") then start_offset = 0 & end_offset = last_line_offset
    # index file have been loaded as indexes variable, you can use this variable as dictionary.
    def set_offset(self):
        # Next cursor's value negative
        if self.next_cursor < 0:
            self.start_offset = None
            self.end_offset = None
            return

        # Fetch from next cursor to end of file
        if self.amount == "":
            self.start_offset = self.next_cursor
            self.end_offset = int(self.indexes["last_line_offset"])
            return 

        # amount != "" but not found in index file -> return empty data
        if self.indexes.get(self.amount) is None:
            self.start_offset = None
            self.end_offset = None
            return

        # Next cursor < position to start searching -> update next cursor
        if self.next_cursor <= self.indexes[self.amount][0]:
            self.start_offset = self.indexes[self.amount][0]
            self.next_cursor = self.start_offset
            self.end_offset = self.indexes[self.amount][1]
            return
        
        # Next cursor > position to start searching -> return empty data
        if self.next_cursor > self.indexes[self.amount][1]:
            self.start_offset = None
            self.end_offset = None
            return
        
        # Start searching from next cursor to last line transaction with amount
        self.start_offset = self.next_cursor
        self.end_offset = self.indexes[self.amount][1]

    
    def get_offset(self):
        return {
            "start_offset": self.start_offset,
            "end_offset": self.end_offset
        }
    
    # Check if next_cursor >= self.next_cursor, if not, pass else update self.next_cursor by argument next_cursor
    # This function call each time new line is read to update offset of current transaction line
    def set_next_cursor(self, next_cursor: int):
        # Only update next cursor if it increases
        if next_cursor > self.next_cursor:
            self.next_cursor = next_cursor

        # next cursor out of file offset
        if self.next_cursor > self.end_offset:
            self.next_cursor = "null"
            return

        # Next cursor = last line offset (empty line) -> next cursor = null
        if self.next_cursor == self.indexes['last_line_offset']:
            self.next_cursor = 'null'
            
        return

    # Get next_cursor for paging
    # This function call when Transaction Table is full or use to get next_cursor when needed
    def get_next_cursor(self):
        return self.get_next_cursor
    

    # Check if transaction detail contains message or not 
    def validate_message(self, transaction_message):
        if self.message == "":
            return True
        if re.search(self.message, transaction_message, re.IGNORECASE) is not None:
            return True
        return False
    
    # Check if transaction_table is full or not
    def is_transaction_table_full(self):
        return self.transaction_table.get_is_full_status()

    # Insert transaction match the search term to the transaction_table
    def insert_transaction(self, transaction: Transaction):
        self.transaction_table.insert_transaction(transaction)  

    def get_result(self):
        return {
            "data": self.transaction_table.to_JSON(),
            "next_cursor": self.next_cursor
        }