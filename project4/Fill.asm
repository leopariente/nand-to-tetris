(RESET)
    @SCREEN
    D=A
    @addr
    M=D

(LOOP)
    @24576
    D=M
    @SET_BLACK
    D;JNE
    D=0
    @DRAW
    0;JMP
(SET_BLACK)
    D=-1
(DRAW)
    @temp_color
    M=D
    @addr
    A=M
    M=D
    @addr
    M=M+1
    @24576
    D=A
    @addr
    D=D-M
    
    @RESET
    D;JEQ
    
    @LOOP
    0;JMP       