from cbg_types import *

#-------------------------------------------------------------------------------
# Arithmetic operators

def add(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    c = a.value + b.value
    if isinstance(c, int):
        return cbgInteger(c)
    else:  # a float
        return cbgFloat(c)

def sub(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    c = a.value - b.value
    if isinstance(c, int):
        return cbgInteger(c)
    else:  # a float
        return cbgFloat(c)

def mul(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    c = a.value * b.value
    if isinstance(c, int):
        return cbgInteger(c)
    else:  # a float
        return cbgFloat(c)

def div(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    c = a.value / b.value
    if isinstance(c, int):
        return cbgInteger(c)
    else:  # a float
        return cbgFloat(c)

#-------------------------------------------------------------------------------
# comparison operators

def lt(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value < b.value)

def le(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value <= b.value)

def eq(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value == b.value)

def ne(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value != b.value)

def ge(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value >= b.value)

def gt(a, b):
    if a.type not in ('integer', 'float') or b.type not in ('integer', 'float'):
        raise ValueError
    return cbgBool(a.value > b.value)
