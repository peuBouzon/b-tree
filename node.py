from typing import List
class Node:

    def __init__(self, n_entries : int, degree : int) -> None:
        self.n_entries = n_entries
        self.keys = [None] * (degree - 1)
        self.values = [None] * (degree - 1)
        self.children : List[Node] = [None] * (degree)


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

    def remove(self, index, include_children = True):
        if index >= 0:
            for j in range(index, len(self) - 1):
                self.keys[j] = self.keys[j + 1]
                self.values[j] = self.values[j + 1]
            if include_children:
                for j in range(index + 1, len(self)):
                    self.children[j] = self.children[j + 1]
        self.n_entries -= 1
    
    def __len__(self):
        return self.n_entries

    def __repr__(self) -> str:
        #return str(self.get_keys())
        return str([f'{k} -> {p}' for k, p in zip(self.get_keys(), self.get_values())])