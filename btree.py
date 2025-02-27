from node import Node
from entry import Entry

class BTree:
    def __init__(self, max_entries_per_node = 1000) -> None:

        if not max_entries_per_node % 2 == 0:
            raise ValueError("The number of entries per node should be even.")
        self.max_entries_per_node = max_entries_per_node
        self.root = Node(0, max_entries_per_node)
        self.height = 0
        self.n_entries = 0

    def get(self, key):
        if key is None:
            raise ValueError("The key to search should be informed.")
        return self._search(self.root, key, self.height)
    
    def _search(self, node : Node, key, height : int):
        if height == 0:
            for entry in node.entries:
                if entry.key == key:
                    return entry.value
        else:
            n_entries_on_node = len(node)
            for i in range(n_entries_on_node):
                # find the greater entry whose value is smaller or equal to the key 
                if i+1 == n_entries_on_node or key < node.entries[i+1].key:
                    return self._search(node.entries[i].next_node, key, height - 1)
        return None