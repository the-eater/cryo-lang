import os 
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
    import pprint
    import json
    from tatsu import parse
    from tatsu.util import asjson

    with open(dir_path + '/../bnf/cryo-lang.ebnf') as f:
        ast = parse(f.read(), sys.stdin.read())
    print('PPRINT')
    pprint.pprint(ast, indent=2, width=20)
    print()

    print('JSON')
    print(json.dumps(asjson(ast), indent=2))
    print()


if __name__ == '__main__':
    main()

