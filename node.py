from typing import List

class Node:

    def __init__(self, n_entries : int, degree : int) -> None:
        self.n_entries = n_entries
        self.keys = [None] * (degree)
        self.values = [None] * (degree)
        self.children : List[Node] = [None] * (degree + 1)

    def get_children(self):
        return self.children[:self.n_entries + 1]
    
    def get_keys(self):
        return self.keys[:self.n_entries]
    
    def get_values(self):
        return self.values[:self.n_entries]
    
    # returns the index of the smallest key greater than or equal to the informed key
    def get_index(self, key):
        i = len(self) - 1
        while i >= 0 and key < self.keys[i]:
            i -= 1
        return i

    def __len__(self):
        return self.n_entries

    def __repr__(self) -> str:
        output = '['
        for k in self.get_keys():
            output += f'key: {k}, '
        return output + ']'