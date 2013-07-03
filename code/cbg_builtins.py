from cbg_operators import *

import string
base_chars = cbgString(string.digits + string.ascii_lowercase)

import sys
if sys.version_info < (3, 0):
    input = raw_input

def base(value, base, alphabet=base_chars):
    value_type = value.type
    if value_type not in ('integer', 'string') or base.type != 'integer' or alphabet.type != 'string':
        raise TypeError
    base, alphabet = base.value, alphabet.value
    if not 2 <= base <= len(alphabet) + 1:
        raise ValueError
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

base, input_ = cbgFunction(base), cbgFunction(input_)