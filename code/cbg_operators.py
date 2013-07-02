from cbg_types import *

#-------------------------------------------------------------------------------
# Arithmetic operators

def uplus(a):
    if a.type in ('integer', 'float'):
        return a
    else:
        raise ValueError

def uminus(a):
    if a.type == 'integer':
        return cbgInteger(-a.value)
    elif a.type == 'float':
        return cbgFloat(-a.value)
    else:
        raise ValueError

def add(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value + b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value + b.value)
    elif a_type == b_type == 'string':
        return cbgString(a.value + b.value)
    elif a_type == b_type == 'list':
        return cbgList(a.value + b.value)
    else:
        raise ValueError

def sub(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value - b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value - b.value)
    else:
        raise ValueError

def mul(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value * b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value * b.value)
    elif (a_type == 'string' and b_type == 'integer') or (b_type == 'string' and a_type == 'integer'):
        return cbgString(a.value * b.value)
    elif (a_type == 'list' and b_type == 'integer') or (b_type == 'list' and a_type == 'integer'):
        return cbgString(a.value * b.value)
    else:
        raise ValueError

def div(a, b):
    a_type, b_type = a.type, b.type
    if a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value / b.value)
    else:
        raise ValueError

def pow_(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value ** b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value ** b.value)
    else:
        raise ValueError

#-------------------------------------------------------------------------------
# Bitwise operators

def bwand(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value & b.value)
    else:
        raise ValueError

def bwor(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value | b.value)
    else:
        raise ValueError

def bwxor(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value ^ b.value)
    else:
        raise ValueError

def bwnot(a):
    if a.type == 'integer':
        return cbgInteger(~a.value)
    else:
        raise ValueError

#-------------------------------------------------------------------------------
# Boolean operators

def bland(a, b):
    if a.type == b.type == 'bool':
        return cbgBool(a.value and b.value)
    else:
        raise ValueError

def blor(a, b):
    if a.type == b.type == 'bool':
        return cbgBool(a.value or b.value)
    else:
        raise ValueErro

def blnot(a):
    if a.type == 'bool':
        return cbgBool(not a.value)
    else:
        raise ValueError

#-------------------------------------------------------------------------------
# Comparison operators
# - implement string comparisons

def lt(a, b):
    a_type, b_type = a.type, b.type
    if a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgBool(a.value < b.value)
    else:
        raise ValueError

def le(a, b):
    return cbgBool(lt(a, b).value or eq(a, b).value)

def eq(a, b):
    return cbgBool(a.value == b.value)

def ne(a, b):
    return cbgBool(a.value != b.value)

def ge(a, b):
    return cbgBool(gt(a, b).value or eq(a, b).value)

def gt(a, b):
    a_type, b_type = a.type, b.type
    if a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgBool(a.value > b.value)
    else:
        raise ValueError

#-------------------------------------------------------------------------------
# Other operators

def rnge(a, b):
    if a.type == b.type == 'integer':
        return cbgList([cbgInteger(i) for i in range(a.value, b.value+1)])
    else:
        raise ValueError
