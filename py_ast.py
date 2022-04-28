from re import A


class ASTNode(object):
    """A node in the abstract syntax tree.

    This is a base class for all nodes in the AST.
    """

    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.children))

    def __add__(self, rhs):
        return Add(self, rhs)
    
    def __sub__(self, rhs):
        return Sub(self, rhs)

    def __mul__(self, rhs):
        return Mul(self, rhs)
    
    def __floordiv__(self, rhs):
        return Div(self, rhs)

    def __lshift__(self, rhs):
        return Shl(self, rhs)

    def __rshift__(self, rhs):
        return Shr(self, rhs)

class Var(ASTNode):
    """A variable."""
    def __init__(self, name):
        super().__init__([])
        self.data = 'var'
        self.children = [name]

class Num(ASTNode):
    """A literal number."""

    def __init__(self, value):
        super().__init__([])
        self.data = 'num'
        self.children = [value]

class Add(ASTNode):
    """Addition."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'add'


class Sub(ASTNode):
    """Subtraction."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'sub'

class Mul(ASTNode):
    """Multiplication."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'mul'

class Div(ASTNode):
    """Division."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'div'

class Shl(ASTNode):
    """Shift left."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'shl'

class Shr(ASTNode):
    """Shift right."""
    
    def __init__(self, lhs, rhs):
            super().__init__([lhs, rhs])
            self.data = 'shr'

def create_ast(function, args):
    """Create an AST from a function."""
    args = [Var(arg) for arg in args]
    return function(*args)

def ast_print(tree):
    """Print an AST."""
    print(tree)
    if hasattr(tree, 'children'):
        for child in tree.children:
            ast_print(child)

if __name__ == "__main__":
    # test ast
    def f(x, y):
        c = x + y
        d = x - c 
        return d

    ast = create_ast(f, ['x', 'y'])
    # ast_print(ast)
    print(ast)

    # let's see if we can make z3 expr
    from main import z3_expr
    print(z3_expr(ast))