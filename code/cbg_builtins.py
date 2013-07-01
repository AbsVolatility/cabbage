import string
base_chars = string.digits + string.ascii_lowercase

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
