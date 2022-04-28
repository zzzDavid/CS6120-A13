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

The idea of synthesizing a minimum program is traversing the search space of `n` instructions, `n` starts from 1 and ranges to a preset maximum number. We enumerate all combinations of instruction choices and formulate a proof problem for each.
For each enumerated program in the search space, we use `hole` variables to encode the operands. We use Z3 SMT solver to solve the proof problem, and keep traversing and increasing `n` until the solver outputs a valid solution. 

### Encoding argument choices

### Generate the search space


## Discussion


