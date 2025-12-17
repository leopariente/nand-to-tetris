from Parser import Parser
from CodeWriter import CodeWriter
from CommandType import CommandType

class VMTranslator:
    
    def __init__(self, file_name):
        self.code_writer = CodeWriter(file_name.replace('.vm', '.asm'))
        self.parser = Parser(file_name, self.code_writer)

    def translate(self):
        while self.parser.hasMoreLines():
            command_type = self.parser.commandType()
            if command_type == CommandType.ARITHMETIC:
                self.code_writer.write_arithmetic(self.parser.arg1())
            elif command_type in (CommandType.PUSH, CommandType.POP):
                self.code_writer.write_push_pop(command_type, self.parser.arg1(), self.parser.arg2())
            self.parser.advance()
        self.code_writer.close()