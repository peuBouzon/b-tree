from typing import List
from entry import Entry

class Node:
    def __init__(self, max_entries, n_elements) -> None:
        self.n_elements = n_elements
        self.max_entries = max_entries
        self.entries : List[Entry] = [] * n_elements

    def __len__(self):
        return self.n_elements