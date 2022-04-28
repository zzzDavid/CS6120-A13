# Tiny SuperOptimizer

Tiny SuperOptimizer is a program synthesis tool that generates a minimum Bril program from an input Python function.

## Introduction

The idea of implementing a superoptimizer comes from this [paper](https://dl.acm.org/doi/10.1145/36177.36194). Given an instruction set, the superoptimizer finds the shortest program to compute a function. 

## A Demo

Tiny SuperOptimizer takes a Python function as input, for example:
```python
def f(x):
    a = x * 2 + 8
    c = a * 128 + 1
    d = c * 2 + a
    return d
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
@main(x: int) {
  v12: int = const 10;
  v9: int = const 1;
  v0: int = shl x v9;
  v0: int = add v0 v12;
  print v0;
}
```

## Implementation

### Encode argument choice

## Discussion


