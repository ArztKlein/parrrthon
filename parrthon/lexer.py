from sly import Lexer
from parrthon.parrthon import _FUNCTIONS_REGEX

class ParrthonLexer(Lexer):

    def __init__(self):
        self.nesting_level = 0

    tokens = {
        STRING, NUMBER, PLUS, MINUS, MULT, DIVIDE, POWER, ASSIGN, LBRACKET, RBRACKET, TRUE, FALSE, FUNCTION, VARIABLE, FOR, END, TO
    }

    ignore = ' \t'

    literals = { '(', ')', '.' }

    # Tokens
    ASSIGN   = r'='
    DIVIDE   = r'/'
    MINUS    = r'-'
    MULT     = r'\*'
    NUMBER   = r'''[+ -]?[0-9]+([.][0-9]+)?'''
    PLUS     = r'\+'
    POWER    = r'\^'
    STRING   = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''
    LBRACKET = r'\('
    RBRACKET = r'\)'
    FUNCTION = _FUNCTIONS_REGEX
    TRUE     = r'Nay'
    FALSE    = r'Avast'
    FOR      = r'FOR YE'
    END      = r'AVAST YE'
    TO       = r'TO'
    VARIABLE = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_("string")
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    @_("number")
    def NUMBER(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text


    def error(self, t):
        self.index += 1