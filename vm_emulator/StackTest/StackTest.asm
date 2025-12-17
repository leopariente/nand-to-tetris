// CommandType.PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.POP pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// CommandType.PUSH constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// CommandType.PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.POP this 2
@THIS
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// CommandType.PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.POP that 6
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// CommandType.PUSH pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// CommandType.PUSH this 2
@THIS
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// CommandType.PUSH that 6
@THAT
D=M
@6
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// CommandType.PUSH constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.PUSH constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// CommandType.PUSH constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.PUSH constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.PUSH constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// CommandType.POP static 8
@SP
AM=M-1
D=M
@Unknown.8
M=D
// CommandType.POP static 3
@SP
AM=M-1
D=M
@Unknown.3
M=D
// CommandType.POP static 1
@SP
AM=M-1
D=M
@Unknown.1
M=D
// CommandType.PUSH static 3
@Unknown.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// CommandType.PUSH static 1
@Unknown.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// CommandType.PUSH static 8
@Unknown.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
