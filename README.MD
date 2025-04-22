# B‑Tree Implementation in Python

This repository provides a simple B‑Tree data structure with insert, search and delete operations, as well as a CLI tool to process batch commands.

## Repository Structure

- [btree.py](btree.py) – Core `BTree` class implementing insertion, search, deletion and node splits/merges.  
- [node.py](node.py) – `Node` class used internally by `BTree`.  
- [cli.py](cli.py) – CLI script: reads commands from an input file and writes results + final tree to an output file.  
- [test_btree_.py](test_btree_.py) – Unit tests for the split‐child operation in `BTree`.

## Requirements

- Python 3.6+

## Usage

### As a Library

```python
from btree import BTree

bt = BTree(degree=4)
bt.put(10, "ten")
bt.put(20, "twenty")
print(bt.get(10))     # => "ten"
bt.delete(10)
print(bt.get(10))     # => None
```

### With the CLI

``` python cli.py input.py output.py ```

where the input format is as follows:

1. First line: degree of the B‑Tree (minimum 4).
2. Second line: number of operations.
3. Remaining lines: commands of form:
    - I key,value – insert or update
    - R key – remove
    - B key – search (writes status to output)

Example:

```
4
15
I 20, 20
I 75, 75
I 77, 77
I 78, 78
I 55, 55
I 62, 62
I 51, 51
I 40, 40
I 60, 60
I 45, 45
R 78
B 15
B 40
B 25
B 78
```