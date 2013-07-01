from __future__ import print_function

import sys
if sys.version_info < (3, 0):
    input = raw_input

from cabbage import *

debug = input('Debug mode? (y/n)> ').lower().startswith('y')

while True:
    s = input('@> ')
    if not s:
        if debug:
            print('variables:', namespace)
        continue
    parsed = parser.parse(s)
    if debug:
        print(parsed)
    if parsed.type == 'expression':
        code = 'print("{}")'.format(gen(parsed.value))
    else:
        code = gen(parsed)
    if debug:
        print(code)
    exec(str(code), namespace)

