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

    def close(self):
        if self.file:
            self.file.close()