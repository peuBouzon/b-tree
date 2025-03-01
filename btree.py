from typing import List
from node import Node
from entry import Entry
import math


class BTree:
    def __init__(self, degree = 1000) -> None:
        self.degree = degree
        self.root = Node(0, degree)
        self.height = 0
        self.n_entries = 0

    def get(self, key):
        return self._search(self.root, key, self.height)
    
    def _search(self, node : Node, key, height : int):
        i = 0
        while i <= len(node):
            if i+1 == len(node) or key < node.keys[i+1]:
                break
            i += 1

        if key == node.keys[i]:
            return node.values[i]

        if height == 0:
            return

        return self._search(node.children[i + 1], key, height - 1)

    def put(self, key, value):
        if len(self.root) >= self.degree - 1:
            old_root = self.root
            new_root = Node(0, self.degree)
            new_root.children[0] = old_root
            self.root = new_root
            self.height += 1
            self._split_child(self.root, 0, new_root.children[0])
            self._insert_non_full(self.root, key, value, self.height) 
        else:
            self._insert_non_full(self.root, key, value, self.height)

    def _insert_non_full(self, node : Node, key, value, height : int):
        if height == 0: # is leaf
            self._insert_non_full_leaf(node, key, value)
        else:
            # find the index of the smallest key greater then the new key
            # this will be used to insert into the correct child

            i = len(node) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i = i + 1

            # split child if full
            if len(node.children[i]) >= self.degree - 1:
                self._split_child(node, i, node.children[i])
                # split child adds a key to the parent node,
                # we need to check if this key is the smallest key greater than the key to be inserted
                if key > node.keys[i + 1]:
                    i += 1

            self._insert_non_full(node.children[i], key, value, height - 1)

    # FIXME: leafs don't need to copy children
    def _split_child(self, parent : Node, child_index : int, child : Node):
        n_keys_child = len(child)
        half = n_keys_child // 2
        new_sibling = Node(half - 1 if n_keys_child % 2 == 0 else half, self.degree)
        child.n_entries = half

        new_sibling.children[0] = child.children[half]
        for j in range(0, len(new_sibling)):
            index_child = j + half + 1
            new_sibling.keys[j] = child.keys[index_child]
            new_sibling.values[j] = child.values[index_child]
            new_sibling.children[j + 1] = child.children[index_child]

        for i in range(len(parent) - 1, child_index - 2, -1):
            if i >= 0:
                parent.keys[i + 1] = parent.keys[i]
                parent.values[i + 1] = parent.values[i]
            parent.children[i + 2] = parent.children[i + 1]

        parent.keys[child_index] = child.keys[half]
        parent.values[child_index] = child.values[half]
        parent.children[child_index] = new_sibling
        parent.n_entries += 1

    def _insert_non_full_leaf(self, node : Node, key, value):
        i = len(node) - 1
        while i >= 0 and key < node.keys[i]:
            node.keys[i + 1] = node.keys[i]
            node.values[i + 1] = node.values[i]
            i -= 1

        i += 1
        if node.keys[i] == key:
            node.values[i] = value
            return

        node.keys[i] = key
        node.values[i] = value
        node.n_entries += 1

    def delete(self, key):
        pass