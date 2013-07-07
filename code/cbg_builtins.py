from cbg_types import *

import sys
if sys.version_info < (3, 0):
    input = raw_input

def base(value, bse, alphabet=cbgString('0123456789abcdefghijklmnopqrstuvwxyz')):
    value_type = value.type
    if value_type not in ('integer', 'string'):
        raise TypeError("'value' argument to function 'base' must be of type 'integer' or 'string', not '{}'".format(value.type))
    elif bse.type != 'integer':
        raise TypeError("'base' argument to function 'base' must be of type 'integer', not '{}'".format(bse.type))
    elif alphabet.type != 'string':
        raise TypeError("'alphabet' argument to function 'base' must be of type 'string', not '{}'".format(alphabet.type))
    bse, alphabet = bse.value, alphabet.out
    if not 2 <= bse <= len(alphabet) + 1:
        raise ValueError("'base' argument to function 'base' must be >= 2 and <= len(alphabet) + 1")
    chars = alphabet[:bse]
    if value_type == 'string':
        value = value.out
        result = 0
        if value.startswith(('+', '-')):
            pos = value.pop(0) == '+'
        for digit in value:
            result *= bse
            result += chars.index(digit)
        return cbgInteger(result)
    else:
        value = value.value
        neg = value < 0
        result = []
        while value:
            value, rm = divmod(value, bse)
            result.append(alphabet[rm])
        if neg:
            result.append('-')
        return cbgString(''.join(result[::-1]))

def input_(prompt=cbgString('')):
    return cbgString(input(prompt.out))

funcs = {'base': cbgFunction(base), 'input': cbgFunction(input_)}