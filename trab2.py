from btree import BTree
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        max_entries_per_node = int(f.readline().strip())
        n_operations = int(f.readline().strip())
        btree = BTree(max_entries_per_node)
        for line in f:
            args = line.split(' ')
            command = args[0].strip()
            arg1 = int(args[1].strip().replace(',', ''))
            if command == 'I':
                btree.put(arg1, int(args[2].strip().replace(',', '')))
            elif command == 'R':
                btree.delete(arg1)
            elif command == 'B':
                print('O REGISTRO ESTA NA ARVORE!' if btree.get(arg1) is not None else 'O REGISTRO NAO ESTA NA ARVORE!')