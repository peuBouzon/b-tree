from typing import List
from entry import Entry

class Node:
    def __init__(self, n_elements, max_entries) -> None:
        self.n_elements = n_elements
        self.max_entries = max_entries
        self.entries : List[Entry] = [None] * max_entries

    def __len__(self):
        return self.n_elements
    
    def insert(self, entry : Entry, index):
        for i in range(self.n_elements, index, -1):
            self.entries[i] = self.entries[i-1]
        self.entries[index] = entry
        self.n_elements += 1

    def split(self):
        new_node = Node(len(self) // 2, self.max_entries)
        self.n_elements //= 2
        for i in range(0, self.max_entries // 2):
            new_node.entries[i] = self.entries[i + self.max_entries // 2]
        return self, new_node

    def __repr__(self) -> str:
        return f'{[e for i, e in enumerate(self.entries) if i < self.n_elements]}' 
    

class Entry:
    def __init__(self, key, value, next_node : Node) -> None:
        self.key = key
        self.value = value
        self.next_node = next_node