from node import Node

class BTree:
    def __init__(self, degree = 1000) -> None:
        self.degree = degree
        self.root = Node(0, degree)
        self.height = 0

    def get(self, key):
        return self._search(self.root, key, self.height)
    
    def _search(self, node : Node, key, height : int):
        # finds the index of the smallest key greater than or equal to the searched key
        i = 0
        while i <= len(node):
            if i+1 == len(node) or key < node.keys[i+1]:
                break
            i += 1

        # if the key is found, return its value
        if key == node.keys[i]:
            return node.values[i]

        # if it's not found and is a leaf, search is over
        if height == 0:
            return

        # else search in the child node
        return self._search(node.children[i + 1], key, height - 1)

    def put(self, key, value):
        # if the root is full
        if len(self.root) >= self.degree - 1:
            old_root = self.root
            # we create a new root
            new_root = Node(0, self.degree)
            # set the old root as its child
            new_root.children[0] = old_root
            self.root = new_root
            # increase the height
            self.height += 1
            # and split the old root
            self._split_child(self.root, 0, new_root.children[0], self.height - 1)
            # after that, we can insert on the new root
            self._insert_non_full(self.root, key, value, self.height) 
        else:
            self._insert_non_full(self.root, key, value, self.height)

    def _insert_non_full(self, node : Node, key, value, height : int):
        # if is leaf
        if height == 0:
            self._insert_non_full_leaf(node, key, value)
        else:
            # find the index of the smallest key greater then the new key
            i = len(node) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i = i + 1

            # if the child is full, we split it
            if len(node.children[i]) >= self.degree - 1:
                self._split_child(node, i, node.children[i], height - 1)
                # _split_child adds a key to the parent node,
                # we need to check if this new key is now the smallest key greater than the key to be inserted
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key, value, height - 1)
    
    def _insert_non_full_leaf(self, node : Node, key, value):
        
        # make a binary search to find the key and update its value if it's already present
        index_key = self.binary_search(node.keys[:node.n_entries], key)
        if index_key is not None:
            node.values[index_key] = value
            return

        # shift every value greater than the new key to the right
        i = len(node) - 1
        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            node.values[i + 1] = node.values[i]
            i -= 1

        i += 1

        # insert the new key and value at the right position
        node.keys[i] = key
        node.values[i] = value
        node.n_entries += 1
    
    def binary_search(self, keys, key):
        if not keys:
            return

        if len(keys) in [1, 2]: 
            return 0 if keys[0] == key else 1 if len(keys) == 2 and keys[1] == key else None

        mid = len(keys) // 2

        if keys[mid] == key:
            return mid
        
        if keys[mid] > key:
            return self.binary_search(keys[:mid], key)

        return self.binary_search(keys[mid + 1:], key)

    def _split_child(self, parent : Node, child_index : int, child : Node, child_height : int):
        n_keys_child = len(child)
        half = n_keys_child // 2
        new_sibling = Node(half - 1 if n_keys_child % 2 == 0 else half, self.degree)
        child.n_entries = half

        for j in range(0, len(new_sibling)):
            index = j + half + 1
            new_sibling.keys[j] = child.keys[index]
            new_sibling.values[j] = child.values[index]
        
        if child_height > 0:
            for j in range(0, len(new_sibling) + 1):
                new_sibling.children[j] = child.children[j + half + 1]

        for i in reversed(range(child_index, len(parent))):
            parent.keys[i + 1] = parent.keys[i]
            parent.values[i + 1] = parent.values[i]

        for i in reversed(range(child_index + 1, len(parent) + 1)):
            parent.children[i + 1] = parent.children[i]

        parent.keys[child_index] = child.keys[half]
        parent.values[child_index] = child.values[half]
        parent.children[child_index + 1] = new_sibling
        parent.n_entries += 1

    def delete(self, key):
        pass