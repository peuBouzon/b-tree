from btree import BTree
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    with open(args.input, 'r') as f:
        degree = int(f.readline().strip())
        n_operations = int(f.readline().strip())
        btree = BTree(max(degree, 4))
        processed = 0
        with open(args.output, 'w') as output_file:
            for line in f:
                args = line.split(' ')
                command = args[0].strip()
                arg1 = int(args[1].strip().replace(',', ''))

                if command == 'I':
                    btree.put(arg1, int(args[2].strip().replace(',', '')))
                elif command == 'R':
                    btree.delete(arg1)
                elif command == 'B':
                    output_file.write('O REGISTRO ESTA NA ARVORE!' if btree.get(arg1) is not None else 'O REGISTRO NAO ESTA NA ARVORE!')
                    if processed < n_operations - 1:
                        output_file.write('\n')
                processed += 1

            output_file.write('\n\n-- ÁRVORE B\n')
            output_file.write(str(btree).replace("'", ""))
