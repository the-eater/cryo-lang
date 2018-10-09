from .parser import CryoLangParser, CryoLangSemantics
import re

class CryoSetStmt(object):
    def __init__(self, left, right, action) -> None:
        super().__init__()

        self.left = left
        self.right = right
        self.action = action

    def __repr__(self):
        return '<SetStmt {} {} {}>'.format(repr(self.left), repr(self.action), repr(self.right))


class CryoValue(object):
    def __init__(self, val):
        super().__init__()

        self.val = val

    def __repr__(self):
        return '<{} {}>'.format(type(self).__name__, repr(self.val))


class CryoNewline(object):
    def __repr__(self):
        return '<CryoNewline>'


class CryoFuncCall(object):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return '<CryoFuncCall {} {}>'.format(self.func, self.args)


class CryoObjectCreation(object):
    def __init__(self, assignments):
        self.assignments = assignments

    def __repr__(self):
        return '<CryoObjectCreation {}>'.format(self.assignments)


class CryoObjectKv(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return '<CryoObjectKv {}: {}>'.format(self.key, self.value)


class CryoArray(CryoValue):
    pass


class CryoSpread(CryoValue):
    pass


class CryoObjectKeyExpr(object):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return '<CryoObjectKeyExpr {}>'.format(self.expr)


class CryoLookup(object):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<CryoLookup {}>'.format(self.path)


class CryoIfStmt(object):
    def __init__(self, test, then, otherwise):
        self.test = test
        self.then = then
        self.otherwise = otherwise

    def __repr__(self):
        return '<CryoIfStmt if {} then {} else {}>'.format(self.test, self.then, self.otherwise)


class CryoObjectAssignAs(object):
    def __init__(self, origin, target):
        self.origin = origin
        self.target = target

    def __repr__(self):
        return '<CryoObjectAssignAs {} as {}>'.format(self.origin, self.target)


class CryoLangActions(CryoLangSemantics):
    escape_string = re.compile(r'\\(.)')
    escapes = {
        '\\': '\\',
        'n': '\\n',
        '\'': '\'',
        '"': '"',
    }

    def stmt_coll(self, ast):
        return super().stmt_coll(ast)

    def stmt(self, ast):
        return super().stmt(ast)

    def tokens(self, ast):
        if ast == 'null':
            return CryoValue(None)

        if ast == 'false':
            return CryoValue(False)

        return CryoValue(True)

    def set_stmt(self, ast):
        return CryoSetStmt(left=ast['left'], action=ast['action'], right=ast['right'])

    def obj_path(self, ast):
        return CryoLookup(ast)

    def nl(self, ast):
        return CryoNewline()

    def string(self, ast):
        return CryoValue(self.escape_string.sub(lambda x: self.escapes[x[1]] if x[1] in self.escapes else x[1], ast[1:-1]))

    def digit(self, ast):
        return CryoValue(float(ast))

    def func_call(self, ast):
        return CryoFuncCall(ast['func'], ast['args'])

    def arr(self, ast):
        return CryoArray(ast[1:])

    def obj(self, ast):
        return CryoObjectCreation(ast)

    def obj_kv(self, ast):
        return CryoObjectKv(ast['key'], ast['val'] if ast['val'] is not None else ast['key'])

    def if_stmt(self, ast):
        return CryoIfStmt(ast['test'], ast['then'] or [], ast['otherwise'] or [])

    def obj_key_expr(self, ast):
        return CryoObjectKeyExpr(ast)

    def obj_assg_to(self, ast):
        if isinstance(ast, str):
            return CryoLookup([ast])

        return ast

    def obj_as(self, ast):
        return CryoObjectAssignAs(ast['origin'], ast['target'])

    def obj_spread(self, ast):
        return CryoSpread(ast)

    def obj_assg_spread(self, ast):
        return CryoSpread(ast)

    def arr_spread(self, ast):
        return CryoSpread(ast)