FUNCTIONS = {
    'chantey': {"func": print, "params": 1},
    'input'  : {"func": input, "params": 1},
    'ASSIGN' : {"func": None, "params": 2},
    'GET'    : {"func": None, "params": 1}
}

_FUNCTIONS_REGEX = '(' + '|'.join([func if FUNCTIONS[func]["func"] is not None else "<TEMP>" for func in FUNCTIONS]).replace("|<TEMP>", '') + ')'