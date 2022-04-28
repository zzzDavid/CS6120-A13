# Tiny SuperOptimizer

Tiny SuperOptimizer is a program synthesis tool that generates a minimum Bril program from an input Python function.

## Introduction

The idea of implementing a superoptimizer comes from this [paper](https://dl.acm.org/doi/10.1145/36177.36194). Given an instruction set, the superoptimizer finds the shortest program to compute a function. 

## Demo

Tiny SuperOptimizer takes a Python function as input, for example:
```python
def f(x, y):
    a = x * 2 + y
    b = a * 5
    c = b * (128 // 4)
    return c
```

The tiny superoptimizer takes in the function and arg names as input, synthesize the minimum program and convert to Bril's json form:

```python
tree, holes = superoptimize(f, ['x'])
converter = to_bril(tree, holes)
print(json.dumps(converter.bril_prog, indent=4))
```

The result looks like this:

```sh
$ python main.py | bril2txt
@main(x: int, y: int) {
  v20: int = const 160;
  v1: int = mul v20 y;
  v12: int = const 6;
  v0: int = shl x v12;
  v0: int = add v0 v1;
  print v0;
}
```

As the result, the output program is a simplified version of the input Python function. A print instruction is added to display the result.

## Implementation

The idea of synthesizing a minimum program is traversing the search space of `n` instructions, with `n` ranging from 1 to a preset maximum number of instruction. 

The optimizer enumerates all combinations of instruction choices and formulate a proof problem for each program.
For each enumerated program in the search space, it uses `hole` variables to encode the operands. The optimizer uses Z3 SMT solver to solve the proof problem, and keep traversing and increasing `n` until the solver outputs a valid solution. 

There are four steps: 
1. Build an AST for the Python function, and create a Z3 expression from the AST.
2. Start from `n=1` and enumerate all possible programs in the search space, formulate a problem for each.
3. Increase `n` until Z3 outputs a valid solution or reaches the maximum of `n`.
4. Convert the output program to Bril's json format.

The two key parts of the process are generating operand choice encodings and enumerate all cases in the search space.

### Encode operand choices
The operand of an instruction can be one of the following situations:
- one of the input variables
- a constant (a hole that we want to fill)
- the result of a previous operation.

We the instruction set to binary operations, thus The optimizer encode the operand as either one of the input variables or a constant. For example, with three inputs `x0`, `x1`, and `x2`, The optimizer encode the operand as:

```
(h2 ? (h1 ? x2 : (h0 ? x1 : x0)) : h3)
```

`h0` and `h1` select one of the input variables, and `h2` select between input variables and a constant `h3`.

### Generate the search space

With the operand encoded, The optimizer can enumerate all operation combinations given the number of instruction `n`. 
Specifically, the implementation is here: [sample(n, vars)](https://github.com/zzzDavid/CS6120-A13/blob/main/search_space.py#L35).

## Discussion

We limit the "instruction set" to a small group of binary operations:
```python
# set of operations used in superoptimization
# sorted by computation cost, from low to high
self.ops = ['<<', '>>', '+', '-', '*', '/']
```
And the optimizer chooses operations with cheaper computation cost over the expensive ones.

Even though the scope of problem is limited, the search space still grows exponentially when `n` increases. For the above example, the optimizer finds a solution in about 3 seconds, while more complex input function may take tens of minutes to yield a solution.
