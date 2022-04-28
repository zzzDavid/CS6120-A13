

from weakref import ref


class to_bril(object):
    def __init__(self, tree, holes):
        self.tree = tree
        self.holes = holes
        self.instrs = []
        self.idx = 0
        self.args = []
        self.bril_prog = dict()
        self.convert()

    def convert(self):
        self.visit(self.tree, 'v0')
        self.post_process()
        arg_list = list()
        for arg in self.args:
            arg_list.append({
                'name': arg,
                'type': 'int'
            })
        self.bril_prog['functions'] = [
            {
                'name': 'main',
                'args': arg_list,
                'instrs': self.instrs
            }
        ]
    
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

    def post_process(self):
        """
        - Reverse the order of instruction
        - Remove all constant if operations
        - Inline all var operations
        """
        self.instrs.reverse()

        # Remove all constant if operations
        # Also add var to args
        new_instrs = []
        const_map = dict()
        var_map = dict() # var -> var, act as Context
        for instr in self.instrs:
            if instr['op'] == 'const':
                const_map[instr['dest']] = instr['value']
                new_instrs.append(instr)
            elif instr['op'] == 'if':
                cond = instr['args'][0]
                true = instr['args'][1]
                false = instr['args'][2]
                if cond in const_map:
                    if const_map[cond] == "0":
                        if false in var_map:
                            var_map[instr['dest']] = var_map[false]
                        else:
                            var_map[instr['dest']] = false
                    else:
                        if true in var_map:
                            var_map[instr['dest']] = var_map[true]
                        else:
                            var_map[instr['dest']] = true
            elif instr['op'] == 'var':
                var_map[instr['dest']] = instr['value']
                if instr['value'] not in self.args and not instr['value'].startswith('h'):
                    self.args.append(instr['value'])
            else:
                new_instrs.append(instr)
        self.instrs = new_instrs

        # Fold id operations and inline var operations
        for instr in self.instrs:
            if 'args' in instr:
                for idx, arg in enumerate(instr['args']):
                    if arg in var_map:
                        instr['args'][idx] = var_map[arg]


        # add print result instr
        self.instrs.append({
            'op': 'print',
            'args': ['v0']
        })

        # Simple DSE
        referenced_vars = set()
        for instr in self.instrs:
            if 'args' in instr:
                for arg in instr['args']:
                    referenced_vars.add(arg)
        new_instrs = []
        for instr in self.instrs:
            if 'dest' in instr and instr['dest'] in referenced_vars:
                new_instrs.append(instr)
            elif 'op' in instr and instr['op'] == 'print':
                new_instrs.append(instr)
        self.instrs = new_instrs

    # prog = dict()    

    # print(prog)

