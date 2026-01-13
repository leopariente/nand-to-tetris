
import sys

from JackAnalyzer import JackAnalyzer

def main():
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <file.jack or directory>")
        return

    path = sys.argv[1]    
    analyzer = JackAnalyzer()
    analyzer.run(path)

if __name__ == "__main__":
    main()