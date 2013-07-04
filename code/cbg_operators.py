from cbg_types import *
from cbg_errors import *

#-------------------------------------------------------------------------------
# Arithmetic operators

def uplus(a):
    if a.type in ('integer', 'float'):
        return a
    else:
        raise CbgTypeError("unary operator '+' not defined for type '{}'".format(a.type))

def uminus(a):
    if a.type == 'integer':
        return cbgInteger(-a.value)
    elif a.type == 'float':
        return cbgFloat(-a.value)
    else:
        raise CbgTypeError("unary operator '-' not defined for type '{}'".format(a.type))

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
        raise CbgTypeError("binary operator '+' not defined for types '{}' and '{}'".format(a.type, b.type))

def sub(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value - b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value - b.value)
    else:
        raise CbgTypeError("binary operator '-' not defined for types '{}' and '{}'".format(a.type, b.type))

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
        raise CbgTypeError("binary operator '*' not defined for types '{}' and '{}'".format(a.type, b.type))

def div(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer' and mod(a, b).value == 0:
        return cbgInteger(a.value // b.value)
    if a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value / b.value)
    else:
        raise CbgTypeError("binary operator '/' not defined for types '{}' and '{}'".format(a.type, b.type))

def pow_(a, b):
    a_type, b_type = a.type, b.type
    if a_type == b_type == 'integer':
        return cbgInteger(a.value ** b.value)
    elif a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgFloat(a.value ** b.value)
    else:
        raise CbgTypeError("binary operator '^' not defined for types '{}' and '{}'".format(a.type, b.type))

def mod(a, b):
    if a.type in ('integer', 'float') and b.type in ('integer', 'float'):
        return cbgFloat(a.value % b.value)
    else:
        raise CbgTypeError("binary operator '%' not defined for types '{}' and '{}'".format(a.type, b.type))

#-------------------------------------------------------------------------------
# Bitwise operators

def bwand(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value & b.value)
    else:
        raise CbgTypeError("binary operator '.&' not defined for types '{}' and '{}'".format(a.type, b.type))

def bwor(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value | b.value)
    else:
        raise CbgTypeError("binary operator '.|' not defined for types '{}' and '{}'".format(a.type, b.type))

def bwxor(a, b):
    if a.type == b.type == 'integer':
        return cbgInteger(a.value ^ b.value)
    else:
        raise CbgTypeError("binary operator '.^' not defined for types '{}' and '{}'".format(a.type, b.type))

def bwnot(a):
    if a.type == 'integer':
        return cbgInteger(~a.value)
    else:
        raise CbgTypeError("unary operator '.~' not defined for type '{}'".format(a.type))

#-------------------------------------------------------------------------------
# Boolean operators

def bland(a, b):
    if a.type == b.type == 'bool':
        return cbgBool(a.value and b.value)
    else:
        raise CbgTypeError("binary operator '&' not defined for types '{}' and '{}'".format(a.type, b.type))

def blor(a, b):
    if a.type == b.type == 'bool':
        return cbgBool(a.value or b.value)
    else:
        raise CCbgTypeError("binary operator '|' not defined for types '{}' and '{}'".format(a.type, b.type))

def blnot(a):
    return cbgBool(not a.value)

#-------------------------------------------------------------------------------
# Comparison operators
# - implement string comparisons

def lt(a, b):
    a_type, b_type = a.type, b.type
    if a_type in ('integer', 'float') and b_type in ('integer', 'float'):
        return cbgBool(a.value < b.value)
    else:
        raise CbgTypeError("binary operator '<' not defined for types '{}' and '{}'".format(a.type, b.type))

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
        raise CbgTypeError("binary operator '>' not defined for types '{}' and '{}'".format(a.type, b.type))

#-------------------------------------------------------------------------------
# Sequence operators

def slce(lst, index):
    if index.type == 'integer':
        lst_type = lst.type
        if lst_type == 'string':
            return cbgString(lst.value[index.value])
        elif lst_type == 'list':
            return lst.value[index.value]
        else:
            raise CbgTypeError("'{}' object is not subscriptable".format(lst.type))
    if index.type == 'list':
        if not all(i.type in ('integer', 'none') for i in index.value):
            raise CbgTypeError("slice values must be integers or 'None'")
        lst_type = lst.type
        if lst_type == 'string':
            return cbgString(lst.value[slice(*[i.value for i in index.value])])
        elif lst_type == 'list':
            return cbgList(lst.value[slice(*[i.value for i in index.value])])
        else:
            raise CbgTypeError("'{}' object is not subscriptable".format(lst.type))
    else:
        raise CbgTypeError("invalid index type '{}'".format(index.type))

#-------------------------------------------------------------------------------
# Other operators

def rnge(a, b):
    if a.type == b.type == 'integer':
        return cbgList([cbgInteger(i) for i in range(a.value, b.value+1)])
    else:
        raise CbgTypeError("binary operator '..' not defined for types '{}' and '{}'".format(a.type, b.type))
