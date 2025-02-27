from node import Node
from entry import Entry

class BTree:
    INVALID_KEY_MESSAGE = "The key to search should be informed."
    INVALID_MAX_ENTRIES_MESSAGE = "The number of entries per node should be even."

    def __init__(self, max_entries_per_node = 1000) -> None:

        if not max_entries_per_node % 2 == 0:
            raise ValueError(BTree.INVALID_MAX_ENTRIES_MESSAGE)

        self.max_entries_per_node = max_entries_per_node
        self.root = Node(0, max_entries_per_node)
        self.height = 0
        self.n_entries = 0

    def get(self, key):
        if key is None:
            raise ValueError(BTree.INVALID_KEY_MESSAGE)
        return self._search(self.root, key, self.height)
    
    def _search(self, node : Node, key, height : int):
        if height == 0:
            for i in range(len(node)):
                if node.entries[i].key == key:
                    return node.entries[i].value
        else:
            for i in range(len(node)):
                if i+1 == len(node) or key < node.entries[i+1].key: # find the greater entry whose value is smaller or equal to the key 
                    return self._search(node.entries[i].next_node, key, height - 1)

    def put(self, key, value):
        if key is None:
            raise ValueError(BTree.INVALID_KEY_MESSAGE)
        new_node : Node = self._insert(self.root, key, value, self.height)
        self.n_entries += 1
        if not new_node is None:
            new_root = Node(2, self.max_entries_per_node)
            new_root.entries[0] = Entry(self.root.entries[0].key, None, self.root)
            new_root.entries[1] = Entry(new_node.entries[0].key, None, new_node)
            self.root = new_root
            self.height += 1

    def _insert(self, node : Node, key, value, height : int):
        new_entry = None
        index_new_entry = 0

        if height != 0:
            n_entries_on_node = len(node)
            for i in range(n_entries_on_node):
                index_new_entry = i + 1
                if i+1 == n_entries_on_node or key < node.entries[i+1].key:
                    new_node : Node = self._insert(node.entries[i].next_node, key, value, height - 1)
                    if new_node is None:
                        return

                    new_entry = Entry(new_node.entries[0].key, None, new_node)
                    break
        else:
            new_entry = Entry(key, value, None)
            for i in range(len(node)):
                index_new_entry = i + 1
                if key == node.entries[i].key:
                    node.entries[i].value = value
                    self.n_entries -= 1
                    return
                if key < node.entries[i].key:
                    index_new_entry -= 1
                    break

        node.insert(new_entry, index_new_entry)

        if len(node) >= self.max_entries_per_node:
            return node.split()[1]

    def delete(self, key):
        self.put(key, None)
        self.n_entries -= 1
