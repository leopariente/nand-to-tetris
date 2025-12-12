import sys
from VMTranslator import VMTranslator

def main():
    if len(sys.argv) != 2:
        print("Usage: python Main.py <inputfile.vm>")
        sys.exit(1)

    input_file = sys.argv[1]
    translator = VMTranslator(input_file)
    translator.translate()    

if __name__ == "__main__":
    main()