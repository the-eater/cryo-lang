import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/..')

from cryo_lang import CryoLangActions, CryoLangParser

if __name__ == '__main__':
    from pprint import pprint
    import sys

    parser = CryoLangParser(semantics=CryoLangActions())

    ast = parser.parse(text=sys.stdin.read())
    print('AST:')
    pprint(ast)
    print()
