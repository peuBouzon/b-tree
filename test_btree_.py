import unittest
from btree import BTree, Node

class TestBTree(unittest.TestCase):
    def test_split_child(self):
        degrees = [4, 1000, 100000]

        for degree in degrees:
            with self.subTest(degree=degree):
                btree = BTree(degree)

                # create a parent node with -1 -> -1 entry and two children
                parent_node = Node(1, degree)
                parent_node.keys = [-1] + [None] * (degree - 2)
                parent_node.values = [-1] + [None] * (degree - 2)

                # create a full child
                child = Node(degree - 1, degree)
                initial_keys = list(range(degree - 2, -1, -1))
                initial_values = list(range(degree - 2, -1, -1))
                initial_children = list(range(degree))
                child.keys = initial_keys
                child.values = initial_values
                child.children = initial_children

                parent_node.children = [Node(1, degree)] + [child] * (degree - 1)

                # second child is full, so we are going to split it
                btree._split_child(parent_node, 1, child, 1)

                half = (degree - 1) // 2
                # the parent node should have the middle key and value of the full child
                self.assertEqual(parent_node.keys[:parent_node.n_entries], [-1, initial_keys[half]])
                self.assertEqual(parent_node.values[:parent_node.n_entries], [-1, initial_values[half]])
                # the number of entries int the parent node should be increased by 1
                self.assertEqual(parent_node.n_entries, 2)
                
                ex_full_child = parent_node.children[1]

                # the then full child should contain the first half of the entries
                self.assertEqual(ex_full_child.n_entries, half)
                self.assertEqual(ex_full_child.keys[:ex_full_child.n_entries], initial_keys[:half])
                self.assertEqual(ex_full_child.values[:ex_full_child.n_entries], initial_values[:half])
                self.assertEqual(ex_full_child.children[:ex_full_child.n_entries + 1], initial_children[:half + 1])

                # and a new child should be created with the other half of the entries minus the middle entry
                new_child = parent_node.children[2]
                self.assertEqual(new_child.n_entries, half - 1 if (degree - 1) % 2 == 0 else half)
                self.assertEqual(new_child.keys[:new_child.n_entries], initial_keys[half + 1:])
                self.assertEqual(new_child.values[:new_child.n_entries], initial_values[half + 1:])
                self.assertEqual(new_child.children[:new_child.n_entries + 1], initial_children[half + 1:])

if __name__ == '__main__':
    unittest.main()