import unittest
from btree import BTree, Node
import random
class TestBTree(unittest.TestCase):

    def test_split_child_odd_degree(self):
        degrees = [4, 5, 1000, 1001, 100000, 100001]

        for degree in degrees:
            with self.subTest(degree=degree):
                btree = BTree(degree)
                parent_node = Node(0, degree)
                child = Node(degree - 1, degree)
                initial_keys = [random.randint(0, 100) for _ in range(degree - 1)]
                initial_values = [random.randint(0, 100) for _ in range(degree - 1)]
                child.keys = initial_keys
                child.values = initial_values
                half = (degree - 1) // 2
                parent_node.children[0] = child
                btree._split_child(parent_node, 0, child)
                self.assertEqual(parent_node.keys[:parent_node.n_entries], [initial_keys[half]])
                self.assertEqual(parent_node.values[:parent_node.n_entries], [initial_values[half]])
                self.assertEqual(parent_node.n_entries, 1)
                self.assertEqual(parent_node.children[0].n_entries, half)
                self.assertEqual(parent_node.children[0].keys[:parent_node.children[0].n_entries], initial_keys[:half])
                self.assertEqual(parent_node.children[0].values[:parent_node.children[0].n_entries], initial_values[:half])
                self.assertEqual(parent_node.children[1].n_entries, half - 1 if (degree - 1) % 2 == 0 else half)
                self.assertEqual(parent_node.children[1].keys[:parent_node.children[1].n_entries], initial_keys[half + 1:])
                self.assertEqual(parent_node.children[1].values[:parent_node.children[1].n_entries], initial_values[half + 1:])

if __name__ == '__main__':
    unittest.main()