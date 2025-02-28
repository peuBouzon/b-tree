from typing import List
from node import Node
from entry import Entry
import math


class BTree:
    def __init__(self, max_entries_per_node = 1000) -> None:
        self.max_entries_per_node = max_entries_per_node
        self.root = Node(0, max_entries_per_node)
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

        return self._search(node.children[i], key, height - 1)
        
    def put(self, key, value):
        if len(self.root) >= self.max_entries_per_node - 1:
            old_root = self.root
            new_root = Node(0, self.max_entries_per_node)
            new_root.children[0] = old_root
            self.root = new_root
            self._split_child(new_root, 1, old_root, self.height)
            print(new_root)
            self._insert(new_root, key, value, self.height)
        else:
            self._insert(self.root, key, value, self.height)

    def _insert(self, node : Node, key, value, height : int):
        i = len(node) - 1
        if height == 0:
            while i >= 1 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
            node.n_elements += 1
        else:
            while i >= 1 and key < node.keys[i]:
                i -= 1
            i = i + 1
            child = node.children[i]
            if len(child) == self.max_entries_per_node - 1:
                self._split_child(node, i, child)
                if key > node.keys[i]:
                    i += 1
            self._insert(child, key, value, height - 1)

    def _split_child(self, node : Node, index : int, child : Node, height_child : int):
        index_median = math.ceil(self.max_entries_per_node / 2) - 1
        new_node = Node(self.max_entries_per_node // 2, self.max_entries_per_node)
        for j in range(1, index_median):
            new_node.keys[j] = child.keys[j + index_median]

        if height_child != 0:
            for j in range(0, index_median):
                new_node.children[j] = child.children[j + index_median]

        child.n_elements = self.max_entries_per_node - index_median

        for j in range(len(node) + 1, index, -1):
            node.children[j] = node.children[j - 1]

        for j in range(len(node), index, -1):
            node.keys[j] = node.keys[j - 1]

        node.children[index] = new_node
        node.keys[index] = new_node.keys[0]
        node.n_elements += 1


    def delete(self, key):
        pass