from typing import List
class Node:

    def __init__(self, n_entries : int, degree : int) -> None:
        self.n_entries = n_entries
        self.keys = [None] * (degree - 1)
        self.values = [None] * (degree - 1)
        self.children : List[Node] = [None] * (degree)

    def __len__(self):
        return self.n_entries

    def __repr__(self) -> str:
        return f'{self.keys[:self.n_entries]}'