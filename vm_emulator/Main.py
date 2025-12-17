import sys
import os
from VMTranslator import VMTranslator

def main():
    if len(sys.argv) != 2:
        print("Usage: python Main.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    target_file = input_path

    if os.path.isdir(input_path):
        dir_name = os.path.basename(os.path.normpath(input_path))
        merged_vm_path = os.path.join(input_path, dir_name + ".vm")
        vm_files = [f for f in os.listdir(input_path) if f.endswith(".vm")]
        
        if not vm_files:
            print("No .vm files found in this directory.")
            sys.exit(1)

        with open(merged_vm_path, 'w') as outfile:
            for vm_file in vm_files:
                full_path = os.path.join(input_path, vm_file)
                
                with open(full_path, 'r') as infile:
                    # Optional: Write a comment indicating source file start
                    outfile.write(f"// Start of {vm_file}\n")
                    outfile.write(infile.read())
                    outfile.write("\n") # Ensure newline between files
        
        target_file = merged_vm_path
    translator = VMTranslator(target_file)
    translator.translate()  

if __name__ == "__main__":
    main()