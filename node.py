class Node:

    def __init__(self, n_elements : int, max_entries : int) -> None:
        self.n_elements = n_elements
        self.max_entries = max_entries
        self.keys = [None] * (max_entries - 1)
        self.values = [None] * (max_entries - 1)
        self.children = [None] * (max_entries)

    def __len__(self):
        return self.n_elements

    def __repr__(self) -> str:
        return f'{[e for i, e in enumerate(self.keys) if i < self.n_elements]}'