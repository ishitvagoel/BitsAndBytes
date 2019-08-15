""""https://repl.it/@Ishitva/StacksSymbolBalance"""


SYMBOLS_MAP = {
    '>': '<',
    '}': '(',
    ']': '[',
    '}': '{',

}

def areSymbolsBalanced(expression):
    symbol_stack = []
    opening_symbols = SYMBOLS_MAP.values()
    closing_symbols = SYMBOLS_MAP.keys()

    for symbol in expression:
        if symbol in opening_symbols:
            symbol_stack.append(symbol)

        if symbol in closing_symbols:
            symbol_stack_size = len(symbol_stack)
            if symbol_stack_size < 1:
                return False
            popped = symbol_stack.pop(symbol_stack_size - 1)
            if SYMBOLS_MAP.get(symbol) == popped:
                continue
            else:
                return False

    if not symbol_stack:
        return True
    return False




