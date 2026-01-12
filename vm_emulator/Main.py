import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter
from CommandType import CommandType

def main():
    if len(sys.argv) != 2:
        print("Usage: python Main.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1].strip().strip('"').strip("'")
    
    if not os.path.exists(input_path):
        print(f"\n❌ Error: The path '{input_path}' does not exist.")
        print(f"   Python looked in: {os.path.abspath(input_path)}")
        print("   Please check the path and try again.\n")
        sys.exit(1)

    files_to_translate = []
    output_file = ""

    if os.path.isdir(input_path):
        dir_name = os.path.basename(os.path.normpath(input_path))
        output_file = os.path.join(input_path, dir_name + ".asm")
        files_to_translate = [
            os.path.join(input_path, f) 
            for f in os.listdir(input_path) 
            if f.endswith(".vm")
        ]
        
        if not files_to_translate:
            print(f"❌ Error: No .vm files found in directory: {input_path}")
            sys.exit(1)
            
    else:
        if not input_path.endswith(".vm"):
            print("❌ Error: Input file must be a .vm file.")
            sys.exit(1)
            
        output_file = input_path.replace(".vm", ".asm")
        files_to_translate = [input_path]

    print(f"Processing {len(files_to_translate)} files...")
    code_writer = CodeWriter(output_file)
    
    if os.path.isdir(input_path):
        print("Writing Bootstrap code (Sys.init)...")
        code_writer.write_init()

    for vm_file in files_to_translate:
        print(f"Translating: {os.path.basename(vm_file)}")
        parser = Parser(vm_file)
        
        if not parser.hasMoreLines():
            print(f"   -> Skipping empty file.")
            continue

        file_short_name = os.path.basename(vm_file).replace('.vm', '')
        if hasattr(code_writer, 'set_file_name'):
             code_writer.set_file_name(file_short_name)
        
        while parser.hasMoreLines():
            command_type = parser.commandType()
            
            if command_type == CommandType.ARITHMETIC:
                code_writer.write_arithmetic(parser.arg1())
            elif command_type == CommandType.RETURN:
                code_writer.write_return()
            elif command_type == CommandType.GOTO:
                code_writer.write_goto(parser.arg1())
            elif command_type == CommandType.IF:
                code_writer.write_if(parser.arg1())
            elif command_type == CommandType.LABEL:
                code_writer.write_label(parser.arg1())
            elif command_type == CommandType.FUNCTION:
                code_writer.write_function(parser.arg1(), parser.arg2())
            elif command_type == CommandType.CALL:
                code_writer.write_call(parser.arg1(), parser.arg2())   
            elif command_type in (CommandType.PUSH, CommandType.POP):
                code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
            
            parser.advance()
            
    code_writer.close()
    print(f"\n✅ Done! Output written to: {output_file}")

if __name__ == "__main__":
    main()