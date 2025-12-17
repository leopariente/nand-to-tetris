from CommandType import CommandType

class Parser:
    def __init__(self, file_name, code_writer):
        try:
            with open(file_name, 'r') as f:
                self.current_index = 0
                self.lines = [
                    line.split('//')[0].strip()
                    for line in f
                ]
                f.close()
                self.lines = [line for line in self.lines if line] 
                self.current_instruction = self.lines[self.current_index]
                self.code_writer = code_writer

                
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Input file not found at {file_name}")

    def hasMoreLines(self):
        return self.current_index < len(self.lines)

    def advance(self):
        self.current_index += 1
        if self.hasMoreLines():
            self.current_instruction = self.lines[self.current_index]


    def commandType(self):
        if self.current_instruction.startswith(('push', 'pop')):
            if self.current_instruction.startswith('push'):
                return CommandType.PUSH
            else:
                return CommandType.POP
        else:
            return CommandType.ARITHMETIC

    def arg1(self):
        if (self.commandType() == CommandType.ARITHMETIC):
            return self.current_instruction
        else:
            return self.current_instruction.split()[1]

    def arg2(self):
        if self.commandType() in (CommandType.PUSH, CommandType.POP):
            return int(self.current_instruction.split()[2])
        else:
            raise ValueError("arg2() called on a non-push/pop command")