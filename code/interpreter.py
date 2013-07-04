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
        if debug:
            print('variables:', namespace)
        continue
    try:
        parsed = parser.parse(s)
        if debug:
            print('parse tree:', parsed)
            print()
        code = [gen(i, print_expr=True) for i in parsed.code]
        code = '\n'.join([indent(i) if isinstance(i, list) else i for i in code])
        if debug:
            print('code:\n' + code)
            print('\n---\n')
        exec(str(code), namespace)
    except CbgException as e:
        print('{}{}'.format(e.type, ': ' + str(e) if str(e) else ''))
    except NameError as e:
        print('NameError:', str(e))
