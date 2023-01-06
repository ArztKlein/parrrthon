import sys

from parrthon.lexer import ParrthonLexer
from parrthon.parser import ParrthonParser
from parrthon.errors import ExitParrthon

def read_file(path: str):
    lexer = ParrthonLexer()
    parser = ParrthonParser()

    with open(path, 'r') as f:
        lines = f.read().splitlines()
        
    # Remove empty lines
    lines = list(filter(None, lines))

    # Parse each line
    for line in lines:
        try:    
            parser.parse(lexer.tokenize(line))
        except EOFError:
            break
        except ExitParrthon:
            return


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Ye biscuit eater need a .parr file path"
    
    path = sys.argv[1]

    read_file(path)