import itertools

class search_space(object):
    def __init__(self):
        # set of operations used in superoptimization
        # sorted by computation cost, from low to high
        self.ops = ['<<', '>>', '+', '-', '*', '/']
        """
        The search space only consider binary operations.
        The operand can be either:
        - one of the input variables
        - a constant (a hole that we want to fill)
        - the result of a previous operation
        """

    def gen_expr_str(self, op_choice, operands):
        return f"{operands[0]} {self.ops[op_choice]} {operands[1]}"

    def gen_var_encoding(self, h_idx, vars):
        # encode the choice of input variables
        # e.g. (h0 ? x1 : x0)
        #      (h1 ? x2 : (h0 ? x1 : x0))
        if len(vars) == 1:
            var_encoding = vars[0]
        else:
            n_select = len(vars) - 1
            rhs = vars[0]
            for i in range(n_select):
                cond = f"h{i + h_idx}"
                lhs = vars[i+1]
                rhs = f"({cond} ? {lhs} : {rhs})"
            var_encoding = rhs
        return var_encoding
    
    def sample(self, n, vars):
        """
        Sample n random expressions from the search space.
        vars: list of strings, input variable names
        """
        op_choices = itertools.product(*[[i for i in range(len(self.ops))]] * n)
        for op_choice in op_choices:
            hole_idx = 0
            var_encoding = self.gen_var_encoding(hole_idx, vars)
            hole_idx += (len(vars) - 1)
            op0 = f"(h{hole_idx} ? {var_encoding} : h{hole_idx+1})"
            hole_idx += 2
            for op in op_choice: # each operation
                var_encoding = self.gen_var_encoding(hole_idx, vars)
                hole_idx += (len(vars) - 1)
                op1 = f"(h{hole_idx} ? {var_encoding} : h{hole_idx+1})"
                hole_idx += 2
                op0 = self.gen_expr_str(op, [op0, op1])
            # yield
            print(op0)

# test
# ss = search_space()
# ss.sample(2, ['x0', 'x1'])