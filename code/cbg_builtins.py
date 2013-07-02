import string
base_chars = string.digits + string.ascii_lowercase

from cbg_operators import *

import sys
if sys.version_info < (3, 0):
    input = raw_input

def base(value, base, alphabet=base_chars):
    if not isinstance(value, (str, int)) or not isinstance(alphabet, str):
        raise TypeError
    if not 2 <= base <= len(alphabet) + 1:
        raise ValueError
    chars = alphabet[:base]
    if isinstance(value, str):
        result = 0
        if value.startswith(('+', '-')):
            pos = value.pop(0) == '+'
        for digit in value:
            result *= base
            result += chars.index(digit)
        return result
    else:
        neg = value < 0
        result = []
        while value:
            value, rm = divmod(value, base)
            result.append(alphabet[rm])
        if neg:
            result.append('-')
        return ''.join(result[::-1])

def input_(prompt=''):
    return cbgString(input(prompt))