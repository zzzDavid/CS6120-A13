
from numpy import var


class to_bril(object):
    def __init__(self, tree, holes):
        self.tree = tree
        self.holes = holes
        self.instrs = []
        self.idx = 0
    
    def unique_name(self):
        name = "v" + str(self.idx)
        self.idx += 1
        return name

    def visit(self, tree, root_var):
        if tree.data == 'add':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'add',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'sub':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'sub',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'shl':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'shl',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'shr':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'shr',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'mul':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'mul',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'div':
            lhs = self.unique_name()
            rhs = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'div',
                'type': 'int',
                'args': [lhs, rhs]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], lhs)
            self.visit(tree.children[1], rhs)
        elif tree.data == 'if':
            cond = self.unique_name()
            true = self.unique_name()
            false = self.unique_name()
            instr = {
                'dest': root_var,
                'op': 'if',
                'type': 'int',
                'args': [cond, true, false]
            }
            self.instrs.append(instr)
            self.visit(tree.children[0], cond)
            self.visit(tree.children[1], true)
            self.visit(tree.children[2], false)
        elif tree.data == 'num':
            instr = {
                'dest': root_var,
                'op': 'const',
                'type': 'int',
                'value': int(tree.children[0])
            }
            self.instrs.append(instr)
        elif tree.data == 'var':
            var_name = str(tree.children[0])
            if var_name.startswith('h') and var_name in self.holes:
                instr = {
                    'dest': root_var,
                    'op': 'const',
                    'type': 'int',
                    'value': str(self.holes.get(var_name, var_name))
                }
                self.instrs.append(instr)
            else:
                instr = {
                    'dest': root_var,
                    'op': 'var',
                    'type': 'int',
                    'value': str(tree.children[0])
                }
                self.instrs.append(instr)

    # prog = dict()    

    # print(prog)

