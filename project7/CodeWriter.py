from CommandType import CommandType

class CodeWriter:
    
    def __init__(self, output_file):
        self.output_file = output_file
        self.file = open(self.output_file, 'w')

    def write_arithmetic(self, command):
        pass

    def write_push_pop(self, commandType, segment, index):
        pass

    def close(self):
        if self.file:
            self.file.close()