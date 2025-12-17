from enum import Enum

class CommandType(Enum):
    ARITHMETIC = 0
    PUSH = 1
    POP = 2
    GOTO = 3
    IF = 4
    FUNCTION = 5
    RETURN = 6
    CALL = 7
    LABEL = 8