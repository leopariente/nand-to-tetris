from CommandType import CommandType

class Parser:
    def __init__(self, file_name):
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

                
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Input file not found at {file_name}")

    def hasMoreLines(self):
        return self.current_index < len(self.lines)

    def advance(self):
        self.current_index += 1
        if self.hasMoreLines():
            self.current_instruction = self.lines[self.current_index]


    def commandType(self):
        cmd = self.current_instruction.split()[0]
        if cmd == 'push':
            return CommandType.PUSH
        elif cmd == 'pop':
            return CommandType.POP
        elif cmd == 'label':
            return CommandType.LABEL
        elif cmd == 'goto':
            return CommandType.GOTO
        elif cmd == 'if-goto':
            return CommandType.IF
        elif cmd == 'function':
            return CommandType.FUNCTION
        elif cmd == 'return':
            return CommandType.RETURN
        elif cmd == 'call':
            return CommandType.CALL
        else:
            return CommandType.ARITHMETIC

    def arg1(self):
        if self.commandType() == CommandType.RETURN:
            return None
        if (self.commandType() == CommandType.ARITHMETIC):
            return self.current_instruction
        else:
            return self.current_instruction.split()[1]

    def arg2(self):
        if self.commandType() in (CommandType.PUSH, CommandType.POP, CommandType.CALL, CommandType.FUNCTION):
            return int(self.current_instruction.split()[2])
        else:
            raise ValueError("arg2() called on a non-push/pop/call command")