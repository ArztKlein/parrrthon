from sly import Parser
from parrthon.parrthon import FUNCTIONS
from parrthon.lexer import ParrthonLexer
from parrthon.errors import *

from operator import add, mul, sub, truediv, pow

def throw_error(error):
        print(error)
        raise ExitParrthon

class Statement:
    def __init__(self, func, values: tuple):
        self.values = values

        try:
            self.func = FUNCTIONS[func]["func"]
            if self.func is None:
                self.func = func
        except KeyError:
            self.func = func

    def run(self, parser):

        if isinstance(self.func, str):
            return self.__run_str(parser)
        
        value1 = self.values[0]

        if isinstance(value1, Statement):
            value1 = value1.run(parser)


        # TODO: Clean this up
        try:
            return self.func(value1)
        except TypeError:
            value2 = self.values[1]

            if isinstance(value2, Statement):
                value2 = value2.run(parser)
            
            return self.func(value1, value2)


    def __run_str(self, parser):
        def unknown_func():
            throw_error(UnknownFunctionError(self.func))
        

        # Get information about the function
        try:
            func_data = FUNCTIONS[self.func]
        except KeyError:
            unknown_func()

        params_amount = func_data["params"]

        
        values = list(self.values).copy()

        # Convert any statements into values
        for idx, value in enumerate(values):
            if isinstance(value, Statement):
                values[idx] = value.run(parser)


        # Run the function
        # TODO: Clean up this mess
        if params_amount == 0:
            match self.func:
                case "NOOP":
                    ...
                case _:
                    unknown_func()
        elif params_amount == 1:
            match self.func:
                case "GET":
                    return parser.get_variable(values[0])
                case _:
                    unknown_func()
        elif params_amount == 2:
            match self.func:
                case "ASSIGN":
                    return parser.set_variable(values[0], values[1])
                case _:
                    unknown_func()


class Loop:
    def __init__(self, identifier, start, end, statement):
        self.identifier = identifier
        self.start      = start
        self.end        = end
        self.statement  = statement

    def run(self, parser):
        for i in range(self.start, self.end):
            parser.set_variable(self.identifier, i)
            self.statement.run(parser)
            
        

class ParrthonParser(Parser):
    tokens = ParrthonLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', MULT, DIVIDE),
        ('right', POWER)
    )

    def __init__(self):
        self.variables = {}
    

    def get_variable(self, identifier):

        try:
            return self.variables[identifier]
        except KeyError:
            self.throw_error(InvalidVariableError(identifier))
    

    def set_variable(self, name, value):
        self.variables[name] = value

    
    @_("statement")
    def a(self, p):
        p.statement.run(self)


    @_("loop_start statement end")
    def statement(self, p):
        name, start, end = p.loop_start.values
        return Loop(name, start, end, p.statement)

    @_("expr")
    def statement(self, p):
        if isinstance(p.expr, Statement):
            return p.expr

        return Statement("NOOP", (0, 0))

    @_("VARIABLE ASSIGN expr")
    def statement(self, p):
        return Statement("ASSIGN", (p.VARIABLE, p.expr))
    
    @_("func LBRACKET expr RBRACKET")
    def expr(self, p):
        return Statement(p.func, (p.expr,))

    @_("expr MINUS expr")
    def expr(self, p):
        return Statement(sub, (p.expr0, p.expr1))

    @_("expr PLUS expr")
    def expr(self, p):
        return Statement(add, (p.expr0, p.expr1))

    @_("expr MULT expr")
    def expr(self, p):
        return Statement(mul, (p.expr0, p.expr1))

    @_("expr DIVIDE expr")
    def expr(self, p):
        return Statement(truediv, (p.expr0, p.expr1))

    @_("expr POWER expr")
    def expr(self, p):
        return Statement(pow, (p.expr0, p.expr1))
    
    @_("LBRACKET expr RBRACKET")
    def expr(self, p):
        return p.expr

    @_("STRING")
    def expr(self, p):
        return p.STRING
    
    @_("FALSE")
    def expr(self, p):
        return False
    
    @_("TRUE")
    def expr(self, p):
        return True

    @_("VARIABLE")
    def expr(self, p):
        return Statement("GET", (p.VARIABLE,))

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_("FUNCTION")
    def func(self, p):
        return p.FUNCTION

    @_("FOR VARIABLE ASSIGN NUMBER TO NUMBER")
    def loop_start(self, p):
        return Statement("FOR_HEADER", (p.VARIABLE, p.NUMBER0, p.NUMBER1))

    @_("END")
    def end(self, p):
        return "END"

    