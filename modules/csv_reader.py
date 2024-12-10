from io import IOBase
import os
from modules.transaction import Transaction

class CsvReader:
    def __init__(self, file_stream: IOBase) -> None:
        self.file_stream = file_stream

    # Method to check that current position of file stream is end of file or not
    def is_eof(self):
        current_position = self.file_stream.tell()    # save current position
        self.file_stream.seek(0, os.SEEK_END)
        
        end_position = self.file_stream.tell()    # find the size of file
        self.file_stream.seek(current_position, os.SEEK_SET)
        return current_position == end_position

    # Function to create an index for CSV file with index by amount
    # Index of CSV file is a dictionary with this format 
    # {
    #   "1st credit (value of credit column)": [offset of 1st line contain this credit, offset of last line contain this credit],
    #   "2nd credit": [offset of 1st line contain this credit, offset of last line contain this credit]
    #
    #   "last_line_offset": offset to the beginning of the last line in CSV file
    # }
    # You can use self.file_stream to get the current offset of file stream
    def index(self):
        indexes = dict()
        line_offset = 0
        prev_offset = 0
        prev_credit = -1

        while self.is_eof() is False:
            line = self.readline()
            transaction = Transaction(line)
            transaction_credit = transaction.to_JSON()["credit"]

            # Add last line offset 
            if prev_credit != transaction_credit and prev_credit != -1:
                indexes[prev_credit].append(prev_offset)
            if indexes.get(transaction_credit) is None:
                indexes[transaction_credit] = [line_offset]

            prev_credit = transaction_credit
            prev_offset = line_offset
            line_offset = self.file_stream.tell()

        
        indexes[prev_credit].append(line_offset)
        # Add offset of last line of file
        indexes["last_line_offset"] = line_offset
        return indexes

    # Get current file stream offset
    def tell(self):
        return self.file_stream.tell()
    
    # Jump to specific offset
    def seek(self, offset: int = 0):
        if offset == 0:
            self.file_stream.seek(offset)
        else:
            self.file_stream.seek(offset - 1)
            self.readline()

    # Read 1 line from file_stream
    def readline(self):
        line = self.file_stream.readline()
        return line
    
    # Read multiple lines from file_stream
    def readlines(self):
        lineList = []
        while self.is_eof() is False:
            line = self.readline()
            lineList.append(line)
        return lineList#