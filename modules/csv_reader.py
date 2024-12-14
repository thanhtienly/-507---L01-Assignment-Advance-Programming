from io import IOBase
import os

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