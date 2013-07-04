from cbg_operators import *

import string
base_chars = cbgString(string.digits + string.ascii_lowercase)

import sys
if sys.version_info < (3, 0):
    input = raw_input

def base(value, base_, alphabet=base_chars):
    value_type = value.type
    if value_type not in ('integer', 'string') or base.type != 'integer' or alphabet.type != 'string':
        raise CbgTypeError("'value' argument to function 'base' must be of types 'integer' or 'string', not '{}'".format(value.type))
    elif base.type != 'integer':
        raise CbgTypeError("'base_' argument to function 'base' must be of type 'integer', not '{}'".format(base_.type))
    elif alphabet.type != 'string':
        raise CbgTypeError("'alphabet' argument to function 'base' must be of type 'string', not '{}'".format(alphabet.type))
    base, alphabet = base_.value, alphabet.value
    if not 2 <= base <= len(alphabet) + 1:
        raise CbgValueError("'base_' argument to function 'base' must be >= 2 and <= len(alphabet) + 1")
    chars = alphabet[:base]
    if value_type == 'string':
        value = value.value
        result = 0
        if value.startswith(('+', '-')):
            pos = value.pop(0) == '+'
        for digit in value:
            result *= base
            result += chars.index(digit)
        return cbgInteger(result)
    else:
        value = value.value
        neg = value < 0
        result = []
        while value:
            value, rm = divmod(value, base)
            result.append(alphabet[rm])
        if neg:
            result.append('-')
        return cbgString(''.join(result[::-1]))

def input_(prompt=''):
    return cbgString(input(prompt))

def getval(value):
    return [i.value for i in value.value] if value.type == 'list' else value.value

base, input_ = cbgFunction(base), cbgFunction(input_)