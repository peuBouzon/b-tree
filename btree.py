from node import Node
from typing import List
import math

class BTree:
    def __init__(self, degree = 1000) -> None:
        self.degree = degree
        self.root = Node(0, degree)
        self.height = 0
        self.min_keys_necessary = math.ceil(self.degree / 2) - 1

    def get(self, key):
        return self._search(self.root, key, self.height)[0]
    
    def _search(self, node : Node, key, height : int):
        # finds the index of the smallest key greater than or equal to the searched key
        i = 0
        while i <= len(node):
            if i+1 == len(node) or key < node.keys[i+1]:
                break
            i += 1

        # if the key is found, return its value
        if key == node.keys[i]:
            return node.values[i], node, i, height

        # if it's not found and is a leaf, search is over
        if height == 0:
            return None, None, None, None

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
            # find the index of the smallest key greater than or equal to the new key
            i = node.get_index(key) + 1

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
        index_key = self._find_index(node.get_keys(), key)
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
    
    # this is just a binary search
    def _find_index(self, keys, key):
        if not keys:
            return

        if len(keys) in [1, 2]: 
            return 0 if keys[0] == key else 1 if len(keys) == 2 and keys[1] == key else None

        mid = len(keys) // 2

        if keys[mid] == key:
            return mid
        
        if keys[mid] > key:
            return self._find_index(keys[:mid], key)

        return self._find_index(keys[mid + 1:], key)

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

    def delete(self, search_key):
        # if the tree is empty, there is nothing to delete
        if len(self.root) <= 0:
            return
        
        self._remove(self.root, search_key, self.height)
        # the call above can remove one key from the root to make sure the child has at least
        # min_keys_necessary + 1, so we need to check if the root is empty
        
        if len(self.root) == 0:
            # if root is an internal node
            if self.height > 0:
                # we can replace it with its left child (its children have been merged, so the right child is gone)
                self.root = self.root.children[0]
            else:
                # if root is a leaf, we can create a new empty Node
                self.root = Node(0, self.degree)

    def _remove(self, node : Node, key, height : int):
        i = node.get_index(key)
        
        # the key is found
        if i >= 0 and key == node.keys[i]:
            if height == 0:
                # CASE 1: the key is in a leaf node
                # recall that we make sure the node has at least one extra element before _remove is called,
                # so, we can just remove the key
                node.remove(i, False)
            else:
                # CASE 2: the key is in an internal node
                self._remove_from_non_leaf(node, i, height)
        else:
            if height == 0:
                return
            
            # CASE 3: the key is not in the current node
            # we need to find the child that contains the key
            # but first, we need to make sure the child has at least the minimum number of keys
            if len(node.children[i + 1]) < self.min_keys_necessary + 1:
                # TODO: fill the child before remove
                pass

            self._remove(node.children[i + 1], key, height - 1)

    def _remove_from_non_leaf(self, node : Node, index : int, height):

        # CASE 2.A: the left child can lose a key
        if len(node.children[index]) > self.min_keys_necessary:
            child : Node = node.children[index]

            # get the leaf with the greatest key from the subtree rooted at the left child
            h = height - 1
            while h > 0:
                child = child.get_children()[-1]
                h -= 1

            # and replace the key to be removed with it
            node.keys[index] = child.get_keys()[-1]
            node.values[index] = child.get_values()[-1]
            
            # after that, we can remove the key from the left child
            self._remove(node.children[index], child.get_keys()[-1], 0)
        
        # CASE 2.B: the right child can lose a key
        elif len(node.children[index + 1]) > self.min_keys_necessary:
            child : Node = node.children[index + 1]

            # get the leaf with the smallest key from the subtree rooted at the right child
            h = height - 1
            while h > 0:
                child = child.get_children()[0]
                h -= 1

            # same analysis as with the left child
            node.keys[index] = child.get_keys()[0]
            node.values[index] = child.get_values()[0]
            self._remove(node.children[index + 1], child.get_keys()[0], 0)

        # CASE 2.C: none of the adjancent children can lose a key
        else:
            # in this case, we can merge the children
            self._merge(node.children[index], node.children[index + 1])

            # and remove the key
            node.remove(index)

    def _merge(self, left : Node, right : Node):
        for i in range(self.min_keys_necessary, 2 * self.min_keys_necessary):
            left.keys[i] = right.keys[i - self.min_keys_necessary]
            left.values[i] = right.values[i - self.min_keys_necessary]
            left.children[i + 1] = right.children[i - self.min_keys_necessary + 1]
        left.n_entries = 2 * self.min_keys_necessary

    def __repr__(self):
        queue = [(self.root, self.height)]

        output = ''
        last_height = self.height
        while queue:
            node, height = queue.pop(0)
            if last_height > height:
                output += '\n'
                last_height = height
            output += f' {node}'
            if height > 0:
                for child in node.get_children():
                    queue.append((child, height - 1))

        return output

