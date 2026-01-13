import sys
import os
from JackTokenizer import JackTokenizer
from Constants import *

class JackAnalyzer:
    """
    The analyzer driver. It handles the input files and drives the process.
    For Project 10 (Stage 0), it generates XxxT.xml files using the Tokenizer.
    """
    
    def __init__(self):
        pass

    def run(self, input_path):
        """
        Main entry point. Determines if input is a file or a directory
        and processes accordingly.
        """
        if os.path.isfile(input_path):
            if input_path.endswith('.jack'):
                self._analyze_file(input_path)
        elif os.path.isdir(input_path):
            for filename in os.listdir(input_path):
                if filename.endswith(".jack"):
                    full_path = os.path.join(input_path, filename)
                    self._analyze_file(full_path)
        else:
            print(f"Error: The path '{input_path}' is invalid.")

    def _analyze_file(self, input_file):
        """
        Processes a single .jack file and generates a corresponding T.xml file.
        """
        output_file = input_file.replace('.jack', 'T.xml')
        
        try:
            tokenizer = JackTokenizer(input_file)
            
            with open(output_file, 'w') as f:
                f.write('<tokens>\n')
                
                while tokenizer.has_more_tokens():
                    tokenizer.advance()
                    token_type = tokenizer.token_type()
                    
                    if token_type == KEYWORD:
                        line = f"<keyword> {tokenizer.keyword()} </keyword>\n"
                        
                    elif token_type == SYMBOL:
                        val = self._xml_escape(tokenizer.symbol())
                        line = f"<symbol> {val} </symbol>\n"
                        
                    elif token_type == IDENTIFIER:
                        line = f"<identifier> {tokenizer.identifier()} </identifier>\n"
                        
                    elif token_type == INT_CONST:
                        line = f"<integerConstant> {tokenizer.int_val()} </integerConstant>\n"
                        
                    elif token_type == STRING_CONST:
                        line = f"<stringConstant> {tokenizer.string_val()} </stringConstant>\n"
                        
                    f.write(line)
                    
                f.write('</tokens>\n')
            
            print(f"Created: {output_file}")
            
        except IOError as e:
            print(f"File Error: {e}")

    def _xml_escape(self, val):
        """
        Helper method to handle XML special characters.
        """
        if val == '<': return '&lt;'
        if val == '>': return '&gt;'
        if val == '"': return '&quot;'
        if val == '&': return '&amp;'
        return val