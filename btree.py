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
            for entry in node.entries:
                if entry.key == key:
                    return entry.value
        else:
            n_entries_on_node = len(node)
            for i in range(n_entries_on_node):
                # find the greater entry whose value is smaller or equal to the key 
                if i+1 == n_entries_on_node or key < node.entries[i+1].key:
                    return self._search(node.entries[i].next_node, key, height - 1)
        return
    
    def put(self, key, value):
        if key is None:
            raise ValueError(BTree.INVALID_KEY_MESSAGE)
        new_node : Node = self._insert(self.root, key, value, self.height)

        if not new_node is None:
            new_root = Node(2, self.max_entries_per_node)
            new_node.entries[0] = Entry(self.root.entries[0].key, None, self.root)
            new_node.entries[1] = Entry(new_node.entries[0].key, None, new_node)

        self.root = new_root
        self.height += 1

    def _insert(self, node : Node, key, value, height : int):
        is_internal_node = height != 0
        new_entry = None

        index_new_entry = None
        if is_internal_node:
            n_entries_on_node = len(node)
            for i in range(n_entries_on_node):
                if i+1 == n_entries_on_node or key < node.entries[i+1].key:
                    new_node : Node = self._insert(node.entries[i], key, value, height - 1)
                    if new_node is None:
                        return

                    index_new_entry = i + 1
                    new_entry = Entry(new_node.entries[0].key, None, new_node)
                    break
        else:
            new_entry = Entry(key, value, None)
            for i in range(n_entries_on_node):
                if key < node.entries[i].key:
                    index_new_entry = i
                    break

        for i in reversed(range(0, self.max_entries_per_node)):
            node.entries[i] = node.entries[i-1]
        node.entries[index_new_entry] = new_entry
        node.n_elements += 1

        return self._split_and_get_new_node(node) if len(node) >= self.max_entries_per_node else None
        
    def _split_and_get_new_node(self, node : Node):
        new_node = Node(self.max_entries_per_node, len(node) // 2)
        node.n_elements //= 2
        for i in range(0, self.max_entries_per_node // 2):
            new_node.entries[i] = node.entries[i + self.max_entries_per_node // 2]
        return new_node 

    def delete(self, key):
        self.put(key, None)
