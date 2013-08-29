from __future__ import print_function

import sys
if sys.version_info < (3, 0):
    input = raw_input

from cabbage import *

debug = input('Debug mode? (y/n)> ').lower().startswith('y')

while True:
    s = input('@> ')
    if s and not s.endswith(';'):
        while True:
            s += input('.. ')
            if s.endswith(';') and (s.count('{') - s.count('}') == 0):
                break
    if not s:
        continue
    try:
        parsed = parser.parse(s, lexer=lexer)
        if debug:
            print('parse tree:', parsed)
            print()
        code = [gen(i, print_expr=True) for i in parsed.code]
        code = indent(code)
        if debug:
            print('code:\n' + code)
            print('\n---\n')
        exec(str(code), namespace)
    except Exception as e:
        print('{}: {}'.format(type(e).__name__, str(e)))