from CommandType import CommandType

SEGMENT_POINTERS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT"
}

class CodeWriter:
    
    def __init__(self, output_file):
        self.output_file = output_file
        self.file = open(self.output_file, 'w')
        self.label_count = 0
        self.function_count = 0

    def write_init(self):
        """
        Writes the assembly code that initializes the VM.
        1. SP = 256
        2. call Sys.init 0
        """
        self.file.write("// Bootstrap Code\n")
        
        # --- Task 1: Set SP = 256 ---
        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
        
        # --- Task 2: Call Sys.init ---
        # We reuse the write_call method to handle the complex stack logic
        # of saving the frame and jumping.
        self.write_call("Sys.init", 0)    

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given 
        arithmetic command.
        """
        # Debug comment to make the asm file readable
        self.file.write(f"// {command}\n")

        # --- Binary Operators (add, sub, and, or) ---
        if command in ['add', 'sub', 'and', 'or']:
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")   # SP-- and access top value (y)
            self.file.write("D=M\n")      # D = y
            self.file.write("A=A-1\n")    # Point to the second value (x)
            
            if command == 'add':
                self.file.write("M=D+M\n") # x = x + y
            elif command == 'sub':
                self.file.write("M=M-D\n") # x = x - y
            elif command == 'and':
                self.file.write("M=D&M\n") # x = x & y
            elif command == 'or':
                self.file.write("M=D|M\n") # x = x | y

        # --- Unary Operators (neg, not) ---
        elif command in ['neg', 'not']:
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")    # Point to the top value (y)
            
            if command == 'neg':
                self.file.write("M=-M\n") # y = -y
            elif command == 'not':
                self.file.write("M=!M\n") # y = !y

        # --- Comparison Operators (eq, gt, lt) ---
        elif command in ['eq', 'gt', 'lt']:
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")   # SP-- (pop y)
            self.file.write("D=M\n")      # D = y
            self.file.write("A=A-1\n")    # Point to x
            self.file.write("D=M-D\n")    # D = x - y
            
            # Generate unique labels for this specific comparison
            label_true = f"TRUE_{self.label_count}"
            label_end = f"END_{self.label_count}"
            self.label_count += 1
            
            self.file.write(f"@{label_true}\n")
            
            if command == 'eq':
                self.file.write("D;JEQ\n") # Jump to TRUE if x-y == 0
            elif command == 'gt':
                self.file.write("D;JGT\n") # Jump to TRUE if x-y > 0
            elif command == 'lt':
                self.file.write("D;JLT\n") # Jump to TRUE if x-y < 0
            
            # Case: False (0)
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=0\n")       # Set stack top to False (0)
            self.file.write(f"@{label_end}\n")
            self.file.write("0;JMP\n")     # Jump to end
            
            # Case: True (-1)
            self.file.write(f"({label_true})\n")
            self.file.write("@SP\n")
            self.file.write("A=M-1\n")
            self.file.write("M=-1\n")      # Set stack top to True (-1)
            self.file.write(f"({label_end})\n")

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.
        """
        self.file.write(f"// {command} {segment} {index}\n")

        # -----------------------------------------------------------
        # HANDLING PUSH
        # -----------------------------------------------------------
        if command == CommandType.PUSH:
            
            # 1. Constant Segment (Slide 21)
            # Logic: *SP = i, SP++
            if segment == "constant":
                self.file.write(f"@{index}\n")
                self.file.write("D=A\n")
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            # 2. Local, Argument, This, That (Slide 25)
            # Logic: addr = segmentPointer + i, *SP = *addr, SP++
            elif segment in ["local", "argument", "this", "that"]:
                # Calculate the address: Base Pointer + Index
                pointer = SEGMENT_POINTERS[segment]
                self.file.write(f"@{pointer}\n")
                self.file.write("D=M\n")        # D = base address
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")      # A = base + index (Target Address)
                self.file.write("D=M\n")        # D = *addr (Get value)
                
                # Push D to stack
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            # 3. Temp Segment (Slide 35)
            # Logic: addr = 5 + i, ...
            elif segment == "temp":
                self.file.write("@5\n")
                self.file.write("D=A\n")
                self.file.write(f"@{index}\n")
                self.file.write("A=D+A\n")      # A = 5 + index
                self.file.write("D=M\n")
                
                # Push D
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            # 4. Pointer Segment (Slide 38)
            # Logic: 0 -> THIS, 1 -> THAT
            elif segment == "pointer":
                this_or_that = "THIS" if index == 0 else "THAT"
                self.file.write(f"@{this_or_that}\n")
                self.file.write("D=M\n")
                
                # Push D
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

            # 5. Static Segment (Slide 32)
            # Logic: @FileName.i
            elif segment == "static":
                # Ensure you have self.filename set! Default to 'Unknown' if not.
                filename = getattr(self, 'filename', 'Unknown')
                self.file.write(f"@{filename}.{index}\n")
                self.file.write("D=M\n")
                
                # Push D
                self.file.write("@SP\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")
                self.file.write("@SP\n")
                self.file.write("M=M+1\n")

        # -----------------------------------------------------------
        # HANDLING POP
        # -----------------------------------------------------------
        elif command == CommandType.POP:
            
            # 1. Local, Argument, This, That (Slide 24)
            # Complexity: We need to store the address in R13 because we need D for the data.
            if segment in ["local", "argument", "this", "that"]:
                pointer = SEGMENT_POINTERS[segment]
                self.file.write(f"@{pointer}\n")
                self.file.write("D=M\n")
                self.file.write(f"@{index}\n")
                self.file.write("D=D+A\n")      # D = base + index
                
                self.file.write("@R13\n")       # Store target address in R13
                self.file.write("M=D\n")
                
                self.file.write("@SP\n")        # Pop value to D
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                
                self.file.write("@R13\n")       # Retrieve target address
                self.file.write("A=M\n")
                self.file.write("M=D\n")        # Write data to target

            # 2. Temp Segment
            elif segment == "temp":
                self.file.write("@5\n")
                self.file.write("D=A\n")
                self.file.write(f"@{index}\n")
                self.file.write("D=D+A\n")      # D = 5 + index
                
                self.file.write("@R13\n")
                self.file.write("M=D\n")
                
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                
                self.file.write("@R13\n")
                self.file.write("A=M\n")
                self.file.write("M=D\n")

            # 3. Pointer Segment
            elif segment == "pointer":
                this_or_that = "THIS" if index == 0 else "THAT"
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                
                self.file.write(f"@{this_or_that}\n")
                self.file.write("M=D\n")

            # 4. Static Segment
            elif segment == "static":
                filename = getattr(self, 'filename', 'Unknown')
                self.file.write("@SP\n")
                self.file.write("AM=M-1\n")
                self.file.write("D=M\n")
                
                self.file.write(f"@{filename}.{index}\n")
                self.file.write("M=D\n")

    def write_goto(self, label):
        self.file.write(f"@{label}\n")
        self.file.write("0;JMP\n")

    def write_label(self, label):
        self.file.write(f"({label})\n")

    def write_if(self, label):
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write(f"@{label}\n")
        self.file.write("D;JNE\n")

    def write_function(self, function_name, total_vars):
        self.file.write(f"({function_name})\n")
        for i in range(int(total_vars)):
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=0\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")

    def write_call(self, function_name, total_args):
        self.file.write(f"// call {function_name} {total_args}\n")
        return_label = f"{function_name}$ret.{self.function_count}"
        self.function_count += 1
        for segment in [return_label, "LCL", "ARG", "THIS", "THAT"]:
            self.file.write(f"@{segment}\n")
            if segment == return_label:
                self.file.write("D=A\n")
            else:
                self.file.write("D=M\n")
            self.file.write("@SP\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
            self.file.write("@SP\n")
            self.file.write("M=M+1\n")
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write(f"@{int(total_args) + 5}\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
        # Set LCL = SP
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
        # Jump to the called function
        self.file.write(f"@{function_name}\n")
        self.file.write("0;JMP\n")
        # Declare the return label
        self.file.write(f"({return_label})\n")

    def write_return(self):
        self.file.write("// return\n")

        # 1. FRAME = LCL (Store LCL in temporary variable R13)
        # We need this anchor because we will change LCL later.
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@R13\n")
        self.file.write("M=D\n")

        # 2. RET = *(FRAME - 5) (Store return address in temp variable R14)
        # The return address was pushed 5 slots before the local variables.
        # D currently holds FRAME (LCL value)
        self.file.write("@5\n")
        self.file.write("A=D-A\n") # A = FRAME - 5
        self.file.write("D=M\n")   # D = content at FRAME-5 (Return Address)
        self.file.write("@R14\n")
        self.file.write("M=D\n")   # R14 = Return Address

        # 3. *ARG = pop() (Reposition the return value for the caller)
        # The return value is at the top of the stack. 
        # We put it where the caller expects it (at location ARG).
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")   # D = return value
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")   # *ARG = return value

        # 4. SP = ARG + 1 (Restore SP of the caller)
        # The caller's stack pointer should be right after the return value.
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")

        # 5. Restore THAT = *(FRAME - 1)
        self.file.write("@R13\n") # Get FRAME
        self.file.write("D=M\n")
        self.file.write("@1\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@THAT\n")
        self.file.write("M=D\n")

        # 6. Restore THIS = *(FRAME - 2)
        self.file.write("@R13\n")
        self.file.write("D=M\n")
        self.file.write("@2\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@THIS\n")
        self.file.write("M=D\n")

        # 7. Restore ARG = *(FRAME - 3)
        self.file.write("@R13\n")
        self.file.write("D=M\n")
        self.file.write("@3\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")

        # 8. Restore LCL = *(FRAME - 4)
        self.file.write("@R13\n")
        self.file.write("D=M\n")
        self.file.write("@4\n")
        self.file.write("A=D-A\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")

        # 9. goto RET (Jump to the saved return address)
        self.file.write("@R14\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")

    def set_file_name(self, file_name):
        self.filename = file_name.split('/')[-1].split('\\')[-1].replace('.vm', '') 
        
    def close(self):
        if self.file:
            self.file.close()