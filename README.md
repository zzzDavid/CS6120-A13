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

## Implementation

### Encode argument choice

## Discussion


