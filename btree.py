from node import Node
import math

# TODO: implement non-preemptive insert

class BTree:
    def __init__(self, degree = 1000) -> None:
        self.degree = degree
        self.root = Node(0, degree)
        self.height = 0
        self.min_keys_necessary = math.ceil(self.degree / 2) - 1

    def get(self, key):
        return self._search(self.root, key, self.height)

    def _search(self, node : Node, key, height : int):
        # finds the index of the smallest key greater than or equal to the searched key
        i = node.get_index(key)

        # if the key is found, return its value
        if i >= 0 and key == node.keys[i]:
            return node.values[i]

        # if it's not found and is a leaf, search is over
        if height == 0:
            return None

        # else search in the child node
        return self._search(node.children[i + 1], key, height - 1)

    # FIXME: duplicated keys
    def put(self, key, value):
        entry = self._insert(self.root, key, value, self.height)
        if entry is not None:
            root = Node(1, self.degree)
            root.keys[0] = entry[0]
            root.values[0] = entry[1]
            # TODO: check if new_child should be first or second child
            root.children[0] = self.root
            root.children[1] = entry[2]
            self.root = root
            self.height += 1

    def _insert(self, node : Node, key, value, height: int):
        key_index = node.get_index(key)
        child_index = key_index + 1
        if (key_index < len(node)) and node.keys[key_index] == key:
            node.values[key_index] = value
            return
        if height > 0:
            entry = self._insert(node.children[child_index], key, value, height - 1)
            if entry is not None:
                median_key, median_value, new_child = entry
                # if the parent node is not full
                for i in reversed(range(child_index, len(node))):
                    node.keys[i + 1] = node.keys[i]
                    node.values[i + 1] = node.values[i]

                for i in reversed(range(child_index + 1, len(node) + 1)):
                    node.children[i + 1] = node.children[i]

                node.keys[child_index] = median_key
                node.values[child_index] = median_value
                node.children[child_index + 1] = new_child
                node.n_entries += 1
                if len(node) >= self.degree:
                    return self._split(node, height)
        else:
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
            if len(node) >= self.degree:
                return self._split(node, height)

    def _split(self, node : Node, height : int):
        n_keys_child = len(node)
        half = n_keys_child // 2
        new_sibling = Node(half - 1 if n_keys_child % 2 == 0 else half, self.degree)
        node.n_entries = half

        for j in range(0, len(new_sibling)):
            index = j + half + 1
            new_sibling.keys[j] = node.keys[index]
            new_sibling.values[j] = node.values[index]
        
        if height > 0:
            for j in range(0, len(new_sibling) + 1):
                new_sibling.children[j] = node.children[j + half + 1]
        return node.keys[half], node.values[half], new_sibling

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
                # we can replace it with its left child (its children would have been merged, so the right child is gone)
                self.root = self.root.children[0]
                self.height -= 1

            # if root is a leaf, we can leave it as an empty Node

    def _remove(self, node : Node, key, height : int):
        i = node.get_index(key)
        # the key is found
        if i >= 0 and key == node.keys[i]:
            if height == 0:
                # CASE 1: the key is in a leaf node
                # recall that we made sure the node had at least one extra element before _remove is called,
                # so, we can just remove the key
                node.remove(i, False)
            else:
                # CASE 2: the key is in an internal node
                self._remove_from_non_leaf(node, i, height)
        else:
            if height == 0:
                return

            # CASE 3: the key is not in the current node
            # we will search it in the correct child
            # but first, we need to make sure this child has at least min_keys_necessary + 1
            child = node.children[i + 1]
            if len(child) < self.min_keys_necessary + 1:
                # CASE 3.A: if any adjascent sibling can lend a key, we borrow from it
                left_sibling = node.children[i] if i >= 0 else None
                right_sibling = node.children[i + 2] if i + 2 <= len(child) else None
                if left_sibling and len(left_sibling) > self.min_keys_necessary:
                    self._rotate_right(node, child, left_sibling, i)
                elif right_sibling and len(right_sibling) > self.min_keys_necessary:
                    self._rotate_left(node, child, right_sibling, i)
                else:
                    # CASE 3.B: if no sibling can lend a key
                    if i >= 0:
                        # merge with left
                        self._merge(node, i)
                        child = node.children[i]
                    else:
                        # merge with right
                        self._merge(node, i + 1)
            self._remove(child, key, height - 1)

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
            # TODO: improve comments
            node.keys[index] = child.get_keys()[-1]
            node.values[index] = child.get_values()[-1]
            
            # after that, we can remove child.get_keys()[-1] from the left child
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
            # in this case, we can merge the children and set the key as the median value
            key = node.keys[index]
            self._merge(node, index)

            # then, we can remove the key from the result
            self._remove(node.children[index], key, height - 1)

    def _rotate_right(self, node: Node, child: Node, left_sibling : Node, i : int):
        # shift every value greater than the new key to the right

        if len(child) < self.degree:
            child.children[len(child) + 1] = child.children[len(child)]

        j = len(child)
        while j >= 0:
            child.keys[j + 1] = child.keys[j]
            child.values[j + 1] = child.values[j]
            child.children[j + 1] = child.children[j]
            j -= 1

        child.keys[0] = node.keys[i]
        child.values[0] = node.values[i]
        child.children[0] = left_sibling.get_children()[-1]
        child.n_entries += 1

        node.keys[i] = left_sibling.keys[len(left_sibling) - 1]
        node.values[i] = left_sibling.values[len(left_sibling) - 1]

        left_sibling.remove(-1, True)

    def _rotate_left(self, node: Node, child: Node, right_sibling : Node, i : int):
        child.keys[len(child)] = node.keys[i + 1]
        child.values[len(child)] = node.values[i + 1]
        child.children[len(child) + 1] = right_sibling.children[0]
        child.n_entries += 1
        node.keys[i + 1] = right_sibling.keys[0]
        node.values[i + 1] = right_sibling.values[0]
        right_sibling.remove(0, True)

    def _merge(self, node : Node, index):
        left : Node = node.children[index]
        right : Node = node.children[index + 1]
        left.keys[len(left)] = node.keys[index]
        left.values[len(left)] = node.values[index]
        for j in range(self.min_keys_necessary, 2 * self.min_keys_necessary):
            left.keys[j + 1] = right.keys[j - self.min_keys_necessary]
            left.values[j + 1] = right.values[j - self.min_keys_necessary]
            left.children[j + 2] = right.children[j - self.min_keys_necessary + 1]
        left.n_entries = 2 * self.min_keys_necessary + 1

        node.remove(index, True)

    def __repr__(self):
        queue = [(self.root, self.height)]

        output = ''
        last_height = self.height
        while queue:
            node, height = queue.pop(0)
            if last_height > height:
                output += '\n'
                last_height = height
            output += f'{node}'
            if height > 0:
                for child in node.get_children():
                    queue.append((child, height - 1))

        return output

